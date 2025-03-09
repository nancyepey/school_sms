from storages.backends.s3 import S3Storage 

class StaticFileStorage(S3Storage):
    #helpers.cloudflare.storages.StaticFileStorage, the new location
    location = "static"
    
class MediaFileStorage(S3Storage):
    #helpers.cloudflare.storages.MediaFileStorage , the new location
    location = "media"