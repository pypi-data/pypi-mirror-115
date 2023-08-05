# -*-coding: utf-8 -*-
"""
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2021-07-28 14:57:10
"""
import os
from ..callbacks.callbacks import Callback
from ..utils import summary
from ..utils import log, file_utils
from ..engine import comm


class LogHistory(Callback):
    def __init__(self, log_dir, log_freq=1, logger=None, is_main_process=True):
        """
        Tensorboard,Log等summary记录信息
        :param log_dir:Log输出日志保存目录
        :param log_freq:Log打印频率
        :param logger:Log实例对象，如果logger=None，则会初始化新的Log实例对象
        :param is_main_process: 是否是主进程，仅当在主进程中才会打印Log信息
        """
        super().__init__()
        if not comm.is_main_process(): return
        self.log_dir = log_dir
        self.log_freq = log_freq
        self.is_main_process = is_main_process
        # Log实例对象
        file_utils.create_dir(self.log_dir)
        self.logfile = os.path.join(self.log_dir, "log.yaml")
        self.logger = log.set_logger(logfile=self.logfile) if logger is None else logger
        # 初始化Tensorboard
        self.writer = summary.SummaryWriter(log_dir=self.log_dir if self.is_main_process else None)

    def on_batch_end(self, batch, logs: dict = {}):
        if not comm.is_main_process(): return
        if batch % self.log_freq == 0 or batch == 0:
            info = dict(logs)
            info.pop("test") if "test" in logs else info
            self.logger.info(info)

    def on_epoch_end(self, epoch, logs: dict = {}):
        if not comm.is_main_process(): return
        if "train" in logs:
            info = logs["train"]
            self.writer.add_scalar("Train_Loss_epoch", info['loss'], epoch)
            self.writer.add_scalar("Train_Acc_epoch", info['acc'], epoch)
            self.writer.add_scalar("lr_epoch", logs["lr"], epoch)
            self.logger.info({"train": info})

        if "test" in logs:
            info = logs["test"]
            self.writer.add_scalar("Test_Loss_epoch", info['loss'], epoch)
            self.writer.add_scalar("Test_Acc_epoch", info['acc'], epoch)
            self.logger.info({"test": info})
