#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reference Verification Tool

Quick script to verify if a specific claim is supported by a reference
using the RAG citation system.

Usage:
    python verify_reference.py "your claim here" "citation_key"
    
Example:
    python verify_reference.py "neural networks are stochastic" "paszke2019pytorch"
"""

import sys
from pathlib import Path
from rag_citation_system import RAGCitationSystem

def verify_claim(claim: str, citation_key: str, project_path: str = None):
    """
    Verify if a claim is supported by content in the referenced paper.
    
    Args:
        claim: The claim to verify
        citation_key: BibTeX key (e.g., "paszke2019pytorch")
        project_path: Path to project directory (defaults to ../assets/student_dropout)
    """
    if project_path is None:
        # Default to student_dropout project
        project_path = Path(__file__).parent.parent / "assets" / "student_dropout"
    else:
        project_path = Path(project_path)
    
    print(f"\n{'='*80}")
    print(f"VERIFYING CLAIM")
    print(f"{'='*80}")
    print(f"Claim: {claim}")
    print(f"Citation: @{citation_key}")
    print(f"Project: {project_path}")
    print(f"{'='*80}\n")
    
    try:
        # Initialize RAG system
        print("Initializing RAG Citation System...")
        references_dir = Path(project_path) / "references"
        rag = RAGCitationSystem(
            references_dir=references_dir,
            project_name="student_dropout"
        )
        
        # Search for relevant content
        print(f"\nSearching for content related to: '{claim}'")
        results = rag.search_and_cite(
            query=claim,
            n_results=5,
            min_relevance=0.3
        )
        
        if not results:
            print("\n❌ NO RELEVANT CONTENT FOUND")
            print(f"The claim '{claim}' does not appear to be supported by @{citation_key}")
            print("Recommendation: Remove this citation or use a different reference.")
            return False
        
        print(f"\n✅ FOUND {len(results)} RELEVANT PASSAGES\n")
        
        # Filter results for the specific citation
        relevant_to_citation = [r for r in results if citation_key in r.get('metadata', {}).get('source', '')]
        
        if not relevant_to_citation:
            print(f"\n⚠️  WARNING: No content found specifically from @{citation_key}")
            print(f"The claim may be supported by OTHER papers, but not this one:")
            for i, result in enumerate(results[:3], 1):
                source = result.get('metadata', {}).get('source', 'Unknown')
                page = result.get('metadata', {}).get('page', 'N/A')
                score = result.get('relevance_score', 0)
                content = result.get('content', '')[:150]
                print(f"\n{i}. Source: {source} (Page {page}, Relevance: {score:.3f})")
                print(f"   Content: {content}...")
            print(f"\nRecommendation: Change citation from @{citation_key} to one of the sources above.")
            return False
        
        print(f"✅ CLAIM IS SUPPORTED BY @{citation_key}\n")
        print(f"Found {len(relevant_to_citation)} relevant passage(s):\n")
        
        for i, result in enumerate(relevant_to_citation, 1):
            page = result.get('metadata', {}).get('page', 'N/A')
            score = result.get('relevance_score', 0)
            content = result.get('content', '')
            
            print(f"{'-'*80}")
            print(f"Passage {i} (Page {page}, Relevance Score: {score:.3f})")
            print(f"{'-'*80}")
            print(content)
            print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python verify_reference.py 'claim' 'citation_key' [project_path]")
        print("\nExample:")
        print("  python verify_reference.py 'neural networks are stochastic' 'paszke2019pytorch'")
        print("\nOr run interactively:")
        
        claim = input("\nEnter claim to verify: ").strip()
        citation_key = input("Enter citation key (e.g., paszke2019pytorch): ").strip()
        
        if claim and citation_key:
            project_path = input("Project path (press Enter for default ../assets/student_dropout): ").strip()
            verify_claim(claim, citation_key, project_path if project_path else None)
    else:
        claim = sys.argv[1]
        citation_key = sys.argv[2]
        project_path = sys.argv[3] if len(sys.argv) > 3 else None
        verify_claim(claim, citation_key, project_path)
