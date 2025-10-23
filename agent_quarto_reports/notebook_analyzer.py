#!/usr/bin/env python3
"""
Notebook Analyzer - Extract Ground Truth from Jupyter Notebooks

This module analyzes notebooks to extract:
1. Notebook summary (what was actually done)
2. Numerical results from outputs
3. Figure/table metadata
4. Methods described

Creates notebook_ground_truth.json for validation.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import nbformat


class NotebookAnalyzer:
    """Extract factual information from Jupyter notebooks."""
    
    def __init__(self, notebook_path: Path):
        """Initialize analyzer with notebook path."""
        self.notebook_path = Path(notebook_path)
        self.notebook = nbformat.read(self.notebook_path, as_version=4)
        self.ground_truth = {
            'notebook_path': str(notebook_path),
            'summary': {},
            'methods': {},
            'results': {},
            'figures': [],
            'tables': [],
            'numerical_facts': []
        }
    
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis and return ground truth."""
        print(f"Analyzing notebook: {self.notebook_path.name}")
        
        # Extract different components
        self._extract_summary()
        self._extract_methods()
        self._extract_results()
        self._extract_figures_tables()
        
        print(f"✓ Analysis complete")
        print(f"  - Methods sections: {len(self.ground_truth['methods'])}")
        print(f"  - Numerical facts: {len(self.ground_truth['numerical_facts'])}")
        print(f"  - Figures found: {len(self.ground_truth['figures'])}")
        print(f"  - Tables found: {len(self.ground_truth['tables'])}")
        
        return self.ground_truth
    
    def _extract_summary(self):
        """Extract high-level summary from notebook."""
        # Get title from first markdown cell
        for cell in self.notebook.cells[:5]:
            if cell.cell_type == 'markdown':
                lines = cell.source.split('\n')
                for line in lines:
                    if line.startswith('#') and not line.startswith('##'):
                        self.ground_truth['summary']['title'] = line.strip('# ').strip()
                        break
                if self.ground_truth['summary'].get('title'):
                    break
        
        # Count cells
        self.ground_truth['summary']['total_cells'] = len(self.notebook.cells)
        self.ground_truth['summary']['code_cells'] = sum(1 for c in self.notebook.cells if c.cell_type == 'code')
        self.ground_truth['summary']['markdown_cells'] = sum(1 for c in self.notebook.cells if c.cell_type == 'markdown')
    
    def _extract_methods(self):
        """Extract methods information from markdown cells."""
        methods_keywords = ['stage 1', 'stage 2', 'stage 3', 'preprocessing', 'feature engineering', 
                          'model', 'training', 'evaluation', 'data']
        
        current_stage = None
        
        for cell in self.notebook.cells:
            if cell.cell_type == 'markdown':
                source_lower = cell.source.lower()
                
                # Detect stages
                for keyword in ['stage 1', 'stage 2', 'stage 3']:
                    if keyword in source_lower:
                        current_stage = keyword.replace(' ', '_')
                        if current_stage not in self.ground_truth['methods']:
                            self.ground_truth['methods'][current_stage] = {
                                'description': cell.source[:200],
                                'techniques': []
                            }
                
                # Extract techniques mentioned
                if current_stage:
                    techniques = []
                    if 'dropout' in source_lower:
                        techniques.append('dropout_regularization')
                    if 'l2' in source_lower or 'regularization' in source_lower:
                        techniques.append('l2_regularization')
                    if 'adam' in source_lower:
                        techniques.append('adam_optimizer')
                    if 'rmsprop' in source_lower:
                        techniques.append('rmsprop_optimizer')
                    
                    if techniques:
                        self.ground_truth['methods'][current_stage]['techniques'].extend(techniques)
    
    def _extract_results(self):
        """Extract numerical results from cell outputs."""
        for idx, cell in enumerate(self.notebook.cells):
            if cell.cell_type == 'code' and cell.get('outputs'):
                for output in cell.outputs:
                    # Extract from text outputs
                    if output.output_type == 'stream':
                        text = output.get('text', '')
                        self._parse_numbers(text, f"cell_{idx}")
                    
                    # Extract from display data
                    elif output.output_type in ['display_data', 'execute_result']:
                        if 'text/plain' in output.get('data', {}):
                            text = output['data']['text/plain']
                            self._parse_numbers(text, f"cell_{idx}")
    
    def _parse_numbers(self, text: str, source: str):
        """Parse numerical values from text."""
        # Look for patterns like "accuracy: 0.95" or "F1: 0.972"
        patterns = [
            r'(accuracy|f1|precision|recall|auc|roc)[\s:=]+(\d+\.?\d*)',
            r'(\d+\.?\d*)%?\s+(accuracy|f1|precision|recall)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                metric = match.group(1) if match.group(1) in ['accuracy', 'f1', 'precision', 'recall', 'auc', 'roc'] else match.group(2)
                value = float(match.group(2)) if match.group(1) in ['accuracy', 'f1', 'precision', 'recall', 'auc', 'roc'] else float(match.group(1))
                
                self.ground_truth['numerical_facts'].append({
                    'metric': metric,
                    'value': value,
                    'source': source,
                    'context': text[:100]
                })
    
    def _extract_figures_tables(self):
        """Extract figure and table information from code cells."""
        for idx, cell in enumerate(self.notebook.cells):
            if cell.cell_type == 'code':
                source = cell.source.lower()
                
                # Detect figure creation
                if any(x in source for x in ['plt.', 'plot(', 'savefig', 'figure']):
                    # Try to extract filename
                    filename_match = re.search(r'savefig\([\'"]([^\'"]+)[\'"]', source)
                    if filename_match:
                        self.ground_truth['figures'].append({
                            'cell_index': idx,
                            'filename': filename_match.group(1),
                            'type': 'matplotlib'
                        })
                
                # Detect table/dataframe display
                if any(x in source for x in ['to_csv', 'dataframe', '.head(', 'display(']):
                    filename_match = re.search(r'to_csv\([\'"]([^\'"]+)[\'"]', source)
                    if filename_match:
                        self.ground_truth['tables'].append({
                            'cell_index': idx,
                            'filename': filename_match.group(1),
                            'type': 'csv'
                        })
    
    def save_ground_truth(self, output_path: Optional[Path] = None) -> Path:
        """Save ground truth to JSON file."""
        if output_path is None:
            output_path = self.notebook_path.parent / f"{self.notebook_path.stem}_ground_truth.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.ground_truth, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Ground truth saved: {output_path}")
        return output_path


def analyze_notebook(notebook_path: Path, output_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Analyze notebook and extract ground truth.
    
    Args:
        notebook_path: Path to Jupyter notebook
        output_path: Optional path to save ground truth JSON
    
    Returns:
        Dictionary containing ground truth information
    """
    analyzer = NotebookAnalyzer(notebook_path)
    ground_truth = analyzer.analyze()
    
    if output_path or True:  # Always save by default
        analyzer.save_ground_truth(output_path)
    
    return ground_truth


if __name__ == '__main__':
    # Test with student dropout notebook
    notebook = Path('/Users/rodrigograndy/Desktop/coding_projects/my_website/assets/student_dropout/figures/student_dropout_nn_151025.ipynb')
    
    if notebook.exists():
        print("Testing Notebook Analyzer...")
        ground_truth = analyze_notebook(notebook)
        print("\n" + "="*80)
        print("GROUND TRUTH SUMMARY")
        print("="*80)
        print(json.dumps(ground_truth['summary'], indent=2))
    else:
        print(f"Notebook not found: {notebook}")
