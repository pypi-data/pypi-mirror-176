
import numpy as np
from sklearn.metrics import  mean_squared_error, r2_score
from sklearn import linear_model
from sklearn import tree
from sklearn import ensemble
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import joblib
from .base import baseml

class Regression(baseml):
    """BaseML中的回归模块,包含['LinearRegression', 'DecisionTree', 'RandomForest',
       'Polynomial', 'Lasso', 'Ridge']回归算法.

    Attributes:
        algorithm: 算法名称
        model: 实例化的模型
    """
    def __init__(self, algorithm='LinearRegression', n_estimators = 20, degree = 2, params = {}):
        """reg类的初始化

        Args:
            algorithm (str, optional): 选择的回归学习器. Defaults to 'LinearRegression'.
            n_estimators (int, optional): RandomForest集成的决策树个数. Defaults to 20.
            degree (int, optional): 多项式回归的阶数. Defaults to 2.
            params (dict, optional): 参数字典,可自定义参数放入,参数名称详见sklearn官方文档. Defaults to {}.
        """
        super(Regression,self).__init__()   # 继承父类的构造方法
        self.algorithm = algorithm
        if self.algorithm ==  'LinearRegression':   # 线性回归
            if len(params) > 1:
                self.model = linear_model.LinearRegression(**params)
            else:
                self.model = linear_model.LinearRegression()
        elif self.algorithm == 'DecisionTree':   # 决策树回归
            if len(params) > 1:
                self.model = tree.DecisionTreeRegressor(**params)
            else:
                self.model = tree.DecisionTreeRegressor()
        elif self.algorithm == 'RandomForest':   # 随机森林回归
            if len(params) > 1:
                self.model = ensemble.RandomForestRegressor(**params)
            else:
                self.model = ensemble.RandomForestRegressor(n_estimators=n_estimators)
        elif self.algorithm == 'Polynomial':     # 多项式回归
            if len(params) > 1:
                self.model = PolynomialFeatures(**params)
                self.poly_linear_model = linear_model.LinearRegression()
            else:
                self.model = PolynomialFeatures(degree=degree)  
                self.poly_linear_model = linear_model.LinearRegression()
        elif self.algorithm == 'Lasso':          # Lasso回归
            if len(params) > 1:
                self.model = linear_model.Lasso(**params)
            else:
                self.model = linear_model.Lasso()
        elif self.algorithm == 'Ridge':          # 岭回归
            if len(params) > 1:
                self.model = linear_model.Ridge(**params)
            else:
                self.model = linear_model.Ridge()

       
    def train(self, validate = True):
        """训练模型

        Args:
            validate (bool, optional): 是否需要验证模型，并输出R值. Defaults to True.
        """

        if validate:  # 需要划分数据集，并输出准确率
            self.x_train, self.x_val, self.y_train, self.y_val = \
                train_test_split(self.x_train, self.y_train, test_size=0.2, random_state=0)

        if self.algorithm == 'Polynomial':
            x_transformed = self.model.fit_transform(self.x_train)#x每个数据对应的多项式系数
            self.poly_linear_model.fit(x_transformed, self.y_train)

        else: 
            self.model.fit(self.x_train, self.y_train)

        if validate:
            if len(self.y_val < 2):
                print("测试集小于2个样本，无法使用R值计算")
            else:
                pred = self.model.predict(self.x_val)
                acc = r2_score(self.y_val, pred)
                print('R值为: {}%'.format(acc))


    def inference(self, data = np.nan):
        """_summary_

        Args:
            data (numpy, optional): 放进来推理的数据,不填默认使用self.x_test.

        Returns:
            pred: 返回预测结果.
        """
        if data is not np.nan: # 对data进行了指定
            self.x_test = data
        if self.algorithm == 'Polynomial':
            x_trans = self.model.transform(self.x_test)
            self.pred = self.poly_linear_model.predict(x_trans)
            # self.pred = self.model.
        else:
            self.pred = self.model.predict(self.x_test)

        return self.pred

    # 重写方法
    def save(self,path="checkpoint.pkl"):
        print("Saving model checkpoints...")
        if self.algorithm == 'Polynomial':
            modelList = [self.model, self.poly_linear_model]
            joblib.dump(modelList, path, compress=3)
        else:
            joblib.dump(self.model, path, compress=3)
        print("Saved successfully!")
        
    
    def load(self, path):
        if self.algorithm == 'Polynomial':
            self.model = joblib.load(path)[0]
            self.poly_linear_model = joblib.load(path)[1]
        else:
            self.model = joblib.load(path)
