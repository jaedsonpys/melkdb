class ValueNotSupportedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class KeyIsNotAStringError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class IncompatibleDatabaseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DecryptFailed(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
