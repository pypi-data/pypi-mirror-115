from minio import Minio


class MinioUtil(Minio):
    def __init__(self, bucket=None, *args, **kwargs):
        super(MinioUtil, self).__init__(*args, **kwargs)
        self.bucket = bucket
        self.create_bucket(self.bucket)

    def create_bucket(self, bucket):
        found = self.bucket_exists(bucket)
        if not found:
            self.make_bucket(bucket)

    def upload_file(self, src, dst, bucket=None):
        bucket = self.__get_bucket(bucket)
        self.fput_object(bucket, dst, src)

    def minio_utils(self, file, bucket=None):
        bucket = self.__get_bucket(bucket)
        self.remove_object(bucket, file)

    def __get_bucket(self, bucket):
        return bucket if bucket else self.bucket


if __name__ == '__main__':
    client = MinioUtil(
        default_bucket="bucket",
        endpoint="localhost:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )
