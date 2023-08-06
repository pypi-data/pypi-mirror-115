import numpy as np

from classicML import _cml_precision
from classicML import CLASSICML_LOGGER
from classicML.api.models import BaseModel
from classicML.backend import get_within_class_scatter_matrix
from classicML.backend import get_w


class LinearDiscriminantAnalysis(BaseModel):
    """线性判别分析.

    Attributes:
        w: numpy.ndarray, 投影向量.
        mu_0: numpy.ndarray, 反例的均值.
        mu_1: numpy.ndarray, 正例的均值.
        is_trained: bool, default=False,
            模型训练后将被标记为True.
        is_loaded: bool, default=False,
            如果模型加载了权重将被标记为True.
    """
    def __init__(self):
        super(LinearDiscriminantAnalysis, self).__init__()
        self.w = None
        self.mu_0 = None
        self.mu_1 = None
        self.is_trained = False
        self.is_loaded = False

    def fit(self, x, y, **kwargs):
        """训练模型.

        Arguments:
            x: numpy.ndarray, array-like, 特征数据.
            y: numpy.ndarray, array-like, 标签.

        Returns:
            LDA实例.
        """
        x = np.asarray(x, dtype=_cml_precision.float)
        y = np.asarray(y, dtype=_cml_precision.int)

        X_0 = x[y == 0]
        X_1 = x[y == 1]

        self.mu_0 = np.mean(X_0, axis=0, keepdims=True)
        self.mu_1 = np.mean(X_1, axis=0, keepdims=True)

        # 获得类内散度矩阵
        S_w = get_within_class_scatter_matrix(X_0, X_1, self.mu_0, self.mu_1)
        # 获得投影向量
        self.w = get_w(S_w, self.mu_0, self.mu_1)
        # 标记训练完成
        self.is_trained = True

        return self

    def predict(self, x, **kwargs):
        """模型进行预测.

        Arguments:
            x: numpy.ndarray, array-like, 特征数据.

        Returns:
            LDA预测的标签张量.

        Raises:
            ValueError: 模型没有训练的错误.
        """
        if self.is_trained is False and self.is_loaded is False:
            CLASSICML_LOGGER.error('模型没有权重')
            raise ValueError('你必须先进行训练')

        coord = np.dot(x, self.w.T).astype(_cml_precision.float)

        center_0 = np.dot(self.w, self.mu_0.T)
        center_1 = np.dot(self.w, self.mu_1.T)

        y_pred = np.abs(coord - center_0) > np.abs(coord - center_1)
        y_pred = np.squeeze(y_pred)
        y_pred = y_pred.astype(_cml_precision.int)

        return y_pred
