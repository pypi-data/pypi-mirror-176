# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/common.base_recurrent.ipynb.

# %% auto 0
__all__ = ['BaseRecurrent']

# %% ../../nbs/common.base_recurrent.ipynb 5
import random

import numpy as np
import torch
import torch.nn as nn
import pytorch_lightning as pl
from pytorch_lightning.callbacks import TQDMProgressBar

from ._scalers import TemporalNorm
from ..tsdataset import TimeSeriesDataModule

# %% ../../nbs/common.base_recurrent.ipynb 6
class BaseRecurrent(pl.LightningModule):
    
    def __init__(self,
                 h,
                 input_size,
                 loss,
                 learning_rate,
                 batch_size=32,
                 scaler_type='robust',
                 futr_exog_list=None,
                 hist_exog_list=None,
                 stat_exog_list=None,
                 num_workers_loader=0,
                 drop_last_loader=False,
                 random_seed=1, 
                 **trainer_kwargs):
        super(BaseRecurrent, self).__init__()

        self.save_hyperparameters() # Allows instantiation from a checkpoint from class
        self.random_seed = random_seed
        pl.seed_everything(self.random_seed, workers=True)

        # Padder to complete train windows, 
        # example y=[1,2,3,4,5] h=3 -> last y_output = [5,0,0]
        self.h = h
        self.input_size = input_size
        self.padder = nn.ConstantPad1d(padding=(0, self.h), value=0)

        # Loss
        self.loss = loss
        self.learning_rate = learning_rate

        # Scaler
        if scaler_type is None:
            self.scaler = None
        else:
            self.scaler = TemporalNorm(scaler_type=scaler_type, dim=-1) # Time dimension is -1.

        # Variables
        self.futr_exog_list = futr_exog_list if futr_exog_list is not None else []
        self.hist_exog_list = hist_exog_list if hist_exog_list is not None else []
        self.stat_exog_list = stat_exog_list if stat_exog_list is not None else []

        # Fit arguments
        self.val_size = 0
        self.test_size = 0

        # Trainer
        # we need to instantiate the trainer each time we want to use it
        self.trainer_kwargs = {**trainer_kwargs}
        if self.trainer_kwargs.get('callbacks', None) is None:
            self.trainer_kwargs = {**{'callbacks': [TQDMProgressBar()], **trainer_kwargs}}
        else:
            self.trainer_kwargs = trainer_kwargs

        # Add GPU accelerator if available
        if self.trainer_kwargs.get('accelerator', None) is None:
            if torch.cuda.is_available():
                self.trainer_kwargs['accelerator'] = "gpu"
        if self.trainer_kwargs.get('devices', None) is None:
            if torch.cuda.is_available():
                self.trainer_kwargs['devices'] = -1

        # Avoid saturating local memory, disabled fit model checkpoints
        if self.trainer_kwargs.get('enable_checkpointing', None) is None:
           self.trainer_kwargs['enable_checkpointing'] = False

        # DataModule arguments
        self.batch_size = batch_size
        self.num_workers_loader = num_workers_loader
        self.drop_last_loader = drop_last_loader

    def on_fit_start(self):
        torch.manual_seed(self.random_seed)
        np.random.seed(self.random_seed)
        random.seed(self.random_seed)
        
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)

    def _normalization(self, batch, val_size=0, test_size=0):

        temporal = batch['temporal'] # B, C, T
        temporal_cols = batch['temporal_cols'].copy()

        # Separate data and mask
        temporal_data_cols = temporal_cols.drop('available_mask').tolist()
        temporal_data = temporal[:, temporal_cols.get_indexer(temporal_data_cols), :]
        temporal_mask = temporal[:, temporal_cols.get_loc('available_mask'), :].clone()

        # Remove validation and test set to prevent leakeage
        if val_size + test_size > 0:
            cutoff = val_size + test_size
            temporal_mask[:, -cutoff:] = 0

        # Normalize. self.scaler stores the shift and scale for inverse transform
        temporal_mask = temporal_mask.unsqueeze(1) # Add channel dimension for scaler.transform.
        temporal_data = self.scaler.transform(x=temporal_data, mask=temporal_mask)

        # Replace values in windows dict
        temporal[:, temporal_cols.get_indexer(temporal_data_cols), :] = temporal_data
        batch['temporal'] = temporal
        
        return batch

    def _inv_normalization(self, y_hat, temporal_cols):
        # Receives window predictions [B, seq_len, H, output]
        # Broadcasts outputs and inverts normalization

        # Get 'y' scale and shift, and add W dimension
        temporal_data_cols = temporal_cols.drop('available_mask')
        y_scale = self.scaler.x_scale[:, temporal_data_cols.get_indexer(['y']), 0].flatten() #[B,C,T] -> [B]
        y_shift = self.scaler.x_shift[:, temporal_data_cols.get_indexer(['y']), 0].flatten() #[B,C,T] -> [B]

        y_scale = y_scale[:,None,None,None] * torch.ones_like(y_hat) # [B,1,1,1] -> [B,seq_len,H,output]
        y_shift = y_shift[:,None,None,None] * torch.ones_like(y_hat) # [B,1,1,1] -> [B,seq_len,H,output]

        y_hat = self.scaler.inverse_transform(z=y_hat, x_scale=y_scale, x_shift=y_shift)

        return y_hat

    def _create_windows(self, batch, step):
        temporal = batch['temporal']
        temporal_cols = batch['temporal_cols']

        if step == 'train':
            if self.val_size + self.test_size > 0:
                cutoff = -self.val_size - self.test_size
                temporal = temporal[:, :, :cutoff]
            temporal = self.padder(temporal)

            # Truncate batch to shorter time-series 
            av_condition = torch.nonzero(torch.min(temporal[:, temporal_cols.get_loc('available_mask')], axis=0).values)
            min_time_stamp = int(av_condition.min())
            
            available_ts = temporal.shape[-1] - min_time_stamp + 1 # +1, inclusive counting
            if available_ts < 1 + self.h:
                raise Exception(
                    'Time series too short for given input and output size. \n'
                    f'Available timestamps: {available_ts}'
                )

            temporal = temporal[:, :, min_time_stamp:]

        if step == 'val':
            if self.test_size > 0:
                temporal = temporal[:, :, :-self.test_size]
            temporal = self.padder(temporal)

        if step == 'predict':
            if (self.test_size == 0) and (len(self.futr_exog_list)==0):
                temporal = self.padder(temporal)

        # Parse batch
        window_size = 1 + self.h # 1 for current t and h for future
        windows = temporal.unfold(dimension=-1,
                                  size=window_size,
                                  step=1)

        # Truncated backprogatation during training (shorten sequence where RNNs unroll)
        n_windows = windows.shape[2]
        if (step == 'train') and (self.input_size > 0) and (n_windows > self.input_size):
            max_sampleable_time = n_windows-self.input_size+1
            start = np.random.choice(max_sampleable_time)
            windows = windows[:, :, start:(start+self.input_size), :]

        # [B, C, input_size, 1+H]
        windows_batch = dict(temporal=windows,
                             temporal_cols=temporal_cols,
                             static=batch.get('static', None),
                             static_cols=batch.get('static_cols', None))

        return windows_batch

    def _parse_windows(self, batch, windows):
        # [B, C, seq_len, 1+H]
        # Filter insample lags from outsample horizon
        y_idx = batch['temporal_cols'].get_loc('y')
        mask_idx = batch['temporal_cols'].get_loc('available_mask')
        insample_y = windows['temporal'][:, y_idx, :, :-self.h]
        insample_mask = windows['temporal'][:, mask_idx, :, :-self.h]
        outsample_y = windows['temporal'][:, y_idx, :, -self.h:]
        outsample_mask = windows['temporal'][:, mask_idx, :, -self.h:]

        # Filter historic exogenous variables
        if len(self.hist_exog_list):
            hist_exog_idx = windows['temporal_cols'].get_indexer(self.hist_exog_list)
            hist_exog = windows['temporal'][:, hist_exog_idx, :, :-self.h]
        else:
            hist_exog = None
        
        # Filter future exogenous variables
        if len(self.futr_exog_list):
            futr_exog_idx = windows['temporal_cols'].get_indexer(self.futr_exog_list)
            futr_exog = windows['temporal'][:, futr_exog_idx, :, :]
        else:
            futr_exog = None
        # Filter static variables
        if len(self.stat_exog_list):
            static_idx = windows['static_cols'].get_indexer(self.stat_exog_list)
            stat_exog = windows['static'][:, static_idx]
        else:
            stat_exog = None

        return insample_y, insample_mask, outsample_y, outsample_mask, \
               hist_exog, futr_exog, stat_exog

    def training_step(self, batch, batch_idx):
        # Normalize
        if self.scaler is not None:
            batch = self._normalization(batch, val_size=self.val_size, test_size=self.test_size)

        # Create windows
        windows = self._create_windows(batch, step='train')

        # Parse windows
        insample_y, insample_mask, outsample_y, outsample_mask, \
               hist_exog, futr_exog, stat_exog = self._parse_windows(batch, windows)

        windows_batch = dict(insample_y=insample_y, # [B, seq_len, 1]
                             insample_mask=insample_mask, # [B, seq_len, 1]
                             futr_exog=futr_exog, # [B, F, seq_len, 1+H]
                             hist_exog=hist_exog, # [B, C, seq_len]
                             stat_exog=stat_exog) # [B, S]

        y_hat = self(windows_batch) # [B, seq_len, H, output]

        # Remove last y_hat dimension if unidimensional loss (for MAE, RMSE, etc.)
        if y_hat.shape[-1] == 1:
            y_hat = y_hat.squeeze(-1)

        loss = self.loss(y=outsample_y, y_hat=y_hat, mask=outsample_mask)
        self.log('train_loss', loss, batch_size=self.batch_size, prog_bar=True, on_epoch=True)
        return loss

    def validation_step(self, batch, batch_idx):
        if self.val_size == 0:
            return np.nan

        # Normalize
        if self.scaler is not None:
            batch = self._normalization(batch, val_size=self.val_size, test_size=self.test_size)

        # Create windows
        windows = self._create_windows(batch, step='val')

        # Parse windows
        insample_y, insample_mask, outsample_y, outsample_mask, \
               hist_exog, futr_exog, stat_exog = self._parse_windows(batch, windows)

        windows_batch = dict(insample_y=insample_y, # [B, seq_len, 1]
                             insample_mask=insample_mask, # [B, seq_len, 1]
                             futr_exog=futr_exog, # [B, F, seq_len, 1+H]
                             hist_exog=hist_exog, # [B, C, seq_len]
                             stat_exog=stat_exog) # [B, S]

        y_hat = self(windows_batch) # [B, seq_len, H, output]

        # Remove train y_hat (+1 and -1 for padded last window with zeros)
        val_windows = (self.val_size) + 1
        y_hat = y_hat[:, -val_windows:-1, :, :]
        outsample_y = outsample_y[:, -val_windows:-1, :]
        outsample_mask = outsample_mask[:, -val_windows:-1, :]

        # Remove last y_hat dimension if unidimensional loss (for MAE, RMSE, etc.)
        if y_hat.shape[-1] == 1:
            y_hat = y_hat.squeeze(-1)

        loss = self.loss(y=outsample_y, y_hat=y_hat, mask=outsample_mask)
        self.log('val_loss', loss, batch_size=self.batch_size, prog_bar=True, on_epoch=True)

        return loss

    def validation_epoch_end(self, outputs):
        if self.val_size == 0:
            return
        avg_loss = torch.stack(outputs).mean()
        self.log("ptl/val_loss", avg_loss, batch_size=self.batch_size)

    def predict_step(self, batch, batch_idx):
        # Normalize
        if self.scaler is not None:
            batch = self._normalization(batch, val_size=0, test_size=self.test_size)

        windows = self._create_windows(batch, step='predict')

        # Parse windows
        insample_y, insample_mask, _, _, \
               hist_exog, futr_exog, stat_exog = self._parse_windows(batch, windows)

        windows_batch = dict(insample_y=insample_y, # [B, seq_len, 1]
                             insample_mask=insample_mask, # [B, seq_len, 1]
                             futr_exog=futr_exog, # [B, F, seq_len, 1+H]
                             hist_exog=hist_exog, # [B, C, seq_len]
                             stat_exog=stat_exog) # [B, S]

        y_hat = self(windows_batch) # [B, seq_len, H, output]

        # Inv Normalize
        if self.scaler is not None:
            y_hat = self._inv_normalization(y_hat=y_hat,
                                            temporal_cols=batch['temporal_cols'])

        return y_hat

    def fit(self, dataset, val_size=0, test_size=0):
        """ Fit.

        The `fit` method, optimizes the neural network's weights using the
        initialization parameters (`learning_rate`, `batch_size`, ...)
        and the `loss` function as defined during the initialization. 
        Within `fit` we use a PyTorch Lightning `Trainer` that
        inherits the initialization's `self.trainer_kwargs`, to customize
        its inputs, see [PL's trainer arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).

        The method is designed to be compatible with SKLearn-like classes
        and in particular to be compatible with the StatsForecast library.

        By default the `model` is not saving training checkpoints to protect 
        disk memory, to get them change `enable_checkpointing=True` in `__init__`.        

        **Parameters:**<br>
        `dataset`: NeuralForecast's `TimeSeriesDataset`, see [documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).<br>
        `val_size`: int, validation size for temporal cross-validation.<br>
        `test_size`: int, test size for temporal cross-validation.<br>
        """
        self.val_size = val_size
        self.test_size = test_size
        datamodule = TimeSeriesDataModule(
            dataset, 
            batch_size=self.batch_size,
            num_workers=self.num_workers_loader,
            drop_last=self.drop_last_loader
        )
        trainer = pl.Trainer(**self.trainer_kwargs)
        trainer.fit(self, datamodule=datamodule)

    def predict(self, dataset, step_size=1, **data_module_kwargs):
        """ Predict.

        Neural network prediction with PL's `Trainer` execution of `predict_step`.

        **Parameters:**<br>
        `dataset`: NeuralForecast's `TimeSeriesDataset`, see [documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).<br>
        `step_size`: int=1, Step size between each window.<br>
        `**data_module_kwargs`: PL's TimeSeriesDataModule args, see [documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).
        """
        if step_size > 1:
            raise Exception('Recurrent models do not support step_size > 1')

        # fcsts (window, batch, h)
        trainer = pl.Trainer(**self.trainer_kwargs)
        datamodule = TimeSeriesDataModule(
            dataset,
            num_workers=self.num_workers_loader,
            **data_module_kwargs
        )
        fcsts = trainer.predict(self, datamodule=datamodule)
        if self.test_size > 0:
            # Remove warmup windows (from train and validation)
            fcsts = torch.vstack([fcst[:, -(1+self.test_size-self.h):,:,:] for fcst in fcsts])
            fcsts = fcsts.numpy().flatten()
            fcsts = fcsts.reshape(-1, self.loss.outputsize_multiplier)
        else:
            fcsts = torch.vstack([fcst[:,-1:,:,:] for fcst in fcsts]).numpy().flatten()
            fcsts = fcsts.reshape(-1, self.loss.outputsize_multiplier)

        return fcsts

    def set_test_size(self, test_size):
        self.test_size = test_size

    def save(self, path):
        """ BaseRecurrent.save

        Save the fitted model to disk.

        **Parameters:**<br>
        `path`: str, path to save the model.<br>
        """
        self.trainer.save_checkpoint(path)
