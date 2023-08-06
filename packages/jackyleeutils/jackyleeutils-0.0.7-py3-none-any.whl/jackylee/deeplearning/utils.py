import torch
from d2l import torch as d2l
import logging
from torch import nn

# 设备相关


def get_device():
    return 'cuda' if torch.cuda.is_available() else 'cpu'


def try_gpu(i=0):  # @save
    """如果存在，则返回gpu(i)，否则返回cpu()"""
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')

# 模型相关


def check_model_device(model):  # 测试模型在cpu还是gpu
    return next(model.parameters()).device


def check_model_params(model, device):
    X_test = torch.randn(size=(8, 3, 224, 224))
    X_test = X_test.to(device)
    for blk in model:
        X_test = blk(X_test)
        print(blk.__class__.__name__, 'output shape:\t', X_test.shape)


def accuracy(y_hat, y):  # @save
    """计算预测正确的数量"""
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    cmp = y_hat.type(y.dtype) == y  # 将
    return float(cmp.type(y.dtype).sum())


# 定义累加器类
class Accumulator:
    """For accumulating sums over `n` variables."""

    def __init__(self, n):
        self.data = [0.0] * n

    def add(self, *args):
        self.data = [a + float(b) for a, b in zip(self.data, args)]

    def reset(self):
        self.data = [0.0] * len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


# 日志相关


def logger_config(log_name, file_name):
    # 记录器
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    # 必须设置为两个handler中级别更低的

    # 处理器handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # 没有给handler指定日志级别，将使用logger的级别
    fileHandler = logging.FileHandler(filename=file_name, encoding='utf-8')
    consoleHandler.setLevel(logging.INFO)

    # formatter格式
    formatter = logging.Formatter(
        fmt="[%(asctime)s] - %(levelname)-8s - %(filename)s - %(lineno)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S %p"
    )

    # 给处理器设置格式
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 记录器要设置处理器
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    # 定义一个过滤器
    flt = logging.Filter("jacky")

    # 关联过滤器
    # logger.addFilter(flt)
    # fileHandler.addFilter(flt)

    return logger
