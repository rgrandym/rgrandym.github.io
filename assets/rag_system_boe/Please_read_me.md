# Environment Setup Instructions

### DO NOT UPDATE Packages: As it is work fine, but I remember some version of numpy, and matplotlib conflicting with some transformers libraries.

## Complete Guide to Replicate the `rag-transformers` Conda Environment

### Prerequisites

- Anaconda or Miniconda installed
- ~15-20 GB free disk space
- macOS, Linux, or Windows (with conda)

---

## Quick Setup (Recommended)

### Step 1: Create Environment from YAML

```bash
# Navigate to project directory
cd /path/to/your_notebook
# Create the conda environment
conda env create -f environment.yml

# Activate the environment
conda activate rag-transformers
```

### Step 2: Download spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### Step 3: Install Ollama (for Local LLM)

**macOS:**

```bash
# Download and install from: https://ollama.ai/
# Or use Homebrew:
brew install ollama

# Pull the Llama 3.1 model
ollama pull llama3.1:8b
```

**Linux:**

```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama3.1:8b
```

**Windows:**
Download installer from: https://ollama.ai/download/windows

### Step 4: Verify Installation

```bash
python -c "
import chromadb
import sentence_transformers
import transformers
import spacy
import langchain
print('✅ All core packages imported successfully!')
"
```

---

## Environment Details

### Python Version

- **Python 3.11.13** (CPython)

### Key Dependencies

| Category                      | Packages                                                |
| ----------------------------- | ------------------------------------------------------- |
| **Embeddings**          | sentence-transformers (5.1.0), BAAI/bge-large-en-v1.5   |
| **LLM**                 | transformers (4.56.1), torch (2.8.0), llama-cpp-python  |
| **Vector DB**           | chromadb (1.0.21), weaviate-client (4.16.9)             |
| **Search**              | rank-bm25 (0.2.2), onnxruntime                          |
| **LangChain**           | langchain (0.3.27), langchain-core, langchain-community |
| **Document Processing** | pymupdf (1.26.4), python-docx (1.2.0)                   |
| **Topic Modeling**      | bertopic (0.17.3), hdbscan, umap-learn                  |
| **NLP**                 | spacy (3.8.7), nltk (3.9.1), ftfy                       |
| **Evaluation**          | ragas (0.3.4)                                           |
| **API**                 | fastapi (0.116.1), uvicorn (0.35.0)                     |

### Platform-Specific Notes

**macOS (ARM/Apple Silicon):**

- Environment optimized for `osx-arm64` architecture
- PyTorch with ARM-optimized builds
- Some packages may compile from source

**Linux (x86_64/AMD64):**

- Use the same `environment.yml`
- May need to install build essentials: `apt-get install build-essential`

**Windows:**

- Some packages may require Visual C++ Build Tools
- Use Anaconda Prompt or PowerShell with conda initialized

---

## Storage Requirements

| Component                         | Size                         |
| --------------------------------- | ---------------------------- |
| Base conda environment            | 3-5 GB                       |
| BAAI/bge-large-en-v1.5 embeddings | ~1.3 GB                      |
| FinBERT sentiment model           | ~440 MB                      |
| Llama 3.1 8B                      | ~4.7 GB                      |
| spaCy en_core_web_sm              | ~12 MB                       |
| ChromaDB vector storage           | Variable (depends on corpus) |
| **Total recommended**       | **15-20 GB**           |

---

---
