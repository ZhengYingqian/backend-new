import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets.samples_generator import make_blobs
#X为样本特征，Y为样本簇类别， 共1000个样本，每个样本3个特征，共4个簇
X, y = make_blobs(n_samples=10000, n_features=3, centers=[[3,3, 3], [0,0,0], [1,1,1], [2,2,2]], cluster_std=[0.2, 0.1, 0.2, 0.2], 
                  random_state =9)
fig = plt.figure()
ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=30, azim=20)
plt.scatter(X[:, 0], X[:, 1], X[:, 2],marker='o')
#先不降维，只对数据进行投影，看看投影后的三个维度的方差分布
from sklearn.decomposition import PCA
pca = PCA(n_components=3)
pca.fit(X)
#返回所保留的n个成分各自的方差百分比
print(pca.explained_variance_ratio_)
print(pca.explained_variance_)
#进行降维，从三维降到2维
pca1 = PCA(n_components=2)
pca1.fit(X)
print(pca1.explained_variance_ratio_)
print(pca1.explained_variance_)
#返回所保留的n个成分各自的方差百分比
print(pca1.explained_variance_ratio_)
print(pca1.explained_variance_)
'''通过对比，因为上面三个投影后的特征维度的方差分别为：
[ 3.78483785  0.03272285  0.03201892]，投影到二维后选择的肯定是前两个特征，而抛弃第三个特征'''
#将降维后的2维数据进行可视化
X_new = pca1.transform(X)
plt.scatter(X_new[:, 0], X_new[:, 1],marker='o')
plt.show()