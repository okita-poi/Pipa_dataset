## Pipa_dataset 琵琶数据集
**数据集内容还在完善当中，请随时注意更新**

该数据集包含了在琵琶上演奏的音乐片段的录音，同时提供了时间对齐的注解，包括音高、起始点的midi文件以及包含基础评价指标的python示例。


音频格式为mp3，长度30秒至90秒不等，采样率192kbps

### 评估标准
这里提供了最基础的评估标准  
#### 匹配逻辑
对于每个标准音符 s_note，在结果音符列表中查找未被匹配的音符 r_note。
#### 匹配条件：
音高相同：开始时间差异在阈值范围内  
一旦找到符合条件的结果音符，记录其索引，并跳出内层循环，继续下一个标准音符的匹配。
#### 计算评估指标
准确率（Precision）：

$$
\text{Precision}
= \frac{\text{TP}}{\text{TP}+\text{FP}} 
​$$
 
召回率（Recall）：
$$
\text{Recall}
= \frac{\text{TP}}{\text{TP}+\text{FN}} 
​$$
​
 
F1 分数（F1 Score）：
$$
\text{F1 Score}
= 2*\frac{\text{Precision} * \text{Recall}}{\text{Precision} + \text{Recall}} 
​$$