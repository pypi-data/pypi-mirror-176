import torch
from d2l import torch as d2l
import logging
from torch import nn
from tqdm import tqdm

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
# 训练函数


def train_valid(net,
                train_loader,
                valid_loader,
                test_loader,
                num_epochs,
                loss_func,
                optimizer,
                device,
                logger=None,
                ):
    # 初始化
    logger.info('开始训练')

    def init_weights(m):
        if type(m) == nn.Linear or type(m) == nn.Conv2d:
            nn.init.xavier_uniform_(m.weight)
    net.apply(init_weights)
    net.to(device)

    for epoch in range(num_epochs):
        print(f'----------第{epoch+1:2d}轮')
        # 训练模式
        metric_train = Accumulator(3)
        net.train()
        for X, y in tqdm(iter(train_loader), desc=f'训练'):
            X = X.to(device)
            y = y.to(device)

            y_hat = net(X)
            loss = loss_func(y_hat, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                metric_train.add(
                    loss * X.shape[0], accuracy(y_hat, y), X.shape[0])
            # 记录准确性
        train_loss = metric_train[0] / metric_train[2]
        train_acc = metric_train[1] / metric_train[2]

        # 验证模式
        metric_valid = Accumulator(2)
        net.eval()
        for X, y in tqdm(iter(valid_loader), desc=f'验证'):
            X = X.to(device)
            y = y.to(device)

            y_hat = net(X)
            loss = loss_func(y_hat, y)

            with torch.no_grad():
                metric_valid.add(accuracy(y_hat, y), X.shape[0])
        valid_acc = metric_valid[0] / metric_valid[1]

        logger.info(
            f'epoch: {epoch+1:2d} - train_loss: {train_loss:.5f} - train_acc: {train_acc:.5f} - valid_acc: {valid_acc:.5f}')

    logger.info('结束训练')
    
    # 测试模式
    metric_test = Accumulator(2)
    net.eval()
    for X, y in tqdm(iter(test_loader), desc=f'测试'):
        X = X.to(device)
        y = y.to(device)

        y_hat = net(X)
        loss = loss_func(y_hat, y)

        with torch.no_grad():
            metric_test.add(accuracy(y_hat, y), X.shape[0])
    test_acc = metric_test[0] / metric_test[1]

    logger.info( f'测试 - test_acc: {test_acc:.5f}')

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
