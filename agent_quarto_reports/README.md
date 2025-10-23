# Agent-Guided Notebook to Quarto Converter

**Production-ready tools for converting Jupyter notebooks to Quarto documents with AI assistance and RAG-powered citations.**

## 📁 Clean Structure

This directory contains only essential files for the notebook-to-quarto workflow.

## 📁 Structure

```
agent_quarto_reports/
├── notebook_to_quarto_agent.py    # Create NEW Quarto documents
├── quarto_updater.py              # UPDATE existing documents  
├── template_yaml.qmd              # YAML template reference
└── README.md                      # This file
```

## 🎯 Two Main Workflows

### 1. CREATE New Document (`notebook_to_quarto_agent.py`)

**Use when**: Starting a completely new Quarto document from a notebook

```python
from agent_quarto_reports.notebook_to_quarto_agent import AgentGuidedConverter

converter = AgentGuidedConverter(
    notebook_path='assets/analysis.ipynb',
    output_path='projects/new_analysis.qmd',
    yaml_template_file='projects/reference_project.qmd',
    selected_outputs={
        'tables': ['data/results.csv'],
        'figures': ['figures/plot1.png', 'figures/plot2.png']
    }
)

# Generate comprehensive prompt for agent
converter.save_prompt('agent_prompt_create.md')
```

**Agent generates**:
- ✅ Compelling 500-word introduction
- ✅ Goals section based on ALL notebook analyses
- ✅ Comprehensive 500-word methodology
- ✅ Detailed 500-word analysis per figure/table
- ✅ Discussion and conclusion sections
- ✅ Proper YAML matching template
- ✅ Professional academic style with references

---

### 2. UPDATE Existing Document (`quarto_updater.py`)

**Use when**: Adding new content to an existing Quarto document

```python
from agent_quarto_reports.quarto_updater import QuartoDocumentUpdater

# APPEND MODE: Add new content at end of section
updater = QuartoDocumentUpdater(
    existing_quarto_path='projects/existing_analysis.qmd',
    notebook_path='assets/additional_analysis.ipynb',  # Optional
    selected_outputs={
        'figures': ['figures/new_plot1.png', 'figures/new_plot2.png'],
        'tables': ['data/new_results.csv']
    },
    update_mode='append',  # or 'replace', 'merge'
    target_section='Results'  # Which section to update
)

updater.save_update_prompt('agent_prompt_update.md')
```

**Three Update Modes**:

1. **`append`**: Add new content at end of section
   - Maintains existing content
   - Adds new figures/tables with analysis
   - Sequential numbering continues

2. **`replace`**: Replace entire section with new content
   - Preserves connections to other sections
   - Complete rewrite of target section
   - Updates cross-references

3. **`merge`**: Intelligently integrate new with existing
   - Finds optimal integration points
   - Avoids redundancy
   - Smooth narrative transitions
   - Renumbers figures/tables

---

## 📝 Complete Example Workflows

### Example 1: Create Neural Network Analysis Document

```python
from agent_quarto_reports.notebook_to_quarto_agent import AgentGuidedConverter

converter = AgentGuidedConverter(
    notebook_path='assets/student_dropout/figures/nn_analysis.ipynb',
    output_path='projects/student-dropout-nn.qmd',
    yaml_template_file='projects/student-dropout-xgb.qmd',
    selected_outputs={
        'tables': ['../assets/student_dropout/figures/nn_comparison.csv'],
        'figures': [
            '../assets/student_dropout/figures/roc_curve.png',
            '../assets/student_dropout/figures/confusion_matrix.png'
        ]
    }
)

converter.save_prompt('agent_prompt_nn_create.md')

# Next: Give prompt to AI agent
# Agent reads notebook, analyzes deeply, generates professional document
```

---

### Example 2: Add New Figures to Existing Results

```python
from agent_quarto_reports.quarto_updater import QuartoDocumentUpdater

updater = QuartoDocumentUpdater(
    existing_quarto_path='projects/student-dropout-nn.qmd',
    notebook_path='assets/student_dropout/figures/nn_analysis.ipynb',
    selected_outputs={
        'figures': [
            '../assets/student_dropout/figures/learning_curves.png',
            '../assets/student_dropout/figures/feature_importance.png'
        ]
    },
    update_mode='append',
    target_section='Results'
)

updater.save_update_prompt('agent_prompt_add_figures.md')

# Agent will:
# 1. Read existing Results section
# 2. Match formatting style
# 3. Continue figure numbering (e.g., fig-3, fig-4 if last was fig-2)
# 4. Write 500-word analysis for each new figure
# 5. Connect to existing narrative
```

