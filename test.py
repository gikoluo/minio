
#pip install minio


from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from minio import PostPolicy
import requests

ACCESS_KEY = 'minio'
SECRET_KEY = 'minio123'
# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('127.0.0.1:9001',
                    access_key=ACCESS_KEY,
                    secret_key=SECRET_KEY,
                    secure=False)





# Make a bucket with the make_bucket API call.
try:
       minioClient.make_bucket("photo", location="asia-east-1")
except BucketAlreadyOwnedByYou as err:
       pass
except BucketAlreadyExists as err:
       pass
except ResponseError as err:
       raise

photo_policy = '''{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetBucketLocation","s3:ListBucket"],"Resource":["arn:aws:s3:::photo"]},{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::photo/*"]}]}'''
minioClient.set_bucket_policy('photo', photo_policy)


# Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
try:
       minioClient.fput_object('photo', 'photo.jpg', '/tmp/photo.jpg')
except ResponseError as err:
       print(err)

r = requests.get('http://127.0.0.1:9001/photo/photo.jpg')

print(r.content)