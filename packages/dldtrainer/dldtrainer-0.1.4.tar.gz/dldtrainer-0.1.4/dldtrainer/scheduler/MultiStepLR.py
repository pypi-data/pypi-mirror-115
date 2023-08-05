# -*-coding: utf-8 -*-
"""
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2021-07-28 15:32:44
"""

import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
from ..callbacks.callbacks import Callback


class MultiStepLR(Callback):
    def __init__(self,
                 optimizer,
                 epochs,
                 nums_steps,
                 milestones,
                 lr_init=0.01,
                 nums_warn_up=0,
                 decay_rates=None):
        """
        a cosine decay scheduler about steps, not epochs.
        :param optimizer: ex. optim.SGD
        :param epochs:
        :param nums_steps: 一个epoch的迭代次数，len(self.train_dataloader)
        :param lr_min : lr_min
        :param lr_init: lr_max is init lr.
        :param nums_warn_up:
        """
        self.optimizer = optimizer
        self.epochs = epochs
        self.nums_steps = nums_steps
        self.max_step = epochs * self.nums_steps
        self.lr_init = lr_init
        self.milestones = milestones
        self.warmup = nums_warn_up * self.nums_steps
        if decay_rates:
            lr_list = [lr_init * decay for decay in decay_rates]
        else:
            lr_list = [lr_init * 0.1 ** decay for decay in range(0, len(self.milestones) + 1)]
        self.lr_list = lr_list
        self.epoch = 0
        super(MultiStepLR, self).__init__()

    def __get_lr(self, epoch, lr_stages, lr_list):
        """
        :param epoch:
        :param lr_stages:
        :param lr_list:
        :return:
        """
        lr = None
        max_stages = 0
        if not lr_stages:
            lr = lr_list[0]
        else:
            max_stages = max(lr_stages)
        for index in range(len(lr_stages)):
            if epoch < lr_stages[index]:
                lr = lr_list[index]
                break
            if epoch >= max_stages:
                lr = lr_list[index + 1]
        return lr

    def __set_stages_lr(self, epoch, lr_stages, lr_list):
        '''
        :param epoch:
        :param lr_stages: [    35, 65, 95, 150]
        :param lr_list:   [0.1, 0.01, 0.001, 0.0001, 0.00001]
        :return:
        '''
        lr = self.__get_lr(epoch, lr_stages, lr_list)
        if lr:
            self.__set_lr(lr)

    def __set_lr(self, lr):
        for param_group in self.optimizer.param_groups:
            param_group["lr"] = lr

    def set_lr(self, epoch, total_step):
        """
        Usage:
        for epoch in range(epochs):
            for i in range(steps_per_epoch):
                scheduler.on_step(steps_per_epoch * epoch + i)
                ...
        :param total_step: total step: steps_per_epoch * epoch + step
        :return:
        """
        if self.warmup and total_step <= self.warmup:
            lr = self.lr_init / self.warmup * total_step
            self.__set_lr(lr)
        else:
            self.__set_stages_lr(epoch, self.milestones, self.lr_list)

    def on_epoch_begin(self, epoch, logs: dict = {}):
        self.epoch = epoch

    def on_batch_end(self, batch, logs: dict = {}):
        self.step(epoch=self.epoch, step=batch)

    def step(self, epoch=0, step=0):
        total_step = self.nums_steps * epoch + step
        self.set_lr(epoch, total_step)
