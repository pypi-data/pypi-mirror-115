# Pytorch Lightning Minio Callback

Callback prepared to log checkpoints and tensorboard data to minio server.

## Quick Start Example

This example program connects to an S3-compatible object storage server, make a bucket on that server, and upload a file
to the bucket.

You need the following items to connect to an S3-compatible object storage server:

| Parameters              | Description                                                   |
|-------------------------|---------------------------------------------------------------|
| save_dir                | Directory to save models in.                                  |
| name                    | Sub-directory to save models in.                              |
| upload_models           | Whether to upload the checkpoints or not                      |
| upload_hparams          | Whether to upload the hparams or not                          |
| upload_tensorboard_data | Whether to upload tensorboard data  or not                    |
| bucket                  | Name of the bucket where data will be stored                  |
| endpoint                | URL to minio service.                                         |
| endpoint                | URL to minio service.                                         |
| access_key              | Access key (aka user ID) of an account in the minio service.  |
| secret_key              | Secret key (aka password) of an account in the minio service. |
| secure                  | Whether endpoint uses https or not.                           |
| secure                  | Whether endpoint uses https or not.                           |

Files will be saved in the with the following format
```
    <save_dir>/<name>/version_x/checkpoints_and_tensorboard_data
```
They will also be uploaded to minio:
```
    <bucket>/<save_dir>/<name>/version_x/checkpoints_and_tensorboard_data
```
### Usage

```py
...
from src.pl_minio_callback.minio_callback import MinioCallback

...
if __name__ == "__main__":
    ...
    logger = TensorBoardLogger(save_dir="models", name="cifar10_resnet")  # Check parameters
    trainer = pl.Trainer(
        callbacks=[
            MinioCallback(
                upload_tensorboard_data=False,
                upload_hparams=False,
                upload_checkpoints=True,
                bucket="tensorboard",
                endpoint="localhost:9000",
                access_key="minio",
                secret_key="minio123",
                secure=False
            )
        ],
        log_every_n_steps=5,
        checkpoint_callback=True,
        logger=logger,
        max_epochs=10,
        gpus=1,
        auto_select_gpus=True
    )
    ...

```
