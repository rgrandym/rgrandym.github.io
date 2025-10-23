#!/usr/bin/env python3
"""
NEW WORKFLOW: Bulletproof Notebook to Quarto Conversion
=======================================================

This is the orchestrator that implements the improved cognitive-load-aware workflow:

Phase 1: EXTRACT → Analyze notebook, extract ground truth
Phase 2: STRUCTURE → Generate Methods + Objectives from notebook summary  
Phase 3: VISUALIZE → Add figures/tables with placeholders
Phase 4: ANALYZE → Write Results descriptions (from visible figures)
Phase 5: SYNTHESIZE → Discussion + Conclusion (from Results)
Phase 6: FRAME → Introduction (last, to match actual content)
Phase 7: VALIDATE → Check all claims against ground truth

Uses rag-transformers environment for RAG operations.
"""

import sys
import json
from pathlib import Path
from enum import Enum
from typing import Dict, List, Optional

# Setup paths
PATH_TO_PROJECT = Path(__file__).parent.parent
sys.path.insert(0, str(PATH_TO_PROJECT))

class Phase(Enum):
    """Phases in the new workflow"""
    EXTRACT = 1        # Extract ground truth from notebook
    STRUCTURE = 2      # Methods + Objectives
    VISUALIZE = 3      # Add figures/tables
    ANALYZE = 4        # Write Results
    SYNTHESIZE = 5     # Discussion + Conclusion
    FRAME = 6          # Introduction
    VALIDATE = 7       # Check accuracy
    
    @property
    def phase_name(self) -> str:
        """Get lowercase phase name"""
        return self.name.lower()