---

### Example 3: Merge Analysis from Multiple Notebooks

```python
from agent_quarto_reports.quarto_updater import QuartoDocumentUpdater

updater = QuartoDocumentUpdater(
    existing_quarto_path='projects/dropout-analysis.qmd',
    notebook_path='assets/nn_deep_dive.ipynb',  # Primary new notebook
    additional_notebooks=[
        'assets/feature_analysis.ipynb',
        'assets/hyperparameter_tuning.ipynb'
    ],
    selected_outputs={
        'figures': ['../assets/comprehensive_comparison.png'],
        'tables': ['../assets/final_metrics.csv']
    },
    update_mode='merge',
    target_section='Results'
)

updater.save_update_prompt('agent_prompt_merge.md')

# Agent will:
# 1. Analyze all 3 notebooks for complementary insights
# 2. Find optimal integration points in existing Results
# 3. Avoid redundancy with existing content
# 4. Create seamless narrative flow
# 5. Renumber all figures/tables sequentially
```

---

### Example 4: Replace Discussion with Updated Insights

```python
from agent_quarto_reports.quarto_updater import QuartoDocumentUpdater

updater = QuartoDocumentUpdater(
    existing_quarto_path='projects/dropout-analysis.qmd',
    notebook_path='assets/revised_analysis.ipynb',
    update_mode='replace',
    target_section='Discussion'
)

updater.save_update_prompt('agent_prompt_replace_discussion.md')

# Agent will:
# 1. Preserve Discussion header
# 2. Rewrite entire section with new insights
# 3. Maintain connections to Introduction and Results
# 4. Update any cross-references elsewhere
# 5. Keep same academic tone and depth
```

---

## 🔧 Configuration Options

### AgentGuidedConverter (Create)

```python
AgentGuidedConverter(
    notebook_path: str,              # Required: Source notebook
    output_path: str,                # Required: Output .qmd file
    yaml_template_file: str,         # Optional: Template for YAML format
    selected_outputs: Dict,          # Optional: Specific outputs to include
    constitution_path: str           # Optional: Project rules file
)
```

**`selected_outputs` format**:
```python
{
    'figures': [
        'path/to/figure1.png',
        'path/to/figure2.png'
    ],
    'tables': [
        'path/to/table1.csv',
        'path/to/table2.csv'
    ]
}
```

---

### QuartoDocumentUpdater (Update)

```python
QuartoDocumentUpdater(
    existing_quarto_path: str,       # Required: Existing .qmd to update
    notebook_path: str,              # Optional: Primary new notebook
    additional_notebooks: List[str], # Optional: Additional notebooks
    selected_outputs: Dict,          # Optional: New files to add
    update_mode: str,                # Required: 'append'/'replace'/'merge'
    target_section: str,             # Optional: Section to update
    constitution_path: str           # Optional: Project rules file
)
```

**Update modes**:
- `'append'`: Add at end (safest, maintains existing)
- `'replace'`: Complete rewrite (use for major revisions)
- `'merge'`: Intelligent integration (best for complementary content)

---

## 💡 Best Practices

### When to CREATE vs UPDATE

**CREATE new document** when:
- ✅ Starting fresh analysis
- ✅ Converting notebook to website format for first time
- ✅ Need complete structure (intro, methods, results, discussion)

**UPDATE existing document** when:
- ✅ Adding new figures to Results
- ✅ Incorporating additional experiments
- ✅ Merging insights from multiple notebooks
- ✅ Revising specific sections with new findings
- ✅ Appending follow-up analyses

### Choosing Update Mode

| Mode | Use When | Preserves Existing? | Best For |
|------|----------|---------------------|----------|
| **append** | Adding new content | ✅ Yes | New figures/tables, additional experiments |
| **replace** | Major revision needed | ❌ No | Complete section rewrite, updated methodology |
| **merge** | Complementary insights | ⚠️ Partially | Integrating related analyses, avoiding redundancy |

### Output Selection Tips

1. **Be specific**: Point to exact files rather than letting agent guess
2. **Curate carefully**: Only include outputs that advance the narrative
3. **Sequential additions**: When updating, add figures/tables in logical order
4. **Preview first**: Check CSV/figure contents before including

### Working with the Agent

1. **Review prompts**: Always check generated prompts before sending to agent
2. **Provide context**: If analysis is complex, add notes to `selected_outputs`
3. **Iterate**: Start with core content, then add figures incrementally
4. **Quality check**: Review agent output for:
   - Correct figure/table numbering
   - Consistent style with existing content
   - Accurate technical claims
   - Proper references

