
# PHASE 3: VISUALIZE (Add Figures/Tables)

## Your Task
Add 2 tables and 7 figures to the Results section IN THIS EXACT ORDER.

## CRITICAL: Follow This Exact Sequence

1. **Table 1**: comparison_neural_networks_all_stages.csv
   - Compares Base vs Tuned models across Stage 1, 2, and 3 data
   - Caption: Performance comparison of neural network architectures across three data stages
2. **Figure 1**: val_accuracy_curve_s3_nn.png, learning_curve_nn_s3.png
   - Left: validation accuracy curves. Right: training/validation loss
   - Caption: Neural network training dynamics showing validation accuracy progression and loss convergence
3. **Figure 2**: cm_all_models_nn_red_square.png
   - Shows classification patterns and error distributions
   - Caption: Confusion matrices across all neural network configurations
4. **Figure 3**: comparison_cm_best_nn_s3.png
   - Compares best model performance across metrics
   - Caption: Detailed confusion matrix comparison for best performing architecture
5. **Figure 4**: tuned_nn_models_best_highlighted.png
   - Shows effect of different hyperparameter combinations
   - Caption: Performance comparison of hyperparameter-tuned models
6. **Table 2**: nn_models_evaluation.csv
   - Shows precision, recall, F1-score, and AUC-ROC for all configurations
   - Caption: Detailed evaluation metrics for neural network models
7. **Figure 5**: learning_curve_final_model.png, accuracy_curve_final_nn_s3_model.png
   - Left: loss convergence. Right: accuracy progression
   - Caption: Final optimized model training dynamics
8. **Figure 6**: confusion_matrix_final_model.png
   - Shows final model classification performance
   - Caption: Confusion matrix for the final deployed model on test set
9. **Figure 7**: roc_curve_best_nn_s3.png
   - Demonstrates discrimination capability across thresholds
   - Caption: Receiver Operating Characteristic curve (AUC-ROC)

## Format Requirements

### For Tables
```python
#| label: tbl-{table-number}
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
<figure id="fig-{figure-number}">
  <img src="../assets/student_dropout/figures/[filename]" 
       style="width: 70%; max-width: 600px; margin: 0 auto; display: block;" 
       alt="[description]">
  <figcaption>Figure {number}: [Use the EXACT caption from the list above]</figcaption>
</figure>
```

### For Multi-Panel Figures (2 images side by side)
```html
<figure id="fig-{figure-number}">
  <div style="display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap;">
    <img src="../assets/student_dropout/figures/[file1]" 
         style="width: 40%; min-width: 300px;" alt="[desc1]">
    <img src="../assets/student_dropout/figures/[file2]" 
         style="width: 40%; min-width: 300px;" alt="[desc2]">
  </div>
  <figcaption>Figure {number}: [Use the EXACT caption from the list above]</figcaption>
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
