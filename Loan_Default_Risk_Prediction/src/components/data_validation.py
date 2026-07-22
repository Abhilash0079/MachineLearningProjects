import os
from src.logger import logger
from src.utils.common import read_yaml

class DataValidation:
    def __init__(self, dataframe):
        self.df = dataframe
        config = read_yaml('config/config.yaml')
        self.expected_rows = config['validation']['expected_rows']
        self.expected_columns = config['validation']['expected_columns']
        self.target_column = config['data']['target_column']
    
    def validate(self):
        logger.info("Staring data validation...")
        report = {}
        report['Rows'] = self.df.shape[0]
        report['Columns'] = self.df.shape[1]

        report['Expected Rows'] = self.expected_rows
        report['Expected Columns'] = self.expected_columns

        report['Shape Valid'] = (
            self.df.shape[0] == self.expected_rows and self.df.shape[1] == self.expected_columns
        )

        report['Target Present'] = self.target_column in self.df.columns
        report['Duplicate Rows'] = self.df.duplicated().sum()
        report['Missing Values'] = int(self.df.isnull().sum().sum())
        report['Data Types'] = self.df.dtypes.astype(str).value_counts().to_dict()

        os.makedirs('artifats/reports', exist_ok=True)
        report_path = 'artifacts/reports/validation_report.txt'

        with open(report_path,'w', encoding='utf-8') as file:
            for key, value in report.items():
                file.write(f"{key}: {value}\n")
        
        logger.info("Validation completed successfully.")

        return report