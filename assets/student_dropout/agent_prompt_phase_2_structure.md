
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
        figcaption.quarto-float-caption {
          text-align: left !important;
        }
        .quarto-figure-center {
          text-align: left !important;
        }
        .fig-label-left-edge {
          text-align: left !important;
          margin-left: calc(-46vw + 50%);
          width: 100vw;
          position: relative;
          left: 0;
        }
        /* Numbered references */
        #refs .csl-entry {
          padding-left: 2em;
          text-indent: -2em;
          margin-bottom: 1em;
        }
        #refs {
          counter-reset: ref-counter;
        }
        #refs .csl-entry::before {
          counter-increment: ref-counter;
          content: counter(ref-counter) ". ";
          margin-right: 0.5em;
        }
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
{
  "stage_3": {
    "description": "# Stage 3 data",
    "techniques": [
      "dropout_regularization",
      "l2_regularization",
      "dropout_regularization",
      "l2_regularization",
      "adam_optimizer"
    ]
  },
  "stage_2": {
    "description": "#### Based on analysis performed for Stage 2 data, UnauthorisedAbsenceCount and AuthorisedAbsenceCount were transformed into categories by binning. ",
    "techniques": [
      "dropout_regularization"
    ]
  },
  "stage_1": {
    "description": "#### EDA for stage 1 showed that the Nationality features is heavily skewed to two nationalities with Chinese representing 36.08% of the students and Bangladeshi representing another 8.01%, which is a",
    "techniques": [
      "dropout_regularization"
    ]
  }
}
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
