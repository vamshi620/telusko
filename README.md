# Excel Analysis Tool

A comprehensive Python tool for analyzing Excel files with statistical analysis and data visualization features.

## Features

- **Data Loading**: Supports loading Excel files with specific sheet selection
- **Basic Analysis**: Dataset information, shape, data types, and memory usage
- **Missing Data Analysis**: Identifies and quantifies missing values
- **Descriptive Statistics**: Statistical summaries for numeric and categorical data
- **Correlation Analysis**: Correlation matrix for numeric columns
- **Outlier Detection**: IQR and Z-score methods for outlier identification
- **Data Visualization**: Automatic generation of distribution plots, correlation heatmaps, and box plots
- **Export Reports**: Comprehensive analysis reports exported to Excel format

## Installation

1. Clone this repository:
```bash
git clone https://github.com/vamshi620/telusko.git
cd telusko
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Basic usage:
```bash
python excel_analyzer.py <excel_file_path>
```

With specific sheet:
```bash
python excel_analyzer.py <excel_file_path> <sheet_name>
```

### Examples

Analyze the sample data:
```bash
python excel_analyzer.py sample_data.xlsx
```

Analyze a specific sheet:
```bash
python excel_analyzer.py data.xlsx "Sales Data"
```

### Using as a Python Module

```python
from excel_analyzer import ExcelAnalyzer

# Create analyzer instance
analyzer = ExcelAnalyzer('your_file.xlsx')

# Run complete analysis
analyzer.run_complete_analysis()

# Or run individual analyses
analyzer.basic_info()
analyzer.missing_data_analysis()
analyzer.descriptive_statistics()
analyzer.correlation_analysis()
analyzer.outlier_detection()
analyzer.create_visualizations()
analyzer.export_summary_report()
```

## Output Files

The tool generates several output files:

1. **Plots Directory**: Contains visualization files
   - `distributions.png`: Distribution plots for all numeric columns
   - `correlation_heatmap.png`: Correlation heatmap for numeric data
   - `boxplots.png`: Box plots for outlier detection

2. **analysis_report.xlsx**: Comprehensive Excel report with multiple sheets:
   - Basic_Info: Dataset overview and metrics
   - Missing_Data: Missing value analysis
   - Numeric_Stats: Descriptive statistics for numeric columns
   - Categorical_Stats: Descriptive statistics for categorical columns
   - Correlation: Correlation matrix

## Sample Data

The repository includes `sample_data.xlsx` with employee data for testing:
- 100 rows of employee information
- Columns: Name, Age, Salary, Department, Experience, Performance_Score
- Contains some missing values for testing missing data analysis

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- openpyxl >= 3.0.10
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- numpy >= 1.21.0

## License

This project is open source and available under the MIT License.