class ImprovedQuartoConverter:
    """
    New converter with improved workflow to prevent cognitive overload
    and ensure factual accuracy.
    """
    
    def __init__(
        self,
        notebook_path: Path,
        output_path: Path,
        selected_outputs: Dict[str, List],
        enable_rag: bool = True
    ):
        self.notebook_path = Path(notebook_path)
        self.output_path = Path(output_path)
        self.selected_outputs = selected_outputs
        self.enable_rag = enable_rag
        
        # Ground truth will be loaded here
        self.ground_truth = None
        self.ground_truth_path = None
        
        # RAG system
        self.rag_system = None
        
        print(f"\n{'='*80}")
        print(f"IMPROVED QUARTO CONVERTER")
        print(f"{'='*80}")
        print(f"Notebook: {self.notebook_path.name}")
        print(f"Output: {self.output_path.name}")
        print(f"RAG: {'Enabled' if enable_rag else 'Disabled'}")
        
    def run_phase_1_extract(self) -> Path:
        """
        Phase 1: Extract ground truth from notebook
        
        This creates a JSON file with:
        - Notebook summary
        - Methods used
        - All numerical results
        - Figure/table metadata
        """
        print(f"\n{'='*80}")
        print(f"PHASE 1: EXTRACT GROUND TRUTH")
        print(f"{'='*80}\n")
        
        from agent_quarto_reports.notebook_analyzer import NotebookAnalyzer
        
        analyzer = NotebookAnalyzer(self.notebook_path)
        self.ground_truth = analyzer.analyze()
        self.ground_truth_path = analyzer.save_ground_truth()
        
        print(f"\n✅ Ground truth extracted:")
        print(f"   - Numerical facts: {len(self.ground_truth['numerical_facts'])}")
        print(f"   - Tables: {len(self.ground_truth['tables'])}")
        print(f"   - Figures: {len(self.ground_truth['figures'])}")
        print(f"   - Methods: {len(self.ground_truth['methods'])}")
        
        return self.ground_truth_path
    
    def generate_phase_prompt(self, phase: Phase, context: Optional[Dict] = None) -> str:
        """Generate prompt for specific phase"""
        
        if phase == Phase.STRUCTURE:
            return self._prompt_structure(context)
        elif phase == Phase.VISUALIZE:
            return self._prompt_visualize(context)
        elif phase == Phase.ANALYZE:
            return self._prompt_analyze(context)
        elif phase == Phase.SYNTHESIZE:
            return self._prompt_synthesize(context)
        elif phase == Phase.FRAME:
            return self._prompt_frame(context)
        elif phase == Phase.VALIDATE:
            return self._prompt_validate(context)
        else:
            return f"# Phase {phase.value}: {phase.phase_name}\n\nNot implemented yet."
    
    def _prompt_structure(self, context: Dict) -> str:
        """Phase 2: Generate Methods + Objectives from notebook summary"""
        
        methods_info = json.dumps(self.ground_truth.get('methods', {}), indent=2)
        
        return f"""
# PHASE 2: STRUCTURE (Methods + Objectives)

## CRITICAL: Use Template YAML

Start the document with this EXACT YAML header (update title, description, date, categories, image):

```yaml
---
title: "Your Title Here"
description: "Brief description"
date: "YYYY-MM-DD"
categories: ["Category 1", "Category 2", "Category 3", "Category 4"]
image: "../assets/PROJECT_NAME/figures/main_image.png"
featured: true
jupyter: python3
page-layout: full
bibliography: ../assets/PROJECT_NAME/references/references.bib
format:
  html:
    include-in-header:
      text: |
        <style>
        figcaption.quarto-float-caption {{
          text-align: left !important;
        }}
        .quarto-figure-center {{
          text-align: left !important;
        }}
        .fig-label-left-edge {{
          text-align: left !important;
          margin-left: calc(-46vw + 50%);
          width: 100vw;
          position: relative;
          left: 0;
        }}
        /* Numbered references */
        #refs .csl-entry {{
          padding-left: 2em;
          text-indent: -2em;
          margin-bottom: 1em;
        }}
        #refs {{
          counter-reset: ref-counter;
        }}
        #refs .csl-entry::before {{
          counter-increment: ref-counter;
          content: counter(ref-counter) ". ";
          margin-right: 0.5em;
        }}
        </style>
---
```

## Context
You have the notebook ground truth showing what was ACTUALLY done.

## Your Task
Write TWO sections based ONLY on the notebook:

### 1. Methods Section (300 words)
Describe what was done in the analysis. Include:
- Data description
- Preprocessing steps  
- Model architectures used
- Training procedures
- Evaluation metrics

**Ground Truth Methods**:
```json
{methods_info}
```

### 2. Goals and Objectives (150 words)
List 3-5 objectives that the analysis aimed to achieve.
Base these on what the notebook actually investigated.

## Requirements
- ✅ Start with the YAML template above
- ✅ Only describe what's in the notebook
- ✅ Use past tense (this was done)
- ✅ Cite techniques with RAG [@author_year]
- ❌ NO results yet
- ❌ NO fabricated methods

**Output**: Complete .qmd file with YAML + Methods + Goals sections
"""
    
    def _prompt_visualize(self, context: Dict) -> str:
        """Phase 3: Add figures and tables with custom ordering"""
        
        tables = self.selected_outputs.get('tables', [])
        figures = self.selected_outputs.get('figures', [])
        order = self.selected_outputs.get('order', [])
        
        # Build ordered list showing what to add in sequence
        ordered_items = []
        
        if order:
            # Use custom order
            for item in order:
                if item.startswith('table-'):
                    table_num = int(item.split('-')[1])
                    table = next((t for t in tables if t.get('number') == table_num), None)
                    if table:
                        if isinstance(table, dict):
                            ordered_items.append({
                                'type': 'table',
                                'number': table['number'],
                                'file': table['file'],
                                'description': table['description'],
                                'caption': table['caption']
                            })
                elif item.startswith('figure-'):
                    fig_num = int(item.split('-')[1])
                    figure = next((f for f in figures if f.get('number') == fig_num), None)
                    if figure:
                        if isinstance(figure, dict):
                            ordered_items.append({
                                'type': 'figure',
                                'number': figure['number'],
                                'files': figure['files'],
                                'description': figure['description'],
                                'caption': figure['caption']
                            })
        else:
            # Default order: all tables first, then all figures
            for t in tables:
                if isinstance(t, dict):
                    ordered_items.append({
                        'type': 'table',
                        'number': t['number'],
                        'file': t['file'],
                        'description': t['description'],
                        'caption': t['caption']
                    })
            for f in figures:
                if isinstance(f, dict):
                    ordered_items.append({
                        'type': 'figure',
                        'number': f['number'],
                        'files': f['files'],
                        'description': f['description'],
                        'caption': f['caption']
                    })
        
        # Format the ordered list
        ordered_list = []
        for idx, item in enumerate(ordered_items, 1):
            if item['type'] == 'table':
                ordered_list.append(
                    f"{idx}. **Table {item['number']}**: {item['file']}\n"
                    f"   - {item['description']}\n"
                    f"   - Caption: {item['caption']}"
                )
            else:  # figure
                files_str = ', '.join(item['files'])
                ordered_list.append(
                    f"{idx}. **Figure {item['number']}**: {files_str}\n"
                    f"   - {item['description']}\n"
                    f"   - Caption: {item['caption']}"
                )
        
        return f"""
# PHASE 3: VISUALIZE (Add Figures/Tables)

## Your Task
Add {len(tables)} tables and {len(figures)} figures to the Results section IN THIS EXACT ORDER.

## CRITICAL: Follow This Exact Sequence

{chr(10).join(ordered_list)}

## Format Requirements

### For Tables
```python
#| label: tbl-{{table-number}}
#| tbl-cap: "[Use the EXACT caption from the list above]"
#| echo: false
#| tbl-cap-location: bottom

import pandas as pd
from IPython.display import display

df = pd.read_csv('../assets/student_dropout/figures/[filename]')
display(df)
```

### For Single-Image Figures
```html
<figure id="fig-{{figure-number}}">
  <img src="../assets/student_dropout/figures/[filename]" 
       style="width: 70%; max-width: 600px; margin: 0 auto; display: block;" 
       alt="[description]">
  <figcaption>Figure {{number}}: [Use the EXACT caption from the list above]</figcaption>
</figure>
```

### For Multi-Panel Figures (2 images side by side)
```html
<figure id="fig-{{figure-number}}">
  <div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap;">
    <img src="../assets/student_dropout/figures/[file1]" 
         style="width: 40%; min-width: 300px;" alt="[desc1]">
    <img src="../assets/student_dropout/figures/[file2]" 
         style="width: 40%; min-width: 300px;" alt="[desc2]">
  </div>
  <figcaption>Figure {{number}}: [Use the EXACT caption from the list above]</figcaption>
</figure>
```

## Requirements
- ✅ Follow the NUMBERED SEQUENCE above (1, 2, 3, ...)
- ✅ Use the EXACT table/figure numbers from the list
- ✅ Use the EXACT captions provided (copy-paste them)
- ✅ Create subsection headers: ### Table X or ### Figure X
- ✅ Use multi-panel format when a figure has 2+ files
- ❌ DO NOT reorder - follow the sequence exactly
- ❌ DO NOT write analysis yet (Phase 4 will add that)
- ❌ DO NOT change captions

**Output**: Complete Results section with all visualizations in the specified order
"""
    
    def _prompt_analyze(self, context: Dict) -> str:
        """Phase 4: Write Results analysis"""
        
        # Get one output at a time to avoid cognitive overload
        current_idx = context.get('current_result_index', 0)
        total = context.get('total_results', 0)
        output_info = context.get('current_output', {})
        
        # Include relevant numerical facts
        relevant_facts = self._get_relevant_facts(output_info)
        
        return f"""
# PHASE 4: ANALYZE (Results for Output {current_idx + 1}/{total})

## Your Task
Write analysis for ONE figure/table (200 words).

## Current Output
{json.dumps(output_info, indent=2)}

## Relevant Numerical Facts from Notebook
{json.dumps(relevant_facts, indent=2)}

## Structure
1. **What you see** (50 words): Describe the visual/table
2. **Key findings** (75 words): State the numbers (USE GROUND TRUTH)
3. **Interpretation** (50 words): What does this mean?
4. **Limitations** (25 words): What's missing/uncertain?

## Requirements
- ✅ Use ONLY numbers from ground truth above
- ✅ Describe what's visible in the figure/table
- ✅ Keep to 200 words
- ❌ NO fabricated numbers
- ❌ NO speculation beyond the data

**Output**: One complete result subsection
"""
    
    def _prompt_synthesize(self, context: Dict) -> str:
        """Phase 5: Discussion + Conclusion from results"""
        
        return f"""
    
# PHASE 5: SYNTHESIZE (Discussion + Conclusion)

## Your Task
Now that Results are written, synthesize the findings.

### 1. Discussion (300 words)
Answer these questions:
- How do results relate to the objectives?
- How do results compare to literature? (Use RAG citations)
- What are the implications?
- What are the limitations?

### 2. Conclusion (150 words)
Summarize:
- Key findings (from Results)
- Practical recommendations
- Future work directions

## Requirements
- ✅ Reference specific results from Results section
- ✅ Cite comparison papers with RAG [@author_year]
- ✅ Be honest about limitations
- ❌ NO new data/numbers
- ❌ NO claims not supported by Results

**Output**: Discussion + Conclusion sections
"""
    
    def _prompt_frame(self, context: Dict) -> str:
        """Phase 6: Introduction (LAST!)"""
        
        return f"""
# PHASE 6: FRAME (Introduction)

## Your Task
Write the Introduction NOW that you know what the document actually contains.

## Structure (300 words)
1. **Problem context** (75 words): Why does dropout prediction matter?
2. **Gap** (50 words): What's missing in current approaches?
3. **This work** (125 words): Summarize what THIS document shows
4. **Preview results** (50 words): Key finding (from actual Results)

## Requirements
- ✅ Align with actual Methods/Results/Discussion
- ✅ Cite background papers with RAG [@author_year]
- ✅ Preview REAL results (from Results section)
- ❌ NO promises the document doesn't keep
- ❌ NO claims not in the document

**Output**: Introduction section
"""
    
    def _prompt_validate(self, context: Dict) -> str:
        """Phase 7: Validation checklist"""
        
        return f"""
# PHASE 7: VALIDATE

## Your Task
Check the complete document for accuracy.

## Validation Checklist

### 1. Numerical Accuracy
- [ ] All numbers in document exist in ground truth
- [ ] No fabricated accuracy/precision/recall values
- [ ] No made-up performance comparisons

### 2. Claims Grounding
- [ ] Methods describe what notebook actually did
- [ ] Results analyze visible figures/tables
- [ ] Discussion interprets actual results

### 3. Citation Coverage
- [ ] All techniques cited
- [ ] All comparison claims cited
- [ ] Background statements cited

### 4. Internal Consistency
- [ ] Introduction matches actual results
- [ ] Objectives align with what was done
- [ ] Conclusion summarizes actual findings

**Output**: Validation report with issues found
"""
    
    def _get_relevant_facts(self, output_info: Dict) -> List[Dict]:
        """Extract numerical facts relevant to current output"""
        if not self.ground_truth:
            return []
        
        # Get all numerical facts
        all_facts = self.ground_truth.get('numerical_facts', [])
        
        # Filter relevant ones (simple heuristic for now)
        # TODO: Improve relevance matching
        return all_facts[:10]  # Return first 10 as example
    
    def save_phase_prompt(self, phase: Phase, output_file: Optional[Path] = None, context: Optional[Dict] = None) -> Path:
        """Save phase prompt to file"""
        
        if output_file is None:
            # Save in assets/<project_name>/
            notebook_path = Path(self.notebook_path)
            parts = notebook_path.parts
            
            if 'assets' in parts:
                assets_idx = parts.index('assets')
                if assets_idx + 1 < len(parts):
                    project_name = parts[assets_idx + 1]
                else:
                    project_name = self.output_path.stem
            else:
                project_name = self.output_path.stem
            
            project_dir = PATH_TO_PROJECT / 'assets' / project_name
            project_dir.mkdir(parents=True, exist_ok=True)
            output_file = project_dir / f"agent_prompt_phase_{phase.value}_{phase.phase_name}.md"
        
        prompt = self.generate_phase_prompt(phase, context)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"✓ Phase {phase.value} ({phase.phase_name.upper()}) prompt saved: {output_file}")
        print(f"  Length: {len(prompt)} characters (~{len(prompt) // 4} tokens)")
        
        return output_file