---

## 📚 Agent Prompt Contents

### CREATE Prompt Includes:
- Complete notebook summary (cells, imports, sections)
- YAML template format and CSS classes
- External files preview (CSV data, figure paths)
- Detailed instructions for:
  - 500-word introduction
  - Goals section
  - 500-word methods
  - 500-word figure/table analyses
  - Discussion and conclusion
- Constitution rules
- Quality checklist

### UPDATE Prompt Includes:
- Existing document structure and sections
- Current content (for context and style matching)
- New notebook analyses to integrate
- External files to add
- Specific update mode instructions
- Figure/table numbering guidelines
- Style consistency requirements
- Integration strategy

---

## 🎓 Advanced Usage

### Custom YAML Templates

Create a reference `.qmd` file with desired YAML structure:

```yaml
---
title: "Template Title"
date: "2025-01-01"
categories: ["Category 1", "Category 2"]
format:
  html:
    include-in-header:
      text: |
        <style>
        /* Custom CSS here */
        </style>
---
```

Then point to it:
```python
yaml_template_file='path/to/your/template.qmd'
```

### Multiple Sequential Updates

```python
# Update 1: Add baseline results
updater1 = QuartoDocumentUpdater(
    existing_quarto_path='projects/analysis.qmd',
    selected_outputs={'figures': ['baseline_results.png']},
    update_mode='append',
    target_section='Results'
)
updater1.save_update_prompt('update1.md')

# ... agent generates update ...

# Update 2: Add tuned model results  
updater2 = QuartoDocumentUpdater(
    existing_quarto_path='projects/analysis.qmd',  # Updated version
    selected_outputs={'figures': ['tuned_results.png']},
    update_mode='append',
    target_section='Results'
)
updater2.save_update_prompt('update2.md')
```

### Integration with Git Workflow

```bash
# Create feature branch for new analysis
git checkout -b feature/nn-analysis

# Generate Quarto document
python agent_quarto_reports/notebook_to_quarto_agent.py

# Review agent output
git diff projects/new_analysis.qmd

# Commit if satisfied
git add projects/new_analysis.qmd
git commit -m "Add neural network analysis document"

# Later: add new figures
python agent_quarto_reports/quarto_updater.py

# Review changes
git diff projects/new_analysis.qmd

# Commit incremental update
git add projects/new_analysis.qmd
git commit -m "Add confusion matrix and ROC curve analysis"
```

---

## 🐛 Troubleshooting

### "Template file not found"
- Check path is relative to project root
- Verify file exists: `ls -la path/to/template.qmd`

### "Cannot parse existing sections"
- Ensure document has proper `## Section` headers
- Check YAML front matter is properly delimited with `---`

### "Figure numbering inconsistent"
- Review existing document for current figure labels
- Agent should auto-detect, but you can specify in update mode

### "Style doesn't match existing"
- Provide more context in target_section
- Use `merge` mode for better style matching
- Check CSS classes are applied correctly

---

## 📖 Related Documentation

- `NOTEBOOK_TO_QUARTO_GUIDE.md` - Original conversion guide
- `.specify/memory/constitution.md` - Project rules and standards
- `styles/styles.css` - CSS classes for figures/tables
- `_quarto.yml` - Website configuration

---

## 🔄 Workflow Diagram

```
┌─────────────────┐
│  Jupyter        │
│  Notebook       │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│  CREATE         │  │  UPDATE         │
│  New Document   │  │  Existing Doc   │
└────────┬────────┘  └────────┬────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  Agent Prompt   │  │  Update Prompt  │
│  Generated      │  │  Generated      │
└────────┬────────┘  └────────┬────────┘
         │                    │
         ▼                    ▼
┌─────────────────────────────────────┐
│          AI Agent Analysis          │
│  - Deep notebook understanding      │
│  - 500-word section generation      │
│  - Style matching                   │
│  - Figure/table integration         │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Professional   │
│  Quarto Doc     │
│  Ready for      │
│  Website        │
└─────────────────┘
```

---

## 💪 Future Enhancements

Potential additions to the system:

- [ ] Batch processing multiple notebooks
- [ ] Auto-detection of optimal update mode
- [ ] Template library for different project types
- [ ] Validation of generated content against original notebook
- [ ] Direct API integration (OpenAI, Anthropic) for full automation
- [ ] Version control integration for tracking changes
- [ ] Preview generation before committing updates

---

**Last Updated**: 2025-10-19  
**Version**: 2.0.0
