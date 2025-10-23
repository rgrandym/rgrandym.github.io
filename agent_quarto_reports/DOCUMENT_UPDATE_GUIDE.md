# Document Update Guide

This guide explains how to update existing Quarto documents created with the bulletproof workflow.

## Quick Reference

| What to Update | Where to Edit | Need to Regenerate? |
|----------------|---------------|---------------------|
| Add/remove citations | Edit .qmd file directly | No |
| Update text in any section | Edit .qmd file directly | No |
| Add new figure/table | Update config → Regenerate | Yes (Phase 3 & 4) |
| Change figure/table order | Update config ORDER → Regenerate | Yes (Phase 3) |
| Fix data/numbers | Check ground truth → Edit .qmd | No |
| Update Methods | Edit .qmd file directly | No |

---

## 1. Updating Specific Sections (Text Changes)

**When**: You want to improve writing, add details, fix errors in existing sections

**How**: Edit the `.qmd` file directly

### Example: Update Discussion Section

```bash
# Open the document
code projects/student-dropout-prediction_nn_201025.qmd

# Find the section (e.g., "## Discussion")
# Edit the text directly
# Save

# Render to see changes
quarto render projects/student-dropout-prediction_nn_201025.qmd
```

**No need to regenerate prompts** - just edit and render!

---

## 2. Adding/Removing Citations

**When**: You want to cite additional papers or remove citations

### Step 1: Ensure paper is in references

```bash
# Check if paper is in .bib file
cat assets/student_dropout/references/references.bib | grep -i "scikit-learn"
```

If not there, add it to `references.bib`:
```bibtex
@article{pedregosa2011scikit,
  title={Scikit-learn: Machine learning in Python},
  author={Pedregosa, Fabian and others},
  journal={Journal of Machine Learning Research},
  year={2011}
}
```

### Step 2: Add citation in text

```markdown
## Methods

Data preprocessing used StandardScaler from scikit-learn [@pedregosa2011scikit] 
to normalize features. Neural networks were implemented in PyTorch [@paszke2019pytorch].
```

### Step 3: Render to update references

```bash
quarto render projects/student-dropout-prediction_nn_201025.qmd
```

**That's it!** The References section auto-updates with numbered entries.

### Using RAG to Find Citations

If you want RAG to suggest papers automatically:

```bash
# Activate RAG environment
conda activate rag-transformers

# Check what papers RAG has indexed
python -c "
from agent_quarto_reports.rag_citation_system import RAGCitationSystem
rag = RAGCitationSystem(
    references_dir='assets/student_dropout/references',
    project_name='student_dropout'
)
results = rag.search_references('machine learning preprocessing')
for r in results[:5]:
    print(f'{r[\"title\"]}: {r[\"citation_key\"]}')
"
```

---

## 3. Adding New Figures or Tables

**When**: You created new visualizations and want to add them to the document

### Step 1: Add files to assets folder

```bash
# Put new figure in the figures folder
cp ~/my_new_plot.png assets/student_dropout/figures/
```

### Step 2: Update config file

Edit `assets/student_dropout/project_agent_config.py`:

```python
FIGURES = [
    {
        'number': 1,
        'files': ['existing_figure.png'],
        'caption': 'Existing figure...',
        'description': 'Shows X'
    },
    {
        'number': 2,  # ← New figure
        'files': ['my_new_plot.png'],
        'caption': 'New analysis showing feature importance',
        'description': 'Bar chart of top 10 features'
    },
    # ... rest of figures (renumber if needed)
]

# Update ORDER to include new figure
ORDER = [
    'table-1',
    'figure-1',
    'figure-2',  # ← Add here in desired position
    'figure-3',
    # ...
]
```

### Step 3: Regenerate Phase 3 and Phase 4 prompts

```bash
conda activate rag-transformers
python assets/student_dropout/project_agent_config.py
```

This creates:
- Updated `agent_prompt_phase_3_visualize.md` (with new figure in order)
- New `agent_prompt_phase_4_analyze_figure_2.md` (for analysis)

