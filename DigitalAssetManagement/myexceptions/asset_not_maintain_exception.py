class AssetNotMaintainException(Exception):
    def __init__(self, message="Asset has not been maintained for more than 2 years."):
        super().__init__(message)
