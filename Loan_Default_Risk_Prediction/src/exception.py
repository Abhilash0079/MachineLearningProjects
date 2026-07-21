import sys


def get_error_message(error: Exception) -> str:
    _, _, traceback_object = sys.exc_info()

    if traceback_object is None:
        return str(error)

    file_name = traceback_object.tb_frame.f_code.co_filename
    line_number = traceback_object.tb_lineno

    return (
        f"Error occurred in file '{file_name}', "
        f"at line {line_number}: {str(error)}"
    )


class LoanDefaultException(Exception):
    def __init__(self, error: Exception):
        self.error_message = get_error_message(error)
        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message