the results are closer to our preddictions which i have mentioned before.infact they are slightly better than our predictions 

my predicted threshold was right(threshold = 0.25)form my range 0.2 to 0.3, with this it catches 50 out of 54 diabetic patients. it misses only 4 instead of 22 from earlier. the cost for this is 37 false positives but it is always better to have a false positive which can be solved by an additional blood test than losing a real diabetic patient who was untreated because he was missing out in the prediction.we can go even lower to threshold = 0.20
which will help us catch one more diabetic patient and increases 9 more false positives.

precision fell from 0.762 to 0.575, which is slightly better than what i have expected i.e 0.55

accuracy has dropped to 0.734. so more healthy people were tagged as healthy compared to my predicted value.the accuracy is misleading because for threshold at 0.50 , the accuracy was at 0.792 whereas for threshold = 0.25 , the accuracy is 0.734. here the threshold at 0.50 has more accuracy but still it misses 22 patients who have diabetes. 

baseline point: a model predicting "nobody is diabetic" gets 0.649 accuracy and catches zero patients. That's the strongest proof that the accuracy misleads.

i should have chosen the threshold for a separated validation set rather than the test set itself bcoz the test set has only 54 diabetic patients so the recall each patient moves is about 1.9%.