### Step 4: Add to document

Read the Phase 3 prompt to see the new sequence, then:

**Option A - Manual (faster for single addition)**:
```markdown
### Figure 2

<figure id="fig-2">
  <img src="../assets/student_dropout/figures/my_new_plot.png" 
       style="width: 70%; max-width: 600px; margin: 0 auto; display: block;" 
       alt="Feature importance">
  <figcaption>Figure 2: New analysis showing feature importance</figcaption>
</figure>

Feature importance analysis reveals... [Write analysis based on Phase 4 prompt]
```

**Option B - Use Phase 4 prompt**:
- Read `agent_prompt_phase_4_analyze_figure_2.md`
- Follow instructions to write 200-word analysis
- Add to Results section

### Step 5: Render

```bash
quarto render projects/student-dropout-prediction_nn_201025.qmd
```

---

## 4. Changing Figure/Table Order

**When**: You want figures/tables to appear in different sequence

### Update ORDER in config

```python
# Before: Table 2 after all figures
ORDER = [
    'table-1',
    'figure-1', 'figure-2', 'figure-3',
    'table-2',  # ← Want this earlier
    'figure-4', 'figure-5'
]

# After: Table 2 between figures 2 and 3
ORDER = [
    'table-1',
    'figure-1',
    'figure-2',
    'table-2',  # ← Moved up
    'figure-3',
    'figure-4',
    'figure-5'
]
```

### Regenerate Phase 3 prompt

```bash
conda activate rag-transformers
python assets/student_dropout/project_agent_config.py
```

### Manually reorder in document

1. Cut/paste the `### Table 2` section to new position
2. Follow the sequence from updated Phase 3 prompt
3. Render to verify

---

## 5. Removing Figures or Tables

### Step 1: Update config

```python
# Remove from FIGURES list
FIGURES = [
    {'number': 1, 'files': ['fig1.png'], ...},
    # DELETED: {'number': 2, 'files': ['fig2.png'], ...},
    {'number': 2, 'files': ['fig3.png'], ...},  # ← Renumber!
    {'number': 3, 'files': ['fig4.png'], ...},
]

# Update ORDER
ORDER = [
    'table-1',
    'figure-1',
    # 'figure-2',  ← Remove
    'figure-2',  # Was figure-3, now figure-2
    'figure-3',  # Was figure-4, now figure-3
]
```

### Step 2: Remove from document

Delete the corresponding section in the `.qmd` file:
```markdown
### Figure 2  ← Delete this entire section

<figure id="fig-2">
...
</figure>

Analysis text...  ← Delete through here
```

### Step 3: Renumber remaining figures

Update IDs and captions:
```markdown
<!-- Was Figure 3, now Figure 2 -->
### Figure 2

<figure id="fig-2">  <!-- Was fig-3 -->
  <img src="..." alt="...">
  <figcaption>Figure 2: ...</figcaption>  <!-- Was Figure 3 -->
</figure>
```

---

## 6. Adding More References to RAG Database

**When**: You have new papers you want RAG to suggest automatically

### Step 1: Add PDFs to references folder

```bash
cp ~/Downloads/new_paper.pdf assets/student_dropout/references/
```

### Step 2: Reindex RAG database

```bash
conda activate rag-transformers

python -c "
from agent_quarto_reports.rag_citation_system import RAGCitationSystem
from pathlib import Path

rag = RAGCitationSystem(
    references_dir=Path('assets/student_dropout/references'),
    project_name='student_dropout'
)

# Force reindex
rag.index_references(force_reindex=True)
print('✅ RAG database updated with new papers')
"
```

### Step 3: Add to .bib file

Manually add BibTeX entry to `references.bib`:
```bibtex
@article{newpaper2025,
  title={Title of New Paper},
  author={Author, First and Author, Second},
  journal={Journal Name},
  year={2025}
}
```

Now RAG can suggest this paper, and you can cite it with `[@newpaper2025]`

---

## 7. Fixing Numbers/Data Issues

**When**: You realize numbers in the document don't match the notebook

