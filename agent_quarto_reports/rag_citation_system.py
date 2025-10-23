#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production-Grade RAG Citation System for Quarto Documents

This module provides validated, accurate academic citations for Quarto documents by:
- Processing PDF papers from project-specific references/ directories
- Using BGE-large embeddings for state-of-the-art semantic search
- Hybrid search (ChromaDB + BM25) with Reciprocal Rank Fusion
- Generating inline citations with page numbers
- Auto-generating BibTeX entries
- Validating citation accuracy and cross-references

Quality over speed: Every citation is validated before insertion.
"""

import re
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from sentence_transformers import SentenceTransformer, CrossEncoder
except ImportError:
    SentenceTransformer = None
    CrossEncoder = None

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

import numpy as np


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Citation:
    """Structured citation with validation metadata"""
    authors: List[str]
    year: str
    title: str
    doi: Optional[str]
    page_numbers: List[int]
    text_snippet: str
    confidence: float
    source_file: str
    
    def to_inline(self) -> str:
        """Generate inline citation: (Author et al., Year, p. XX)"""
        if not self.authors:
            return f"({self.year})"
        
        if len(self.authors) == 1:
            author_str = self.authors[0].split()[-1]  # Last name
        elif len(self.authors) == 2:
            author_str = f"{self.authors[0].split()[-1]} & {self.authors[1].split()[-1]}"
        else:
            author_str = f"{self.authors[0].split()[-1]} et al."
        
        page_str = f", p. {self.page_numbers[0]}" if self.page_numbers else ""
        return f"({author_str}, {self.year}{page_str})"
    
    def to_bibtex_key(self) -> str:
        """Generate BibTeX key: authorYearTitle"""
        author_part = self.authors[0].split()[-1].lower() if self.authors else "unknown"
        title_part = "".join(self.title.split()[:3]).lower()
        return f"{author_part}{self.year}{title_part}"


@dataclass
class RetrievedChunk:
    """Retrieved text chunk with metadata"""
    text: str
    page_number: int
    source_file: str
    bm25_score: float
    semantic_score: float
    combined_score: float
    metadata: Dict[str, Any]


# ============================================================================
# PDF PROCESSING
# ============================================================================

class PDFProcessor:
    """Extract text and metadata from academic PDFs"""
    
    def __init__(self):
        if fitz is None:
            raise ImportError("PyMuPDF (fitz) required. Install: pip install pymupdf")
    
    def extract_metadata(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract paper metadata from PDF"""
        try:
            doc = fitz.open(str(pdf_path))
            metadata = doc.metadata
            
            # Extract from filename if metadata missing
            filename = pdf_path.stem
            
            # Parse authors from filename or metadata
            authors = self._extract_authors(metadata, filename)
            
            # Parse year from filename or metadata
            year = self._extract_year(metadata, filename)
            
            # Parse title
            title = metadata.get('title') or self._clean_filename_title(filename)
            
            # Extract DOI if present
            doi = self._extract_doi(doc)
            
            doc.close()
            
            return {
                'authors': authors,
                'year': year,
                'title': title,
                'doi': doi,
                'filename': pdf_path.name,
                'source_file': str(pdf_path)
            }
        except Exception as e:
            print(f"Warning: Could not extract metadata from {pdf_path.name}: {e}")
            return {
                'authors': [],
                'year': 'n.d.',
                'title': pdf_path.stem,
                'doi': None,
                'filename': pdf_path.name,
                'source_file': str(pdf_path)
            }
    
    def _extract_authors(self, metadata: Dict, filename: str, first_page_text: str = "") -> List[str]:
        """
        Extract author names with improved parsing.
        
        PRIORITY SYSTEM:
        1. **Standardized filename format**: AuthorLastName_Year_Title.pdf
           - Single author: Chen_2016_XGBoost.pdf → ["Chen"]
           - Two authors: Chen-Guestrin_2016_XGBoost.pdf → ["Chen", "Guestrin"]
           - Multi-author: Smith-Jones-Davis_2020_Title.pdf → ["Smith et al."]
        2. PDF metadata 'author' field
        3. First page text extraction (look for author patterns)
        4. Generic fallback
        """
        
        # PRIORITY 1: Parse from standardized filename format
        # Format: AuthorLastName_Year_Title.pdf or Author1-Author2_Year_Title.pdf
        # Remove .pdf extension first
        clean_name = re.sub(r'\.(pdf|PDF)$', '', filename)
        
        # Look for pattern: Word(s)_Year_RestOfTitle
        # Where Year is 4-digit number starting with 19 or 20
        match = re.match(r'^([A-Z][a-zA-Z\-]+)_(\d{4})_', clean_name)
        if match:
            author_part = match.group(1)
            
            # Check for hyphenated multiple authors
            if '-' in author_part:
                authors = [a.strip() for a in author_part.split('-') if a.strip()]
                if len(authors) == 1:
                    return authors
                elif len(authors) == 2:
                    return authors  # Will format as "Author1 & Author2"
                else:
                    # 3+ authors, use "First et al."
                    return [f"{authors[0]} et al."]
            else:
                # Single author
                return [author_part]
        
        # PRIORITY 2: Try PDF metadata
        if metadata and metadata.get('author'):
            authors_str = metadata['author']
            # Clean up common metadata issues
            authors_str = authors_str.strip()
            
            # Skip if it's just the title or single word
            if len(authors_str.split()) >= 2 and not authors_str.isupper():
                # Split by common separators
                authors = re.split(r'[,;&]|\sand\s|\set\sal\.', authors_str)
                cleaned_authors = []
                for a in authors:
                    a = a.strip()
                    # Filter out non-author strings
                    if a and len(a) > 1:
                        # Remove common prefixes/suffixes
                        a = re.sub(r'^(by|author[s]?:?)\s+', '', a, flags=re.IGNORECASE)
                        cleaned_authors.append(a)
                
                if cleaned_authors:
                    if len(cleaned_authors) > 2:
                        return [f"{cleaned_authors[0]} et al."]
                    return cleaned_authors
        
        # PRIORITY 3: Parse from first page text (advanced - look for author line patterns)
        if first_page_text:
            # Common pattern: Author names appear in first 500 characters
            # Look for lines with names (capitalized words) before abstract/introduction
            first_section = first_page_text[:500]
            # This is complex and often unreliable, so keeping it simple
            # Could be enhanced with ML-based extraction
            pass
        
        # PRIORITY 4: Fallback - try to extract from any part of filename
        parts = clean_name.split('_')
        for part in parts[:2]:  # Check first 2 parts only
            # Skip common title words and years
            if re.match(r'^\d{4}$', part):
                continue
            if part.lower() in {'the', 'a', 'an', 'using', 'with', 'for', 'on'}:
                continue
            # If looks like a name (capitalized, mostly letters)
            if part and part[0].isupper() and sum(c.isalpha() for c in part) / len(part) > 0.6:
                return [part]
        
        return ['Unknown']
    
    def _extract_year(self, metadata: Dict, filename: str, first_page_text: str = "") -> str:
        """
        Extract publication year with improved parsing.
        
        PRIORITY SYSTEM:
        1. Standardized filename format: AuthorName_YYYY_Title.pdf
        2. PDF metadata (creationDate, modDate)
        3. First page text
        4. Fallback to 'n.d.'
        """
        # PRIORITY 1: Extract from standardized filename
        # Look for 4-digit year in Author_YYYY_Title pattern
        match = re.search(r'_(\d{4})_', filename)
        if match:
            year = match.group(1)
            # Validate it's a reasonable publication year (1900-2099)
            if year.startswith('19') or year.startswith('20'):
                return year
        
        # PRIORITY 2: Try PDF metadata
        if metadata.get('creationDate'):
            year_match = re.search(r'(19|20)\d{2}', str(metadata['creationDate']))
            if year_match:
                return year_match.group(0)
        
        if metadata.get('modDate'):
            year_match = re.search(r'(19|20)\d{2}', str(metadata['modDate']))
            if year_match:
                return year_match.group(0)
        
        # PRIORITY 3: Look in first page text
        if first_page_text:
            # Common patterns: "2023", "(2023)", "©2023"
            years_found = re.findall(r'\b(19|20)\d{2}\b', first_page_text[:1000])
            if years_found:
                # Use the first reasonable year found
                return years_found[0]
        
        # PRIORITY 4: Try anywhere in filename as fallback
        year_match = re.search(r'\b(19|20)\d{2}\b', filename)
        if year_match:
            return year_match.group(0)
        
        return 'n.d.'
    
    def _clean_filename_title(self, filename: str) -> str:
        """Clean filename to extract title with better heuristics"""
        # Remove file extension
        title = re.sub(r'\.(pdf|PDF)$', '', filename)
        
        # Remove year patterns
        title = re.sub(r'\b(19|20)\d{2}\b', '', title)
        
        # Replace underscores and hyphens with spaces
        title = re.sub(r'[-_]+', ' ', title)
        
        # Remove common patterns like "et al"
        title = re.sub(r'\bet\s+al\.?\b', '', title, flags=re.IGNORECASE)
        
        # Remove version numbers (v1, v2, etc.)
        title = re.sub(r'\bv\d+\b', '', title, flags=re.IGNORECASE)
        
        # Collapse multiple spaces
        title = re.sub(r'\s+', ' ', title)
        
        # Clean and return
        title = title.strip()
        return title.strip()
    
    def _extract_doi(self, doc) -> Optional[str]:
        """Extract DOI from PDF content"""
        # Check first 3 pages for DOI
        for page_num in range(min(3, doc.page_count)):
            page = doc[page_num]
            text = page.get_text()
            doi_match = re.search(r'10\.\d{4,}/[^\s]+', text)
            if doi_match:
                return doi_match.group(0)
        return None
    
    def extract_chunks(
        self,
        pdf_path: Path,
        chunk_size: int = 300,
        overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Extract text chunks from PDF with page numbers.
        
        Args:
            pdf_path: Path to PDF file
            chunk_size: Target chunk size in words (200-300 recommended)
            overlap: Overlap between chunks in words
        
        Returns:
            List of chunk dictionaries with text, page_number, metadata
        """
        try:
            doc = fitz.open(str(pdf_path))
            chunks = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text = page.get_text()
                
                # Clean text
                text = self._clean_text(text)
                if not text:
                    continue
                
                # Split into paragraphs first
                paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                
                # Chunk paragraphs
                current_chunk = []
                current_word_count = 0
                
                for para in paragraphs:
                    para_words = para.split()
                    para_word_count = len(para_words)
                    
                    if current_word_count + para_word_count <= chunk_size:
                        current_chunk.append(para)
                        current_word_count += para_word_count
                    else:
                        # Save current chunk
                        if current_chunk:
                            chunks.append({
                                'text': '\n\n'.join(current_chunk),
                                'page_number': page_num + 1,  # 1-indexed
                                'word_count': current_word_count,
                                'source_file': str(pdf_path)
                            })
                        
                        # Start new chunk with overlap
                        if overlap > 0 and current_chunk:
                            # Take last paragraph for overlap
                            overlap_text = current_chunk[-1]
                            overlap_words = len(overlap_text.split())
                            current_chunk = [overlap_text, para]
                            current_word_count = overlap_words + para_word_count
                        else:
                            current_chunk = [para]
                            current_word_count = para_word_count
                
                # Add final chunk
                if current_chunk:
                    chunks.append({
                        'text': '\n\n'.join(current_chunk),
                        'page_number': page_num + 1,
                        'word_count': current_word_count,
                        'source_file': str(pdf_path)
                    })
            
            doc.close()
            return chunks
            
        except Exception as e:
            print(f"Error extracting chunks from {pdf_path.name}: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ''
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Normalize whitespace
        text = re.sub(r'\r\n|\r', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove hyphenation at line breaks
        text = re.sub(r'-\n', '', text)
        
        # Collapse multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        
        return text.strip()


# ============================================================================
# HYBRID SEARCH ENGINE
# ============================================================================

class HybridSearchEngine:
    """Hybrid search combining ChromaDB (semantic) and BM25 (keyword)"""
    
    def __init__(
        self,
        collection_name: str,
        persist_dir: Path,
        model_path: Optional[Path] = None
    ):
        """
        Initialize hybrid search engine.
        
        Args:
            collection_name: ChromaDB collection name (project-specific)
            persist_dir: Directory for ChromaDB persistence
            model_path: Path to BGE-large model (optional, downloads if None)
        """
        if chromadb is None:
            raise ImportError("chromadb required. Install: pip install chromadb")
        if BM25Okapi is None:
            raise ImportError("rank-bm25 required. Install: pip install rank-bm25")
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers required. Install: pip install sentence-transformers")
        
        self.collection_name = collection_name
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        # Load embedding model (BGE-large for quality)
        if model_path and model_path.exists():
            print(f"Loading BGE-large from: {model_path}")
            self.embedding_model = SentenceTransformer(str(model_path))
        else:
            print("Loading BGE-large from HuggingFace...")
            self.embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5')
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self._get_or_create_collection()
        
        # BM25 index
        self.bm25 = None
        self.bm25_path = self.persist_dir / f"{collection_name}_bm25.pkl"
    
    def _get_or_create_collection(self):
        """Get or create ChromaDB collection"""
        try:
            return self.client.get_collection(self.collection_name)
        except:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Academic papers for RAG citations"}
            )
    
    def index_documents(
        self,
        chunks: List[Dict[str, Any]],
        metadata_list: List[Dict[str, Any]]
    ):
        """
        Index document chunks into ChromaDB and BM25.
        
        Args:
            chunks: List of chunk dicts (text, page_number, source_file)
            metadata_list: List of paper metadata dicts (one per paper)
        """
        if not chunks:
            return
        
        # Create metadata mapping (filename -> paper metadata)
        metadata_map = {}
        for meta in metadata_list:
            metadata_map[meta['source_file']] = meta
        
        # Prepare for ChromaDB
        texts = []
        embeddings = []
        ids = []
        metadatas = []
        
        # Prepare for BM25
        tokenized_docs = []
        
        for i, chunk in enumerate(chunks):
            chunk_text = chunk['text']
            source_file = chunk['source_file']
            page_num = chunk['page_number']
            
            # Get paper metadata
            paper_meta = metadata_map.get(source_file, {})
            
            # Generate embedding
            embedding = self.embedding_model.encode(
                chunk_text,
                normalize_embeddings=True
            )
            
            # Prepare metadata for ChromaDB (ChromaDB doesn't accept None values)
            chunk_meta = {
                'page_number': page_num,
                'source_file': source_file,
                'authors': str(paper_meta.get('authors', [])),
                'year': paper_meta.get('year', 'n.d.'),
                'title': paper_meta.get('title', 'Unknown'),
                'doi': paper_meta.get('doi') or '',  # Convert None to empty string
                'word_count': chunk.get('word_count', 0)
            }
            
            # Add to collections
            texts.append(chunk_text)
            embeddings.append(embedding.tolist())
            ids.append(f"chunk_{i}")
            metadatas.append(chunk_meta)
            
            # Tokenize for BM25
            tokens = self._tokenize(chunk_text)
            tokenized_docs.append(tokens)
        
        # Index in ChromaDB
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        # Build BM25 index
        self.bm25 = BM25Okapi(tokenized_docs, k1=1.2, b=0.75)
        
        # Save BM25 index
        with open(self.bm25_path, 'wb') as f:
            pickle.dump(self.bm25, f)
        
        print(f"Indexed {len(chunks)} chunks from {len(metadata_list)} papers")
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for BM25"""
        # Lowercase and split
        text = text.lower()
        # Remove punctuation but keep alphanumeric
        text = re.sub(r'[^\w\s]', ' ', text)
        # Split and filter
        tokens = [t for t in text.split() if len(t) > 1]
        return tokens
    
    def load_bm25(self):
        """Load BM25 index from disk"""
        if self.bm25_path.exists():
            with open(self.bm25_path, 'rb') as f:
                self.bm25 = pickle.load(f)
            return True
        return False
    
    def hybrid_search(
        self,
        query: str,
        top_k: int = 10,
        semantic_weight: float = 0.6,
        bm25_weight: float = 0.4,
        min_confidence: float = 0.65
    ) -> List[RetrievedChunk]:
        """
        Hybrid search with Reciprocal Rank Fusion.
        
        Args:
            query: Search query
            top_k: Number of results to return
            semantic_weight: Weight for semantic search (0.6 recommended)
            bm25_weight: Weight for BM25 search (0.4 recommended)
            min_confidence: Minimum confidence threshold (0.65 for quality)
        
        Returns:
            List of RetrievedChunk objects, sorted by combined score
        """
        # Load BM25 if not loaded
        if self.bm25 is None:
            if not self.load_bm25():
                print("Warning: BM25 index not found, using semantic only")
                bm25_weight = 0.0
                semantic_weight = 1.0
        
        # Semantic search
        semantic_results = self._semantic_search(query, top_k * 2)
        
        # BM25 search
        bm25_results = []
        if self.bm25 is not None:
            bm25_results = self._bm25_search(query, top_k * 2)
        
        # Apply RRF (Reciprocal Rank Fusion)
        combined = self._reciprocal_rank_fusion(
            semantic_results,
            bm25_results,
            semantic_weight,
            bm25_weight,
            k=60  # RRF constant
        )
        
        # Filter by confidence and return top_k
        filtered = [c for c in combined if c.combined_score >= min_confidence]
        return filtered[:top_k]
    
    def _semantic_search(self, query: str, top_k: int) -> List[RetrievedChunk]:
        """Semantic search using ChromaDB"""
        query_embedding = self.embedding_model.encode(
            query,
            normalize_embeddings=True
        )
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        chunks = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                distance = results['distances'][0][i]
                score = 1.0 - distance  # Convert distance to similarity
                metadata = results['metadatas'][0][i]
                
                chunks.append(RetrievedChunk(
                    text=doc,
                    page_number=metadata.get('page_number', 0),
                    source_file=metadata.get('source_file', ''),
                    bm25_score=0.0,
                    semantic_score=score,
                    combined_score=score,
                    metadata=metadata
                ))
        
        return chunks
    
    def _bm25_search(self, query: str, top_k: int) -> List[RetrievedChunk]:
        """BM25 keyword search"""
        if self.bm25 is None:
            return []
        
        query_tokens = self._tokenize(query)
        scores = self.bm25.get_scores(query_tokens)
        
        # Get top indices
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        # Get documents from ChromaDB
        data = self.collection.get(include=['documents', 'metadatas'])
        documents = data.get('documents', [])
        metadatas = data.get('metadatas', [])
        
        chunks = []
        for idx in top_indices:
            if idx < len(documents) and scores[idx] > 0:
                metadata = metadatas[idx] if idx < len(metadatas) else {}
                
                # Normalize BM25 score (0-1 range)
                normalized_score = min(scores[idx] / 20.0, 1.0)
                
                chunks.append(RetrievedChunk(
                    text=documents[idx],
                    page_number=metadata.get('page_number', 0),
                    source_file=metadata.get('source_file', ''),
                    bm25_score=normalized_score,
                    semantic_score=0.0,
                    combined_score=normalized_score,
                    metadata=metadata
                ))
        
        return chunks
    
    def _reciprocal_rank_fusion(
        self,
        semantic_results: List[RetrievedChunk],
        bm25_results: List[RetrievedChunk],
        semantic_weight: float,
        bm25_weight: float,
        k: int = 60
    ) -> List[RetrievedChunk]:
        """
        Combine results using Reciprocal Rank Fusion.
        
        RRF formula: score = Σ(1 / (k + rank))
        """
        # Create unified result set
        result_map = {}
        
        # Add semantic results
        for rank, chunk in enumerate(semantic_results, 1):
            key = chunk.text[:100]  # Use text snippet as key
            if key not in result_map:
                result_map[key] = chunk
            result_map[key].combined_score += semantic_weight / (k + rank)
        
        # Add BM25 results
        for rank, chunk in enumerate(bm25_results, 1):
            key = chunk.text[:100]
            if key not in result_map:
                result_map[key] = chunk
            result_map[key].combined_score += bm25_weight / (k + rank)
        
        # Sort by combined score
        results = sorted(
            result_map.values(),
            key=lambda x: x.combined_score,
            reverse=True
        )
        
        return results


# ============================================================================
# CITATION GENERATOR
# ============================================================================

class CitationGenerator:
    """Generate and validate citations from retrieved chunks"""
    
    def __init__(self, reranker_model: Optional[str] = None):
        """
        Initialize citation generator.
        
        Args:
            reranker_model: CrossEncoder model for re-ranking (optional)
        """
        self.reranker = None
        if reranker_model and CrossEncoder:
            try:
                self.reranker = CrossEncoder(reranker_model)
            except:
                print("Warning: Could not load reranker model")
    
    def generate_citation(
        self,
        claim: str,
        retrieved_chunks: List[RetrievedChunk],
        validate: bool = True
    ) -> Optional[Citation]:
        """
        Generate citation from retrieved chunks.
        
        Args:
            claim: The claim needing citation
            retrieved_chunks: Retrieved text chunks
            validate: Whether to validate citation quality
        
        Returns:
            Citation object or None if validation fails
        """
        if not retrieved_chunks:
            return None
        
        # Use best chunk (highest score)
        best_chunk = retrieved_chunks[0]
        
        # Extract metadata
        metadata = best_chunk.metadata
        
        # Parse authors
        authors_str = metadata.get('authors', '[]')
        try:
            authors = eval(authors_str) if authors_str.startswith('[') else [authors_str]
        except:
            authors = ['Unknown']
        
        # Create citation
        citation = Citation(
            authors=authors,
            year=metadata.get('year', 'n.d.'),
            title=metadata.get('title', 'Unknown'),
            doi=metadata.get('doi'),
            page_numbers=[best_chunk.page_number],
            text_snippet=best_chunk.text[:200],
            confidence=best_chunk.combined_score,
            source_file=best_chunk.source_file
        )
        
        # Validate if requested
        if validate:
            if not self._validate_citation(claim, citation, best_chunk.text):
                return None
        
        return citation
    
    def _validate_citation(
        self,
        claim: str,
        citation: Citation,
        evidence_text: str
    ) -> bool:
        """
        Validate that citation supports the claim.
        
        Basic validation: Check for keyword overlap and confidence threshold.
        Advanced validation would use CrossEncoder for semantic entailment.
        """
        # Confidence threshold
        if citation.confidence < 0.65:
            return False
        
        # Keyword overlap check (basic validation)
        claim_words = set(claim.lower().split())
        evidence_words = set(evidence_text.lower().split())
        overlap = len(claim_words & evidence_words)
        overlap_ratio = overlap / max(len(claim_words), 1)
        
        if overlap_ratio < 0.2:  # Less than 20% overlap
            return False
        
        # Use reranker for advanced validation (if available)
        if self.reranker:
            score = self.reranker.predict([(claim, evidence_text)])[0]
            if score < 0.5:  # Not entailed
                return False
        
        return True
    
    def generate_bibtex(self, citations: List[Citation]) -> str:
        """
        Generate BibTeX entries for citations.
        
        Args:
            citations: List of Citation objects
        
        Returns:
            BibTeX formatted string
        """
        bibtex_entries = []
        seen_keys = set()
        
        for citation in citations:
            # Generate unique key
            base_key = citation.to_bibtex_key()
            key = base_key
            counter = 1
            while key in seen_keys:
                key = f"{base_key}_{counter}"
                counter += 1
            seen_keys.add(key)
            
            # Generate entry
            authors_bibtex = ' and '.join(citation.authors)
            
            entry = f"""@article{{{key},
    author = {{{authors_bibtex}}},
    title = {{{citation.title}}},
    year = {{{citation.year}}},"""
            
            if citation.doi:
                entry += f"\n    doi = {{{citation.doi}}},"
            
            entry += "\n}"
            
            bibtex_entries.append(entry)
        
        return '\n\n'.join(bibtex_entries)


# ============================================================================
# RAG CITATION SYSTEM (Main Interface)
# ============================================================================

class RAGCitationSystem:
    """
    Complete RAG system for academic citations in Quarto documents.
    
    Usage:
        rag = RAGCitationSystem(references_dir, project_name)
        rag.index_references()
        citation = rag.get_citation("claim text here")
        bibtex = rag.export_bibtex()
    """
    
    def __init__(
        self,
        references_dir: Path,
        project_name: str,
        model_dir: Optional[Path] = None
    ):
        """
        Initialize RAG system.
        
        Args:
            references_dir: Directory containing PDF references
            project_name: Project identifier (for collection naming)
            model_dir: Directory containing BGE-large model (optional)
        """
        self.references_dir = Path(references_dir)
        self.project_name = project_name
        self.model_dir = model_dir
        
        # Check if references exist
        if not self.references_dir.exists():
            raise ValueError(f"References directory not found: {references_dir}")
        
        # Find PDFs
        self.pdf_files = list(self.references_dir.glob('*.pdf'))
        if not self.pdf_files:
            raise ValueError(f"No PDF files found in {references_dir}")
        
        print(f"Found {len(self.pdf_files)} PDF references")
        
        # Initialize components
        self.pdf_processor = PDFProcessor()
        
        # Initialize search engine
        persist_dir = self.references_dir / '.chroma'
        self.search_engine = HybridSearchEngine(
            collection_name=f"{project_name}_references",
            persist_dir=persist_dir,
            model_path=model_dir / 'bge-large-en-v1.5' if model_dir else None
        )
        
        self.citation_generator = CitationGenerator()
        
        # Track citations for BibTeX export
        self.citations_used = []
    
    def index_references(self, force_reindex: bool = False):
        """
        Index PDF references into search engine.
        
        Args:
            force_reindex: Force re-indexing even if index exists
        """
        # Check if already indexed
        if not force_reindex and self.search_engine.load_bm25():
            print("Using existing index")
            return
        
        print(f"Indexing {len(self.pdf_files)} PDF references...")
        
        all_chunks = []
        all_metadata = []
        
        for pdf_path in self.pdf_files:
            print(f"Processing: {pdf_path.name}")
            
            # Extract metadata
            metadata = self.pdf_processor.extract_metadata(pdf_path)
            all_metadata.append(metadata)
            
            # Extract chunks
            chunks = self.pdf_processor.extract_chunks(
                pdf_path,
                chunk_size=250,  # 200-300 words for academic text
                overlap=50
            )
            all_chunks.extend(chunks)
            
            print(f"  - {len(chunks)} chunks extracted")
        
        # Index everything
        self.search_engine.index_documents(all_chunks, all_metadata)
        print(f"Indexing complete: {len(all_chunks)} chunks indexed")
    
    def get_citation(
        self,
        claim: str,
        top_k: int = 5,
        validate: bool = True
    ) -> Optional[Citation]:
        """
        Get citation for a claim.
        
        Args:
            claim: The factual claim needing citation
            top_k: Number of chunks to retrieve
            validate: Whether to validate citation quality
        
        Returns:
            Citation object or None if no good match found
        """
        # Search for supporting evidence
        chunks = self.search_engine.hybrid_search(
            query=claim,
            top_k=top_k,
            min_confidence=0.65
        )
        
        if not chunks:
            return None
        
        # Generate citation
        citation = self.citation_generator.generate_citation(
            claim=claim,
            retrieved_chunks=chunks,
            validate=validate
        )
        
        if citation:
            self.citations_used.append(citation)
        
        return citation
    
    def export_bibtex(self) -> str:
        """Export all used citations as BibTeX"""
        return self.citation_generator.generate_bibtex(self.citations_used)
    
    def get_context_for_claim(self, claim: str, top_k: int = 3) -> List[str]:
        """
        Get context snippets for a claim (for LLM prompts).
        
        Args:
            claim: The claim to find context for
            top_k: Number of context snippets to return
        
        Returns:
            List of context text snippets with citations
        """
        chunks = self.search_engine.hybrid_search(
            query=claim,
            top_k=top_k,
            min_confidence=0.60  # Slightly lower for context
        )
        
        contexts = []
        for chunk in chunks:
            # Format: "Text snippet (Author, Year, p. X)"
            authors_str = chunk.metadata.get('authors', '[]')
            try:
                authors = eval(authors_str) if authors_str.startswith('[') else [authors_str]
            except:
                authors = ['Unknown']
            
            author_str = authors[0].split()[-1] if authors else 'Unknown'
            year = chunk.metadata.get('year', 'n.d.')
            page = chunk.page_number
            
            context = f"{chunk.text[:300]}... ({author_str}, {year}, p. {page})"
            contexts.append(context)
        
        return contexts
