# Environment Update: my_website Conda Environment

**Date**: 2025-10-09  
**Environment**: `my_website` (Python 3.12)  
**Purpose**: Support student dropout prediction notebook and ML/DS projects

## Packages Installed

### Core Data Science & ML Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| **numpy** | 2.3.3 | Numerical computing |
| **pandas** | 2.3.3 | Data manipulation |
| **matplotlib** | 3.10.7 | Data visualization |
| **seaborn** | 0.13.2 | Statistical visualization |
| **scipy** | 1.16.2 | Scientific computing |

### Machine Learning

| Package | Version | Purpose |
|---------|---------|---------|
| **scikit-learn** | 1.7.2 | ML algorithms, preprocessing, metrics |
| **xgboost** | 3.0.5 | Gradient boosting framework |
| **shap** | 0.48.0 | Model interpretability |

### Deep Learning

| Package | Version | Purpose |
|---------|---------|---------|
| **tensorflow** | 2.20.0 | Deep learning framework |
| **keras** | 3.11.3 | High-level neural network API |

### Supporting Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| **tqdm** | 4.67.1 | Progress bars |
| **joblib** | 1.5.2 | Parallel computing |
| **numba** | 0.62.1 | JIT compilation |

### Previously Installed (Quarto/Jupyter)

| Package | Version | Purpose |
|---------|---------|---------|
| **jupyter** | 1.1.1 | Notebook environment |
| **jupyterlab** | 4.4.9 | Advanced notebook IDE |
| **nbclient** | 0.10.2 | Notebook execution |
| **nbformat** | 5.10.4 | Notebook format |
| **pyyaml** | 6.0.3 | YAML parsing |
| **tabulate** | 0.9.0 | Table formatting |

## System Requirements

### macOS Specific
- **OpenMP** (libomp) - Required for XGBoost
  ```bash
  brew install libomp
  ```

## Activation

```bash
conda activate my_website
```

## Verification

Test all packages are working:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from keras.optimizers import Adam, RMSprop
from sklearn.metrics import accuracy_score, roc_auc_score
import xgboost as xgb
import shap
from scipy.stats import pearsonr
from tqdm import tqdm
```

## Package Compatibility

All packages have been verified to work together:
- ✅ TensorFlow 2.20.0 with Keras 3.11.3
- ✅ XGBoost 3.0.5 with NumPy 2.3.3
- ✅ Scikit-learn 1.7.2 with pandas 2.3.3
- ✅ All packages compatible with Python 3.12

## Use Cases

This environment supports:
1. **Quarto website rendering** with Python code execution
2. **Machine Learning projects** (XGBoost, Neural Networks)
3. **Data analysis** with pandas, numpy, scipy
4. **Visualization** with matplotlib, seaborn
5. **Model interpretability** with SHAP
6. **Jupyter notebooks** for development

## Notes

- All packages installed via `pip` for better compatibility
- OpenMP installed via Homebrew (system-level dependency)
- Environment follows constitution requirement: Python 3.12 in my_website conda env
- Total environment size: ~2.5GB
- Full package list available in `requirements.txt`

## Future Additions

To add more packages to this environment:

```bash
conda activate my_website
pip install <package-name>
```

Always verify compatibility with existing packages after installation.
