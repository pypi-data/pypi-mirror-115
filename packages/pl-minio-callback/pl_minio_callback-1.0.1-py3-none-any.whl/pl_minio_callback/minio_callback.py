import os

from pytorch_lightning.callbacks import ModelCheckpoint

from .minio_util import MinioUtil


class MinioCallback(ModelCheckpoint):
    def __init__(self, upload_tensorboard_data=True, upload_hparams=True, upload_checkpoints=True, bucket="test",
                 endpoint="localhost:9000",
                 access_key=None, secret_key=None, session_token=None, secure=True, region=None, http_client=None,
                 credentials=None, *args, **kwargs):

        assert upload_checkpoints or upload_hparams or upload_tensorboard_data, \
            "All upload params set to False in MinioCallback "

        super().__init__(*args, **kwargs)
        self.minio = \
            MinioUtil(bucket, endpoint, access_key, secret_key, session_token, secure, region, http_client, credentials)
        self.upload_tensorboard_data = upload_tensorboard_data
        self.upload_hparams = upload_hparams
        self.upload_checkpoints = upload_checkpoints

    def on_train_start(self, trainer, pl_module):
        super(MinioCallback, self).on_train_start(trainer, pl_module)
        self._save_hparams(trainer)

    def on_train_epoch_end(self, trainer, pl_module, unused=None):
        super(MinioCallback, self).on_train_epoch_end(trainer, pl_module, unused)
        self._save_tensorboard(trainer)

    def on_validation_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx):
        super(MinioCallback, self) \
            .on_validation_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)
        self._save_tensorboard(trainer)

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx):
        super(MinioCallback, self) \
            .on_train_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)
        if batch_idx == 0 or batch_idx % trainer.log_every_n_steps == 0:
            self._save_tensorboard(trainer)

    def _save_hparams(self, trainer):
        if self.upload_hparams:
            h_params_file = os.path.join(trainer.log_dir, trainer.logger.NAME_HPARAMS_FILE)
            self.minio.upload_file(h_params_file, h_params_file)

    def _save_tensorboard(self, trainer):
        if self.upload_tensorboard_data:
            tensorboard_file = trainer.logger.experiment.file_writer.event_writer._file_name
            self.minio.upload_file(tensorboard_file, tensorboard_file)

    def _save_model(self, trainer, model_file):
        super()._save_model(trainer, model_file)
        if self.upload_checkpoints:
            self.minio.upload_file(model_file, model_file)

    def _del_model(self, trainer, filepath):
        if trainer.should_rank_save_checkpoint and self._fs.exists(filepath):
            self._fs.rm(filepath)
            self.minio.minio_utils(filepath)
