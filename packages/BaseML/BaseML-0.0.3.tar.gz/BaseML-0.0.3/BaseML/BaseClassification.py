
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn
from sklearn.metrics import accuracy_score, mean_squared_error, precision_score, recall_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import silhouette_score, silhouette_samples
import joblib
import cv2
import random
from skimage.feature import hog
from .base import baseml

class Classification(baseml):
    """BaseML中的分类模块,包含['KNN', 'SVM', 'NaiveBayes', 'CART', 'AdaBoost', 'MLP', 
       'RandomForest']分类算法.

    Attributes:
        algorithm: 算法名称
        model: 实例化的模型
    """

    def __init__(self, algorithm='KNN', n_neighbors=5, n_estimators=100, n_hidden = (100,), params = {}):
        """cls类初始化.

        Args:
            algorithm (str, optional): 采用的分类算法. Defaults to 'KNN'.
            n_neighbors (int, optional): KNN的k值. Defaults to 5.
            n_estimators (int, optional): Adaboost|RandomForest所集成的决策树个数. Defaults to 100.
            n_hidden (tuple, optional): MLP隐藏层的形状. Defaults to (100,).
            params (dict, optional): 参数字典,可自定义参数放入,参数名称详见sklearn官方文档. Defaults to {}.
        """
        super(Classification,self).__init__()   # 继承父类的构造方法
        self.algorithm = algorithm

        if self.algorithm == 'KNN':
            if len(params) > 1:
                self.model = KNeighborsClassifier(**params)
            else:
                self.model = KNeighborsClassifier(n_neighbors=n_neighbors)
        elif self.algorithm == 'SVM':
            if len(params) > 1:
                self.model = SVC(**params)
            else:
                self.model = SVC()
        elif self.algorithm == 'NaiveBayes':
            if len(params) > 1:
                self.model = GaussianNB(**params)
            else:
                self.model = GaussianNB()
        elif self.algorithm == 'CART':
            if len(params) > 1:
                self.model = DecisionTreeClassifier(**params)
            else:
                self.model = DecisionTreeClassifier()
        elif self.algorithm == 'AdaBoost':
            if len(params) > 1:
                self.model = AdaBoostClassifier(**params)
            else:
                self.model = AdaBoostClassifier(n_estimators=n_estimators, random_state=0)

        elif self.algorithm == 'MLP':
            if len(params) > 1:
                self.model = MLPClassifier(**params)
            else:
                self.model = MLPClassifier(hidden_layer_sizes = n_hidden, solver='lbfgs')
        elif self.algorithm == 'RandomForest':
            if len(params) > 1:
                self.model = RandomForestClassifier(**params)
            else:
                self.model == RandomForestClassifier(n_estimators=n_estimators,random_state=0)


    def train(self, validate = True):
        """训练模型.

        Args:
            validate (bool, optional): 是否需要验证模型，并输出准确率. Defaults to True.
        """
        if self.algorithm in ['AdaBoost','SVM','NaiveBayes', 'MLP','KNN','CART','RandomForest']:

            if validate:  

                self.x_train, self.x_val, self.y_train, self.y_val = \
                train_test_split(self.x_train, self.y_train, test_size=0.2, random_state=0)

            self.model.fit(self.x_train, self.y_train)

            if validate:
                pred = self.model.predict(self.x_val)
                acc = accuracy_score(self.y_val, pred)
                print('准确率为：{}%'.format(acc * 100))



    def inference(self, data = np.nan, verbose = True):
        """使用模型进行推理

        Args:
            data (numpy, optional): 放进来推理的数据,不填默认使用self.x_test.
            verbose (bool, optional): 是否输出推理中的中间结果. Defaults to True.

        Returns:
            pred: 返回预测结果.
        """
        if data is not np.nan: # 对data进行了指定
            self.x_test = data
        elif len(self.x_train) > 0 and len(self.x_test) == 0:
            self.x_test = self.x_train

        if self.algorithm in ['AdaBoost','SVM','NaiveBayes', 'MLP','KNN','CART', 'RandomForest']:
            self.pred = self.model.predict(self.x_test)
            return self.pred


    def extract_hog_features(self, X):
        image_descriptors = []
        for i in range(len(X)):                                         # 此处的X为之前训练部分所有图像的矩阵形式拼接而来，
            # print(i)                                                  # 所以len(X)实为X中矩阵的个数，即训练部分图像的个数
            fd, _ = hog(X[i], orientations=9, pixels_per_cell=(16, 16), cells_per_block=(16, 16),
                                block_norm='L2-Hys', visualize=True)    # 此处的参数细节详见其他文章
            image_descriptors.append(fd)                                # 拼接得到所有图像的hog特征
        return image_descriptors                                        # 返回的是训练部分所有图像的hog特征


    def extract_hog_features_single(self, X):
        image_descriptors_single = []
        fd, _ = hog(X, orientations=9, pixels_per_cell=(16, 16), cells_per_block=(16, 16),
                                block_norm='L2-Hys', visualize=True)
        image_descriptors_single.append(fd)
        return image_descriptors_single

    
    def read_data_and_pre(self, label2id, path):
        X = []
        Y = []
        path =r'../dataset/JAFFE/training_set'
        for label in os.listdir(path):
            for img_file in os.listdir(os.path.join(path, label)):              # 遍历
                image = cv2.imread(os.path.join(path, label, img_file))         # 读取图像
                result = image/255.0                                            # 图像归一化
                res = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                   # 转灰度
                # cv2.waitKey(0)
                cv2.destroyAllWindows()
                X.append(res)                                                   # 将读取到的所有图像的矩阵形式拼接在一起
                Y.append(label2id[label])                                       # 将读取到的所有图像的标签拼接在一起
        self.X = self.extract_hog_features(X)
        self.Y = Y
        return self.extract_hog_features(X), Y                                                             # 返回的X,Y分别是图像的矩阵表达和图像的标签


    def plot(self):
        acc = accuracy_score(self.y_test, self.pred)
        precision = precision_score(self.y_test, self.pred, average='macro')
        recall = recall_score(self.y_test, self.pred, average='macro')
        cm = confusion_matrix(self.y_test, self.pred)
        print(cm)
        print('Acc: ', acc)
        print('Precision: ', precision)
        print('Recall: ', recall)
        
        xtick = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        ytick = xtick
        
        f, ax = plt.subplots(figsize=(7, 5))
        ax.tick_params(axis='y', labelsize=15)
        ax.tick_params(axis='x', labelsize=15)
        
        seaborn.set(font_scale=1.2)
        plt.rc('font',family='Times New Roman', size=15)
        
        seaborn.heatmap(cm,fmt='g', cmap='Blues', annot=True, cbar=True,xticklabels=xtick, yticklabels=ytick, ax=ax)
        
        plt.title('Confusion Matrix', fontsize='x-large')
        
        plt.show()

    
    def test(self, path):
    # 下面为同一文件夹下多张图片的表情识别
    # labelid2 = {0:'angry',1: 'disgust',2: 'fear',3:'happy',4:'neutral',5:'sad',6:'surprise'}
        path=path
        i = 1
        for dir in os.listdir((path)):
            temp_path = os.path.join(path, dir)
            for image_file in os.listdir(temp_path):
                image = cv2.imread(os.path.join(temp_path,image_file))
                # result = image/255.0
                # cv2.waitKey(1000)
                # cv2.destroyAllWindows()
                result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                X_Single = self.extract_hog_features_single(result)
                predict = self.model.predict(X_Single)         # 可以在这里选择分类器的类别
                print(i)
                i += 1
                if predict == 0:
                    print('angry')
                elif predict == 1:
                    print('disgust')
                elif predict == 2:
                    print('fear')
                elif predict == 3:
                    print('happy')
                elif predict == 4:
                    print('neutral')
                elif predict == 5:
                    print('sad')
                elif predict == 6:
                    print('surprise')