### Step 1: Check ground truth

```bash
# View extracted numbers from notebook
cat assets/student_dropout/figures/student_dropout_nn_151025_ground_truth.json | jq '.numerical_facts[0:10]'
```

### Step 2: Find the correct number

```bash
# Search for specific metric
cat assets/student_dropout/figures/student_dropout_nn_151025_ground_truth.json | jq '.numerical_facts[] | select(.metric == "f1")'
```

### Step 3: Update document

Edit `.qmd` file directly:
```markdown
<!-- BEFORE (wrong) -->
The model achieved 94% accuracy...

<!-- AFTER (correct - from ground truth) -->
The model achieved 97.2% F1-score and ROC-AUC of 0.985...
```

### Step 4: If numbers still don't match, regenerate ground truth

```bash
conda activate rag-transformers

python -c "
from agent_quarto_reports.notebook_analyzer import NotebookAnalyzer
from pathlib import Path

analyzer = NotebookAnalyzer(
    Path('assets/student_dropout/figures/student_dropout_nn_151025.ipynb')
)
analyzer.analyze()
analyzer.save_ground_truth()
print('✅ Ground truth regenerated')
"
```

---

## 8. Complete Document Regeneration

**When**: Major changes to notebook, or you want to start fresh

### Full workflow:

```bash
conda activate rag-transformers

# 1. Regenerate ground truth + all prompts
python assets/student_dropout/project_agent_config.py

# 2. Review all phase prompts
ls -1 assets/student_dropout/agent_prompt_phase_*.md

# 3. Follow prompts step-by-step to rewrite sections
# Phase 2: Methods + Objectives
# Phase 3: Add figures/tables
# Phase 4: Analyze each output (one at a time!)
# Phase 5: Discussion + Conclusion
# Phase 6: Introduction
# Phase 7: Validate

# 4. Render final document
quarto render projects/student-dropout-prediction_nn_201025.qmd
```

---

## 9. Quick Fixes

### Fix broken image paths
```bash
# Find all image references
grep -n "src=\"" projects/student-dropout-prediction_nn_201025.qmd

# Common issue: wrong relative path
# Wrong: src="assets/student_dropout/figures/fig.png"
# Right: src="../assets/student_dropout/figures/fig.png"
```

### Verify all citations exist
```bash
# Find all citations in text
grep -o '@[a-z0-9]*' projects/student-dropout-prediction_nn_201025.qmd | sort -u

# Check if they're all in .bib file
cat assets/student_dropout/references/references.bib | grep "@"
```

### Check if references are numbered
```bash
# View CSS for numbered references
grep -A 10 "Numbered references" projects/student-dropout-prediction_nn_201025.qmd

# Should see:
# content: counter(ref-counter) ". ";
```

---

## 10. Common Workflows

### Add analysis for existing figure
1. Open `.qmd` file
2. Find the figure section
3. Add paragraph below figcaption
4. Render

### Change figure caption
1. Update in config `FIGURES` list
2. Update in `.qmd` file `<figcaption>` tag
3. Render

### Add citation to existing text
1. Ensure paper in `.bib` file
2. Add `[@citation_key]` in text
3. Render

### Reorder sections
1. Cut/paste in `.qmd` file
2. Update any cross-references (e.g., "as shown in Figure 3")
3. Render

---

## Summary

| Change Type | Edit Config? | Regenerate Prompts? | Edit .qmd? | Render? |
|-------------|--------------|---------------------|------------|---------|
| Text/writing | No | No | ✅ | ✅ |
| Add citation | No | No | ✅ | ✅ |
| Add figure/table | ✅ | ✅ | ✅ | ✅ |
| Change order | ✅ | ✅ (Phase 3) | ✅ | ✅ |
| Remove output | ✅ | ✅ | ✅ | ✅ |
| Fix numbers | No | No | ✅ | ✅ |
| New PDF in RAG | No | Reindex RAG | No | No |

**Remember**: The `.qmd` file is your final document. Config + prompts are helpers for major changes. Most edits can be done directly in the `.qmd` file!
