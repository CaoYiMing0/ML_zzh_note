# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 去中心化
from sklearn.preprocessing import StandardScaler
# 训练集合测试集的划分
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap
# 逻辑回归进行分类
from sklearn.linear_model import LogisticRegression

# 读取数据
df_wine = pd.read_csv('wine.data', header=None)
"""
该数据集是UCI的公开数据集，是对意大利同一地区种植的葡萄酒进行分析的结果，数据集共14列数据，
第一个属性是类标识符，分别是1/2/3来表示，代表葡萄酒的三个分类，剩余的13个属性是：酒精、苹果酸、
灰、灰分的碱度、镁、总酚、黄酮类化合物、非黄烷类酚类、原花色素、颜色强度、色调等。
"""
# 设置索引
df_wine.columns = ['Class lable', 'Alcohol',
                   'Malic acid', 'Ash', 'Alcalinity of ash',
                   'Magnesium', 'Total phenols', 'Flavanoids',
                   'Nonflavanoid phenols', 'Proanthocyanins',
                   'Color intensity', 'Hue', 'OD280/OD315 of diluted wines', 'Proline']
# 数据维度
print(df_wine.shape)  # (178, 14)  178个样本，14个特征含类别
# 每一类数据包含的样本个数
print(df_wine['Class lable'].value_counts())
print(df_wine.head())

# 数据集划分
# 数据集设置：x为样本特征数据，y为目标数据，即标注结果
X, y = df_wine.iloc[:, 1:].values, df_wine.iloc[:, 0].values
# 数据集划分：将数据集划分为训练集合测试集数据（测试集数据为30%，训练集为70%）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    stratify=y,
                                                    random_state=0)

# 数据标准化
# 实例化
sc = StandardScaler()
# 对数据集进行标准化（一般情况下我们在训练集中进行均值和方差的计算，直接在测试集中使用）
X_train_std = sc.fit_transform(X_train)
X_test_std = sc.transform(X_test)

# PCA实现
# 特征值计算
cov_mat = np.cov(X_train_std.T)
# 对协方差矩阵进行特征值分解
eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)
# 特征值
print(
    eigen_vals)  # [4.84274532 2.41602459 1.54845825 0.96120438 0.84166161 0.6620634 0.51828472 0.34650377 0.3131368  0.10754642 0.21357215 0.15362835 0.1808613 ]

# 特征值分布
# 特征值之和
tot = sum(eigen_vals)
# 对特征进行排序，并计算所占的比例
var_exp = [(i / tot) for i in sorted(eigen_vals, reverse=True)]
# 累计求和
cum_var_exp = np.cumsum(var_exp)
# 绘制图像
plt.figure()
plt.bar(range(1, 14), var_exp, alpha=0.5, align='center', label='tezhengzhi fenbu')
plt.step(range(1, 14), cum_var_exp, where='mid', label='leiji tezhengzhi')
plt.ylabel('tezhengzhi bili')
plt.xlabel('tezheng index')
plt.legend(loc='best')
plt.show()

