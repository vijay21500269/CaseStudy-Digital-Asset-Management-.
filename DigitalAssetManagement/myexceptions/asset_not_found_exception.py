class AssetNotFoundException(Exception):
    def __init__(self, message="Asset not found."):
        super().__init__(message)
