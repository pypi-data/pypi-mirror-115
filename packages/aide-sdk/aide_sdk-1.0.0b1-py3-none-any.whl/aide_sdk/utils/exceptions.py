class ManifestNotFoundError(Exception):
    def __init__(self):
        super().__init__("The manifest.json file could not be found")


class ManifestNotValidError(Exception):
    def __init__(self):
        super().__init__("The manifest.json is invalid")
