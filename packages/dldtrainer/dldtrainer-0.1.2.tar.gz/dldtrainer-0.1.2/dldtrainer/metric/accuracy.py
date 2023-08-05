# -*-coding: utf-8 -*-
"""
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2021-07-28 11:32:42
"""
import numpy as np
import torch
from sklearn.metrics import accuracy_score
from .eval_tools.metrics import AverageMeter, accuracy
from ..callbacks import callbacks
from .eval_tools import classification_report


class Accuracy(callbacks.Callback):
    def __init__(self, target_names=None):
        """
        计算Accuracy的回调函数
        :param target_names: list of str of shape (n_labels,), default=None
                             Optional display names matching the labels (same order).
        """
        super(Accuracy, self).__init__()
        self.target_names = target_names
        self.train_losses = AverageMeter()
        self.train_top1 = AverageMeter()
        self.test_losses = AverageMeter()
        self.test_top1 = AverageMeter()
        self.true_labels = np.ones(0)
        self.pred_labels = np.ones(0)

    def on_test_begin(self, logs: dict = {}):
        self.train_losses.reset()
        self.train_top1.reset()
        self.test_losses.reset()
        self.test_top1.reset()
        self.true_labels = np.ones(0)
        self.pred_labels = np.ones(0)

    def on_test_end(self, logs: dict = {}):
        acc = accuracy_score(self.true_labels, self.pred_labels) * 100.0
        report = classification_report.get_classification_report(self.true_labels,
                                                                 self.pred_labels,
                                                                 target_names=self.target_names)
        # confuse_file = os.path.join(self.log_root, "confusion_matrix.csv")
        # conf_matrix = classification_report.get_confusion_matrix(true_labels, pred_labels, None, confuse_file)
        print("\nAcc:{:.4f}\n{}".format(acc, report))

    def on_train_summary(self, inputs, outputs, losses, epoch, step, logs: dict = {}):
        # measure accuracy and record loss
        targets, labels = inputs
        acc, = accuracy(outputs.data, labels, topk=(1,))
        self.train_losses.update(losses.data.item(), labels.size(0))
        self.train_top1.update(acc.data.item(), labels.size(0))
        logs["train"] = {
            'loss': self.train_losses.avg,
            'acc': self.train_top1.avg
        }

    def on_test_summary(self, inputs, outputs, losses, epoch, batch, logs: dict = {}):
        # measure accuracy and record loss
        targets, labels = inputs
        acc, = accuracy(outputs.data, labels, topk=(1,))
        self.test_losses.update(losses.data.item(), labels.size(0))
        self.test_top1.update(acc.data.item(), labels.size(0))
        logs["test"] = {
            'loss': self.test_losses.avg,
            'acc': self.test_top1.avg
        }
        # get predict result
        outputs = torch.nn.functional.softmax(outputs, dim=1)
        pred_score, pred_index = torch.max(outputs, dim=1)
        pred_index = pred_index.cpu().detach().numpy()
        labels = labels.cpu().detach().numpy()
        self.true_labels = np.hstack([self.true_labels, labels])
        self.pred_labels = np.hstack([self.pred_labels, pred_index])
