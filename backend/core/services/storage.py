from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Storage class for handling static files in S3"""

    location = "static"


class MediaStorage(S3Boto3Storage):
    """Storage class for handling media uploads in S3"""

    location = "media"
