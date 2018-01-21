
# coding: utf-8

# In[7]:


import numpy as np
from sklearn.base import BaseEstimator

from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error

from svm_checker import Checker


# In[2]:


SVM_PARAMS_DICT = {
    'C': 10.,
    'random_state': 777,
    'iters': 10000,
    'batch_size': 100,
    'step': 0.015
}


# In[72]:


class MySVM(BaseEstimator):
    def __init__(self, C, random_state, iters, batch_size, step):
        self.C = C
        self.random_state = random_state
        self.iters = iters
        self.batch_size = batch_size
        self.step = step

    # будем пользоваться этой функцией для подсчёта <w, x>
    def __predict(self, X):
        return np.dot(X, self.w) + self.w0

    # sklearn нужно, чтобы predict возвращал классы, поэтому оборачиваем наш __predict в это
    def predict(self, X):
        res = self.__predict(X)
        res[res > 0] = 1
        res[res < 0] = 0
        return res

    # производная регуляризатора
    def der_reg(self):
        return 1. / self.C * self.w

    # будем считать стохастический градиент не на одном элементе, а сразу на пачке (чтобы было эффективнее)
    def der_loss(self, x, y):
        #s.shape == (self.batch_size, features)
        #y.shape == (self.batch_size,)

        # считаем производную по каждой координате на каждом объекте
        margin = np.multiply(y, self.__predict(x))

        # занулить производные там, где отступ > 1
        margin[margin < 1] = -1.0
        margin[margin > 1] = 0.0
        
        # для масштаба возвращаем средний градиент по пачке
        return np.mean(margin)

    def fit(self, X_train, y_train):
        # RandomState для воспроизводитмости
        random_gen = np.random.RandomState(self.random_state)
        
        # получаем размерности матрицы
        size, dim = X_train.shape
        
        # случайная начальная инициализация
        self.w = random_gen.rand(dim)
        self.w0 = random_gen.randn()

        for _ in range(self.iters):  
            # берём случайный набор элементов
            rand_indices = random_gen.choice(size, self.batch_size)
            x = X_train[rand_indices]
            y = y_train[rand_indices] * 2 - 1 # исходные метки классов это 0/1 а нам надо -1/1

            # считаем производные
            # TODO

            # обновляемся по антиградиенту
            self.w -= np.mean(np.multiply(x, y.reshape(self.batch_size, 1)) * self.der_loss(x,y) * self.step, axis = 0)
            self.w0 -= np.mean(y * self.der_loss(x,y) * self.step)

        # метод fit для sklearn должен возвращать self
        return self


# In[73]:


#algo = MySVM(**SVM_PARAMS_DICT)


# In[74]:


#X_data, y_data = make_classification(
#    n_samples=10000, n_features=20, 
#    n_classes=2, n_informative=20, 
#    n_redundant=0,
#    random_state=42
#)


# In[75]:


#np.mean(cross_val_score(algo, X_data, y_data, cv=2, scoring='accuracy'))


# In[76]:


#Checker().check('MY_SVN.ipynb')

