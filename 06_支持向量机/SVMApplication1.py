"""
国际象棋规则介绍
兵王问题：黑方只剩一个王，白方剩一个兵和王
两种可能：
    （1）白方将死黑方，获胜。（注：黑方只有一个王不可能胜白方）
    （2）和棋。
这两种可能视三个棋子在棋盘的位置而确定。
兵的升变：兵走至对方底线，可以升变为除王以外的任意一子。
逼和：一方的王未被将军，但移动到任意地方都会被对方将死，则此时是和棋。


数据集：
    UCI Machine Learning Repository
    http://archive.ics.uci.edu/ml/datasets.html


过程：
·总样本数28056，其中正样本2796，负样本25260
·随机取5000个样本训练，其余测试。
·样本归一化，在训练样本上，求出每个维度的均值和方差，在训练和测试样本上同时归一化。
    newX = (X - mean(X))/std(X)
·选取一个高斯核
·在CScale = [2^(-5),2^15]; gamma = [2^(-15),2^3];上遍历求识别率的最大值。
 上述C和gamma的区间设置参见LIBSVM自带的介绍：a practical guide to support vector classification


交叉验证：
    5000个样本分五组，每组1000个
    a 1000   b 1000  c 1000  d 1000  e 1000
    第一次（a b c d）训练，e测试
    第二次......
    ......
    第五次（b c d e）训练，a测试


训练参数设置svmtrain(yTraining,xTraining,cmd)
cmd的参数设置如下：
(1)-s 0 "-s svm_type:set type of SVM(default 0)\n"
        "0 -- C-SVC (multi-class classification)\n"
        "1 -- nu-SVC (multi-class classification)\n"
        "2 -- one-class SVM\n"
        "3 -- epsilon-SVR (regression)\n"
        "4 -- nu-SVR (regression)\n"
(2)-t 2 "-t kernel_type:set type of kernel function (default 2)\n"
        "0 -- linear: u'*v\n"
        "1 -- polynomial:(gamma*u'*v+coef0)^degree\n"
        "2 -- radial basis function:exp(-gamma*|u-v|^2)\n"
        "3 -- sigmoid:tanh(gamma*u'*v + coef0)\n"
        "4 -- precomputed kernel(kernel values in training_instance_matrix)\n"
(3)-c CVALUE
    "-c cost:set the parameter C of C-SVC,epsilon-SVR,and nu-SVR(default 1)\n"
(4)-g gammaValue
    "-g gamma:set gamma in kernel function (default 1/num_features)\n"
(5)-v 5   (5折交叉验证)
    "-v n:n-fold cross validation"
"""




