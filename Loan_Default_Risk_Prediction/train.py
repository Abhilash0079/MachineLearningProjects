from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation

def main():
    ingestion = DataIngestion()
    df = ingestion.load_data()
    validator = DataValidation(df)
    report = validator.validate()
    print("\nValidation Report\n")

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()