#!/usr/bin/env python3
"""
Example script demonstrating how to use the ExcelAnalyzer class programmatically.
"""

from excel_analyzer import ExcelAnalyzer

def main():
    """Example usage of ExcelAnalyzer."""
    print("=== Excel Analyzer Example ===\n")
    
    # Check if sample data exists
    try:
        # Create analyzer for sample data
        analyzer = ExcelAnalyzer('sample_data.xlsx')
        
        print("Example 1: Basic Information")
        info = analyzer.basic_info()
        print(f"Dataset has {info['shape'][0]} rows and {info['shape'][1]} columns\n")
        
        print("Example 2: Missing Data Analysis")
        missing = analyzer.missing_data_analysis()
        print()
        
        print("Example 3: Quick Statistics")
        stats = analyzer.descriptive_statistics()
        print()
        
        print("Example 4: Correlation Analysis")
        corr = analyzer.correlation_analysis()
        print()
        
        print("Example 5: Create visualizations only")
        analyzer.create_visualizations(output_dir="example_plots")
        print("Visualizations saved to 'example_plots' directory\n")
        
        print("Example 6: Export report only")
        analyzer.export_summary_report("example_report.xlsx")
        print("Report saved as 'example_report.xlsx'\n")
        
        print("✅ All examples completed successfully!")
        print("You can also run the complete analysis with:")
        print("analyzer.run_complete_analysis()")
        
    except FileNotFoundError:
        print("Error: sample_data.xlsx not found.")
        print("Please run 'python excel_analyzer.py sample_data.xlsx' first to create sample data.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()