if __name__ == "__main__":
    # Test with student dropout project
    notebook = PATH_TO_PROJECT / 'assets/student_dropout/figures/student_dropout_nn_151025.ipynb'
    output = PATH_TO_PROJECT / 'projects/student-dropout-prediction_nn_201025.qmd'
    
    converter = ImprovedQuartoConverter(
        notebook_path=notebook,
        output_path=output,
        selected_outputs={
            'tables': ['comparison_neural_networks_all_stages.csv'],
            'figures': []
        },
        enable_rag=True
    )
    
    # Run Phase 1
    converter.run_phase_1_extract()
    
    # Generate prompts for phases 2-7
    print(f"\n{'='*80}")
    print("GENERATING PHASE PROMPTS")
    print(f"{'='*80}\n")
    
    converter.save_phase_prompt(Phase.STRUCTURE, context={})
    converter.save_phase_prompt(Phase.VISUALIZE, context={})
    converter.save_phase_prompt(Phase.ANALYZE, context={'current_result_index': 0, 'total_results': 1, 'current_output': {}})
    converter.save_phase_prompt(Phase.SYNTHESIZE, context={})
    converter.save_phase_prompt(Phase.FRAME, context={})
    converter.save_phase_prompt(Phase.VALIDATE, context={})
    
    print(f"\n✅ All phase prompts generated!")
