from src.components.data_ingestion import DataIngestion

def main():

    ingestion = DataIngestion()

    df = ingestion.load_data()

    print(df.head())

    print()

    print(df.shape)


if __name__ == "__main__":
    main()