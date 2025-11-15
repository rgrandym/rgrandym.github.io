#!/usr/bin/env python3
"""
PROJECT AGENT CONFIGURATION - NEW BULLETPROOF WORKFLOW
=======================================================

This configuration uses the improved workflow that prevents fabrication 
and cognitive overload.

WORKFLOW PHASES:
1. EXTRACT (auto)    - Extract ground truth from notebook
2. STRUCTURE         - Write Methods + Objectives
3. VISUALIZE         - Add all figures/tables
4. ANALYZE (×N)      - Write Results (one output at a time)
5. SYNTHESIZE        - Write Discussion + Conclusion
6. FRAME             - Write Introduction (LAST!)
7. VALIDATE (auto)   - Check against ground truth

CONFIGURATION INSTRUCTIONS:
---------------------------

1. Define TABLES and FIGURES below with:
   - 'number': The display number (Table 1, Figure 1, etc.)
   - 'file' or 'files': Actual filename(s)
   - 'description': What it shows (for you)
   - 'caption': Exact caption to use in document

2. Define ORDER - List items in the exact order they should appear:
   - Use 'table-1', 'table-2' for tables
   - Use 'figure-1', 'figure-2', etc. for figures
   - Example: ['table-1', 'figure-1', 'figure-2', 'table-2', 'figure-3']
   
   This allows flexible ordering like:
   - Table 1 before Figure 1
   - Figures 1-4 grouped together
   - Table 2 in the middle of figures
   - Any custom arrangement you want

3. The agent will follow ORDER exactly when writing the Results section.

USAGE:
    conda activate rag-transformers
    python assets/student_dropout/project_agent_config.py

This generates phase prompts in: assets/student_dropout/agent_prompt_phase_*.md
"""

import sys
from pathlib import Path

# ============================================================================
# PROJECT CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path('/Users/rodrigograndy/Desktop/coding_projects/my_website')
PROJECT_NAME = 'student_dropout'

# Input/Output
NOTEBOOK = PROJECT_ROOT / 'assets/student_dropout/figures/student_dropout_nn_151025.ipynb'
OUTPUT_QMD = PROJECT_ROOT / 'projects/student-dropout-prediction_nn_201025.qmd'

# RAG Settings
ENABLE_RAG = True

# Selected Outputs (with explicit ordering and descriptions)
TABLES = [
    {
        'number': 1,
        'file': 'comparison_neural_networks_all_stages.csv',
        'caption': 'Performance comparison of neural network architectures across three data stages',
        'description': 'Compares Base vs Tuned models across Stage 1, 2, and 3 data'
    },
    {
        'number': 2,
        'file': 'nn_models_evaluation.csv',
        'caption': 'Detailed evaluation metrics for neural network models',
        'description': 'Shows precision, recall, F1-score, and AUC-ROC for all configurations'
    }
]

FIGURES = [
    {
        'number': 1,
        'files': ['val_accuracy_curve_s3_nn.png', 'learning_curve_nn_s3.png'],
        'caption': 'Neural network training dynamics showing validation accuracy progression and loss convergence',
        'description': 'Left: validation accuracy curves. Right: training/validation loss'
    },
    {
        'number': 2,
        'files': ['cm_all_models_nn_red_square.png'],
        'caption': 'Confusion matrices across all neural network configurations',
        'description': 'Shows classification patterns and error distributions'
    },
    {
        'number': 3,
        'files': ['comparison_cm_best_nn_s3.png'],
        'caption': 'Detailed confusion matrix comparison for best performing architecture',
        'description': 'Compares best model performance across metrics'
    },
    {
        'number': 4,
        'files': ['tuned_nn_models_best_highlighted.png'],
        'caption': 'Performance comparison of hyperparameter-tuned models',
        'description': 'Shows effect of different hyperparameter combinations'
    },
    {
        'number': 5,
        'files': ['learning_curve_final_model.png', 'accuracy_curve_final_nn_s3_model.png'],
        'caption': 'Final optimized model training dynamics',
        'description': 'Left: loss convergence. Right: accuracy progression'
    },
    {
        'number': 6,
        'files': ['confusion_matrix_final_model.png'],
        'caption': 'Confusion matrix for the final deployed model on test set',
        'description': 'Shows final model classification performance'
    },
    {
        'number': 7,
        'files': ['roc_curve_best_nn_s3.png'],
        'caption': 'Receiver Operating Characteristic curve (AUC-ROC)',
        'description': 'Demonstrates discrimination capability across thresholds'
    }
]

# ============================================================================
# DISPLAY ORDER
# ============================================================================
# Define the exact order outputs should appear in the Results section.
# Use 'table-N' or 'figure-N' where N matches the number defined above.
#
# Examples of different ordering strategies:
#   All tables first:    ['table-1', 'table-2', 'figure-1', 'figure-2', ...]
#   Interleaved:         ['table-1', 'figure-1', 'figure-2', 'table-2', ...]
#   Custom grouping:     ['table-1', 'figure-1', 'figure-2', 'figure-3', 'table-2', ...]

