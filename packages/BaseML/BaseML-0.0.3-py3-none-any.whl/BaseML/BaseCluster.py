import os
import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch

from sklearn.metrics import silhouette_score

from sklearn.model_selection import train_test_split
from .base import baseml


class Cluster(baseml):  # cluster
    """BaseML中的聚类模块,包含['Kmeans', 'Spectral clustering', 'Agglomerative clustering',
       'Birch']聚类算法.

    Attributes:
        algorithm: 算法名称
        model: 实例化的模型
    """

    def __init__(self, algorithm='Kmeans', N_CLUSTERS = 5, params = {}):
        """clt类初始化

        Args:
            algorithm (str, optional): 采用的聚类算法. Defaults to 'Kmeans'.
            N_CLUSTERS (int, optional): 聚类个数. Defaults to 5.
            params (dict, optional): 参数字典,可自定义参数放入,参数名称详见sklearn官方文档. Defaults to {}.
        """
        super(Cluster,self).__init__()   # 继承父类的构造方法
        self.algorithm = algorithm
        self.n = N_CLUSTERS

        if self.algorithm == 'Kmeans':
            if len(params) > 1:
                self.model = KMeans(**params)
            else:
                self.model = KMeans(n_clusters = N_CLUSTERS)
        elif self.algorithm == 'Spectral clustering':
            if len(params) > 1:
                self.model = SpectralClustering(**params)
            else:
                self.model = SpectralClustering(n_clusters = N_CLUSTERS)
        elif self.algorithm == 'Agglomerative clustering':
            if len(params) > 1:
                self.model = AgglomerativeClustering(**params)
            else:
                self.model = AgglomerativeClustering(n_clusters = N_CLUSTERS)
        elif self.algorithm == 'Birch':
            if len(params) > 1:
                self.model = Birch(**params)
            else:
                self.model = Birch(n_clusters = N_CLUSTERS)



    def train(self, validate = True):
        """训练模型.

        Args:
            validate (bool, optional): 是否需要验证模型，并输出模型轮廓系数. Defaults to True.
        """

        self.model.fit(self.x_train)

        if validate:
            score = silhouette_score(self.x_train, labels = self.model.labels_)
            print('轮廓系数为：{}'.format(score))   # -1为不正确的聚类，0为重叠聚类，1为正确的聚类



    def inference(self, data = np.nan, verbose = True):
        """使用模型进行推理

        Args:
            data (numpy, optional): 放进来推理的数据,不填默认使用self.x_train.
            verbose (bool, optional): 是否输出推理中的中间结果. Defaults to True.

        Returns:
            pred: 返回预测结果.
        """
        if data is not np.nan: # 对data进行了指定
            self.x_test = data
        else:
            self.x_test = self.x_train

        if verbose and len(self.x_train) != 0:
            labels = self.model.labels_      # 获取聚类标签
            print(silhouette_score(self.x_train, labels))      # 获取聚类结果总的轮廓系数
            print(self.model.cluster_centers_)	# 输出类簇中心
            for i in range(self.n):
                print(f" CLUSTER-{i+1} ".center(60, '='))
                print(self.x_train[labels == i])

        if self.x_test is not []:
            pred = self.model.predict(self.x_test)
            return pred
