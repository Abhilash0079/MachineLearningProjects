from src.exception import LoanDefaultException
from src.logger import logger


def test_project_setup() -> None:
    try:
        logger.info("Testing project setup.")

        first_number = 10
        second_number = 5

        result = first_number + second_number

        logger.info("Project setup test completed successfully.")
        print(f"Project setup is working. Result: {result}")

    except Exception as error:
        logger.exception("Project setup failed.")
        raise LoanDefaultException(error) from error


if __name__ == "__main__":
    test_project_setup()