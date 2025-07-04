#!/usr/bin/env python3
"""
Excel Analysis Tool
A comprehensive tool for analyzing Excel files with various statistical and visualization features.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys
from typing import Dict, List, Optional, Tuple


class ExcelAnalyzer:
    """A class to analyze Excel files with various statistical and visualization methods."""
    
    def __init__(self, file_path: str, sheet_name: Optional[str] = None):
        """
        Initialize the Excel analyzer.
        
        Args:
            file_path (str): Path to the Excel file
            sheet_name (str, optional): Specific sheet name to analyze. If None, uses the first sheet.
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.data = None
        self.numeric_columns = []
        self.categorical_columns = []
        
        self._load_data()
        self._categorize_columns()
    
    def _load_data(self):
        """Load data from Excel file."""
        try:
            if self.sheet_name:
                self.data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            else:
                self.data = pd.read_excel(self.file_path)
            print(f"Successfully loaded data from {self.file_path}")
            if self.sheet_name:
                print(f"Sheet: {self.sheet_name}")
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            sys.exit(1)
    
    def _categorize_columns(self):
        """Categorize columns into numeric and categorical."""
        self.numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def basic_info(self) -> Dict:
        """
        Get basic information about the dataset.
        
        Returns:
            Dict: Dictionary containing basic dataset information
        """
        info = {
            'shape': self.data.shape,
            'columns': self.data.columns.tolist(),
            'dtypes': self.data.dtypes.to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum(),
            'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns
        }
        
        print("=== BASIC DATASET INFORMATION ===")
        print(f"Shape: {info['shape'][0]} rows × {info['shape'][1]} columns")
        print(f"Memory usage: {info['memory_usage'] / 1024:.2f} KB")
        print(f"Numeric columns ({len(self.numeric_columns)}): {self.numeric_columns}")
        print(f"Categorical columns ({len(self.categorical_columns)}): {self.categorical_columns}")
        
        return info
    
    def missing_data_analysis(self) -> pd.DataFrame:
        """
        Analyze missing data in the dataset.
        
        Returns:
            pd.DataFrame: DataFrame with missing data statistics
        """
        missing_data = pd.DataFrame({
            'Column': self.data.columns,
            'Missing_Count': self.data.isnull().sum(),
            'Missing_Percentage': (self.data.isnull().sum() / len(self.data)) * 100
        })
        
        missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values('Missing_Percentage', ascending=False)
        
        print("\n=== MISSING DATA ANALYSIS ===")
        if missing_data.empty:
            print("No missing data found in the dataset.")
        else:
            print(missing_data.to_string(index=False))
        
        return missing_data
    
    def descriptive_statistics(self) -> Dict[str, pd.DataFrame]:
        """
        Generate descriptive statistics for numeric and categorical data.
        
        Returns:
            Dict: Dictionary containing descriptive statistics
        """
        stats = {}
        
        if self.numeric_columns:
            stats['numeric'] = self.data[self.numeric_columns].describe()
            print("\n=== DESCRIPTIVE STATISTICS (NUMERIC) ===")
            print(stats['numeric'])
        
        if self.categorical_columns:
            stats['categorical'] = self.data[self.categorical_columns].describe(include='all')
            print("\n=== DESCRIPTIVE STATISTICS (CATEGORICAL) ===")
            print(stats['categorical'])
        
        return stats
    
    def correlation_analysis(self) -> Optional[pd.DataFrame]:
        """
        Perform correlation analysis on numeric columns.
        
        Returns:
            pd.DataFrame: Correlation matrix if numeric columns exist
        """
        if len(self.numeric_columns) < 2:
            print("\n=== CORRELATION ANALYSIS ===")
            print("Not enough numeric columns for correlation analysis.")
            return None
        
        correlation_matrix = self.data[self.numeric_columns].corr()
        
        print("\n=== CORRELATION ANALYSIS ===")
        print(correlation_matrix)
        
        return correlation_matrix
    
    def outlier_detection(self, method: str = 'iqr') -> Dict[str, List]:
        """
        Detect outliers in numeric columns.
        
        Args:
            method (str): Method to use for outlier detection ('iqr' or 'zscore')
        
        Returns:
            Dict: Dictionary with outlier information for each numeric column
        """
        outliers = {}
        
        print(f"\n=== OUTLIER DETECTION ({method.upper()}) ===")
        
        for col in self.numeric_columns:
            if method == 'iqr':
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outlier_mask = (self.data[col] < lower_bound) | (self.data[col] > upper_bound)
            elif method == 'zscore':
                z_scores = np.abs((self.data[col] - self.data[col].mean()) / self.data[col].std())
                outlier_mask = z_scores > 3
            
            outlier_indices = self.data[outlier_mask].index.tolist()
            outliers[col] = outlier_indices
            
            print(f"{col}: {len(outlier_indices)} outliers detected")
        
        return outliers
    
    def create_visualizations(self, output_dir: str = "plots"):
        """
        Create various visualizations for the data.
        
        Args:
            output_dir (str): Directory to save plots
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        plt.style.use('default')
        
        # 1. Distribution plots for numeric columns
        if self.numeric_columns:
            n_cols = min(3, len(self.numeric_columns))
            n_rows = (len(self.numeric_columns) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            if n_rows == 1:
                axes = [axes] if n_cols == 1 else axes
            else:
                axes = axes.flatten()
            
            for i, col in enumerate(self.numeric_columns):
                if i < len(axes):
                    self.data[col].hist(bins=30, ax=axes[i], alpha=0.7)
                    axes[i].set_title(f'Distribution of {col}')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('Frequency')
            
            # Hide empty subplots
            for i in range(len(self.numeric_columns), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/distributions.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # 2. Correlation heatmap
        if len(self.numeric_columns) >= 2:
            plt.figure(figsize=(10, 8))
            correlation_matrix = self.data[self.numeric_columns].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, linewidths=0.5)
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        # 3. Box plots for numeric columns
        if self.numeric_columns:
            fig, axes = plt.subplots(1, len(self.numeric_columns), figsize=(5 * len(self.numeric_columns), 6))
            if len(self.numeric_columns) == 1:
                axes = [axes]
            
            for i, col in enumerate(self.numeric_columns):
                self.data.boxplot(column=col, ax=axes[i])
                axes[i].set_title(f'Box Plot of {col}')
            
            plt.tight_layout()
            plt.savefig(f"{output_dir}/boxplots.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"\nVisualization plots saved in '{output_dir}' directory:")
        print("- distributions.png: Distribution plots for numeric columns")
        if len(self.numeric_columns) >= 2:
            print("- correlation_heatmap.png: Correlation heatmap")
        print("- boxplots.png: Box plots for outlier detection")
    
    def export_summary_report(self, output_file: str = "analysis_report.xlsx"):
        """
        Export a comprehensive analysis report to Excel.
        
        Args:
            output_file (str): Output Excel file name
        """
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Basic info sheet
            info_df = pd.DataFrame([
                ['Total Rows', self.data.shape[0]],
                ['Total Columns', self.data.shape[1]],
                ['Numeric Columns', len(self.numeric_columns)],
                ['Categorical Columns', len(self.categorical_columns)]
            ], columns=['Metric', 'Value'])
            info_df.to_excel(writer, sheet_name='Basic_Info', index=False)
            
            # Missing data analysis
            missing_data = self.missing_data_analysis()
            if not missing_data.empty:
                missing_data.to_excel(writer, sheet_name='Missing_Data', index=False)
            
            # Descriptive statistics
            if self.numeric_columns:
                self.data[self.numeric_columns].describe().to_excel(writer, sheet_name='Numeric_Stats')
            
            if self.categorical_columns:
                self.data[self.categorical_columns].describe(include='all').to_excel(writer, sheet_name='Categorical_Stats')
            
            # Correlation matrix
            if len(self.numeric_columns) >= 2:
                self.data[self.numeric_columns].corr().to_excel(writer, sheet_name='Correlation')
        
        print(f"\nComprehensive analysis report exported to '{output_file}'")
    
    def run_complete_analysis(self, create_plots: bool = True, export_report: bool = True):
        """
        Run complete analysis pipeline.
        
        Args:
            create_plots (bool): Whether to create visualization plots
            export_report (bool): Whether to export summary report
        """
        print("🔍 Starting Complete Excel Analysis...")
        print("=" * 50)
        
        # Basic analysis
        self.basic_info()
        self.missing_data_analysis()
        self.descriptive_statistics()
        self.correlation_analysis()
        self.outlier_detection()
        
        # Optional outputs
        if create_plots:
            self.create_visualizations()
        
        if export_report:
            self.export_summary_report()
        
        print("\n" + "=" * 50)
        print("✅ Analysis completed successfully!")


def main():
    """Main function to run the Excel analyzer."""
    if len(sys.argv) < 2:
        print("Usage: python excel_analyzer.py <excel_file_path> [sheet_name]")
        print("Example: python excel_analyzer.py data.xlsx")
        print("Example: python excel_analyzer.py data.xlsx Sheet1")
        sys.exit(1)
    
    file_path = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    # Create analyzer and run analysis
    analyzer = ExcelAnalyzer(file_path, sheet_name)
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()