ORDER = [
    'table-1',    # Comparison across stages (overview)
    'figure-1',   # Training dynamics
    'figure-2',   # Confusion matrices (all models)
    'figure-3',   # Best model CM
    'figure-4',   # Tuned models comparison
    'table-2',    # Detailed metrics (after seeing visuals)
    'figure-5',   # Final model training
    'figure-6',   # Final model CM
    'figure-7',   # ROC curve
]


# ============================================================================
# MAIN RUNNER
# ============================================================================

def main():
    """Generate ground truth and phase prompts"""
    
    # Add to path
    sys.path.insert(0, str(PROJECT_ROOT))
    
    from agent_quarto_reports.improved_converter import ImprovedQuartoConverter, Phase
    
    print(f"\n{'='*80}")
    print(f"PROJECT: {PROJECT_NAME.upper()}")
    print(f"{'='*80}")
    print(f"Notebook: {NOTEBOOK.name}")
    print(f"Output:   {OUTPUT_QMD.name}")
    print(f"RAG:      {'Enabled' if ENABLE_RAG else 'Disabled'}")
    print(f"Tables:   {len(TABLES)}")
    print(f"Figures:  {len(FIGURES)}")
    print()
    
    # Initialize converter
    converter = ImprovedQuartoConverter(
        notebook_path=NOTEBOOK,
        output_path=OUTPUT_QMD,
        selected_outputs={
            'tables': TABLES,
            'figures': FIGURES,
            'order': ORDER  # Pass the custom order
        },
        enable_rag=ENABLE_RAG
    )
    
    # Phase 1: Extract ground truth (automated)
    converter.run_phase_1_extract()
    
    # Generate prompts for phases 2-7
    print(f"\n{'='*80}")
    print("GENERATING PHASE PROMPTS")
    print(f"{'='*80}\n")
    
    # Phase 2: Structure (Methods + Objectives)
    converter.save_phase_prompt(Phase.STRUCTURE, context={})
    
    # Phase 3: Visualize (Add figures/tables)
    converter.save_phase_prompt(Phase.VISUALIZE, context={})
    
    # Phase 4: Analyze (ONE output at a time)
    # Generate prompt for EACH table
    for idx, table in enumerate(TABLES):
        converter.save_phase_prompt(
            Phase.ANALYZE,
            output_file=PROJECT_ROOT / 'assets' / PROJECT_NAME / f'agent_prompt_phase_4_analyze_table_{idx+1}.md',
            context={
                'current_result_index': idx,
                'total_results': len(TABLES) + len(FIGURES),
                'current_output': {'type': 'table', 'file': table}
            }
        )
    
    # Generate prompt for EACH figure group
    for idx, figure_group in enumerate(FIGURES, start=len(TABLES)):
        converter.save_phase_prompt(
            Phase.ANALYZE,
            output_file=PROJECT_ROOT / 'assets' / PROJECT_NAME / f'agent_prompt_phase_4_analyze_figure_{idx-len(TABLES)+1}.md',
            context={
                'current_result_index': idx,
                'total_results': len(TABLES) + len(FIGURES),
                'current_output': {'type': 'figure', 'files': figure_group}
            }
        )
    
    # Phase 5: Synthesize (Discussion + Conclusion)
    converter.save_phase_prompt(Phase.SYNTHESIZE, context={})
    
    # Phase 6: Frame (Introduction - LAST!)
    converter.save_phase_prompt(Phase.FRAME, context={})
    
    # Phase 7: Validate
    converter.save_phase_prompt(Phase.VALIDATE, context={})
    
    print(f"\n{'='*80}")
    print("✅ ALL PROMPTS GENERATED")
    print(f"{'='*80}\n")
    print(f"Ground truth: assets/{PROJECT_NAME}/figures/{NOTEBOOK.stem}_ground_truth.json")
    print(f"Prompts:      assets/{PROJECT_NAME}/agent_prompt_phase_*.md")
    print()
    print("NEXT STEPS:")
    print("1. Execute Phase 2 (Structure): Write Methods + Objectives")
    print("2. Execute Phase 3 (Visualize): Add all figures/tables")
    print(f"3. Execute Phase 4 (Analyze): Write Results for each of {len(TABLES) + len(FIGURES)} outputs")
    print("   - Use agent_prompt_phase_4_analyze_table_1.md")
    print("   - Use agent_prompt_phase_4_analyze_table_2.md")
    print("   - Use agent_prompt_phase_4_analyze_figure_1.md")
    print("   - ... (one at a time to avoid cognitive overload)")
    print("4. Execute Phase 5 (Synthesize): Discussion + Conclusion")
    print("5. Execute Phase 6 (Frame): Introduction")
    print("6. Execute Phase 7 (Validate): Check accuracy")
    print()


if __name__ == "__main__":
    main()
