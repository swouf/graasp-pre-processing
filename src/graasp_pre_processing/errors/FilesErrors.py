class DirError(Exception):
    def __init__(self, path, *args: object) -> None:
        self.path = path
        super().__init__(f'The path {self.path} is not a folder ', *args)