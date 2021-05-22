class TodoError(Exception):
    code = ""


class TitleLengthError(TodoError):
    code = "TITLE_LENGTH_ERROR"


class NotFoundError(TodoError):
    code = "NOT_FOUND"
