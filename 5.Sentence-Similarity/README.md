# Sentence pair similarity

## 1. 数据示例
![simi](../images/simi1.png)

## 2. 模型
### 1. Sentence Bert

SBERT在BERT/RoBERTa的输出结果上增加了一个Pooling操作，从而生成一个固定维度的句子Embedding。实验中采取了三种Pooling策略做对比：

- CLS：直接用CLS位置的输出向量作为整个句子向量

- MEAN：计算所有Token输出向量的平均值作为整个句子向量

- MAX：取出所有Token输出向量各个维度的最大值作为整个句子向量

![simi](../images/simi2.png)

### 2. Siamese Network

同样采取以上三种Pooling策略，loss function 采用 COSINEEMBEDDINGLOSS。我们真正要做的是一个特征提取模型（编码器），而最后使用的方法是对特征提取模型的特征进行对比排序。

### 3. Margin Softmax

同样采取以上三种Pooling策略，将训练集划分为很多组“同义句”，然后有多少组就有多少类，也将句子相似度问题当作分类问题来做。我们真正要做的是一个特征提取模型（编码器），而最后使用的方法是对特征提取模型的特征进行对比排序。
同时加强一下分类条件，就可以提升排序效果了，比如改为：每个样本与它所属类的距离，必须小于它跟其他类的距离的 1/2。
