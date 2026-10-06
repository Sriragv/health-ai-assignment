# Level 3 Prediction

Current results at threshold 0.5 for my numpy model:
precision 0.762 

recall 0.593

TP=32, FN=22, FP=10, TN=90.



The given dataset has 54 diabetic patients out of 154.9Prediction: we need to catch atleast 49 out of the total 154 patients to get a recall of 0.9
I expect to lower the threshold to roughly 0.2-0.3.
More healthy people will be considered as diabetec, so precision will drop from 0.762 to about 0.45-0.55.
Accuracy will also go down, probably to around 0.65-0.70.
Precision cannot go below 0.35 (54/154), which is what flagging everyone would give.