# 特征降维
# 创建列表，由（eigenvalue,eigenvector）元组构成
eigen_pairs = [(np.abs(eigen_vals[i]), eigen_vecs[:, i]) for i in range(len(eigen_vals))]
# 按特征值从大到小对列表（eigenvalue,eigenvector）排序
eigen_pairs.sort(key=lambda k: k[0], reverse=True)
# 特征值与特征向量
print(eigen_pairs)
"""
[(4.842745315655895, array([-0.13724218,  0.24724326, -0.02545159,  0.20694508, -0.15436582,
       -0.39376952, -0.41735106,  0.30572896, -0.30668347,  0.07554066,
       -0.32613263, -0.36861022, -0.29669651])), (2.416024587035225, array([ 0.50303478,  0.16487119,  0.24456476, -0.11352904,  0.28974518,
        0.05080104, -0.02287338,  0.09048885,  0.00835233,  0.54977581,
       -0.20716433, -0.24902536,  0.38022942])), (1.5484582488203524, array([-0.13774873,  0.09615039,  0.67777567,  0.62504055,  0.19613548,
        0.14031057,  0.11705386,  0.13121778,  0.0304309 , -0.07992997,
        0.05305915,  0.13239103, -0.07065022])), (0.9612043774977378, array([-0.0032961 ,  0.56264669, -0.10897711,  0.0338187 , -0.36751107,
        0.24024513,  0.1870533 , -0.02292622,  0.49626233,  0.10648294,
       -0.36905375,  0.14201609, -0.16768217])), (0.8416616104578416, array([-0.29062523,  0.08953787, -0.16083499,  0.05158734,  0.67648707,
       -0.11851114, -0.10710035, -0.50758161,  0.20163462,  0.00573607,
       -0.27691422, -0.06662756, -0.12802904])), (0.6620634040383038, array([ 2.99096847e-01,  6.27036396e-01,  3.89128239e-04, -4.05836452e-02,
        6.57772614e-02, -5.89776247e-02, -3.01103180e-02, -2.71728086e-01,
       -4.39997519e-01, -4.11743459e-01,  1.41673377e-01,  1.75842384e-01,
        1.38018388e-01])), (0.5182847213561963, array([ 0.07905293, -0.27400201,  0.13232805,  0.2239991 , -0.40526897,
       -0.03474194,  0.04178357, -0.63114569, -0.32312277,  0.26908262,
       -0.30264066,  0.13054014,  0.00081134])), (0.34650376641286734, array([-0.36817641, -0.01257758,  0.17757818, -0.44059211,  0.1166175 ,
        0.35019213,  0.21871818,  0.19712942, -0.43305587, -0.06684118,
       -0.45976229,  0.11082755,  0.00560817])), (0.3131368004720887, array([-0.39837702,  0.11045823,  0.38249686, -0.24337385, -0.25898236,
       -0.34231286, -0.03612316, -0.17143688,  0.24437021, -0.15551492,
        0.02119612, -0.23808956,  0.51727846])), (0.2135721466052734, array([ 0.37463888, -0.1374056 ,  0.46158303, -0.41895399,  0.01004706,
       -0.22125424, -0.04175136, -0.08875695,  0.19992186, -0.22166887,
       -0.09846946,  0.01912058, -0.54253207])), (0.1808613047949662, array([ 0.26283426, -0.26676921, -0.11554255,  0.19948341,  0.02890188,
       -0.06638686, -0.21334908,  0.18639128,  0.16808299, -0.46636903,
       -0.53248388,  0.23783528,  0.36776336])), (0.15362835006711026, array([-0.12783451,  0.08064016,  0.01679249, -0.11084566,  0.07938796,
       -0.49145931, -0.0503074 ,  0.17532803, -0.00367596,  0.35975654,
        0.04046698,  0.74222954,  0.03873952])), (0.10754642369670969, array([-0.09448698,  0.02636524,  0.14274751, -0.13048578, -0.06760808,
        0.45991766, -0.81458395, -0.09574809,  0.06724689,  0.08733362,
        0.12906113,  0.18764627,  0.01211126]))]
"""
# 取前两个特征值对应的特征向量作为主要成分
w = np.hstack((eigen_pairs[0][1][:, np.newaxis],
               eigen_pairs[1][1][:, np.newaxis]))
print(w)
"""
[[-0.13724218  0.50303478]
 [ 0.24724326  0.16487119]
 [-0.02545159  0.24456476]
 [ 0.20694508 -0.11352904]
 [-0.15436582  0.28974518]
 [-0.39376952  0.05080104]
 [-0.41735106 -0.02287338]
 [ 0.30572896  0.09048885]
 [-0.30668347  0.00835233]
 [ 0.07554066  0.54977581]
 [-0.32613263 -0.20716433]
 [-0.36861022 -0.24902536]
 [-0.29669651  0.38022942]]
"""
# 原始特征（以第一个样本为例）
print(X_train_std[0])
"""
压缩前：
[ 0.71225893  2.22048673 -0.13025864  0.05962872 -0.50432733 -0.52831584
 -1.24000033  0.84118003 -1.05215112 -0.29218864 -0.20017028 -0.82164144
 -0.62946362]
"""
# 特征压缩后结果
print(X_train_std[0].dot(w))  # [2.38299011 0.45458499]
# 全部特征压缩
X_train_pca = X_train_std.dot(w)
# 特征压缩后结果展示
colors = ['r', 'b', 'g']
markers = ['s', 'x', 'o']
for l, c, m in zip(np.unique(y_train), colors, markers):
    # 按照样本的真实值进行展示
    plt.scatter(X_train_pca[y_train == 1, 0],
                X_train_pca[y_train == 1, 1],
                c=c, label=1, marker=m)
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()
