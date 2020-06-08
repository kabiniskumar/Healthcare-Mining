For Solr and TF Analysis, we used the “Top 1% error” and “Top 5% error” metrics to determine its efficiency.
    
The Top-1% error is the percentage of the times that the model did not give the correct class the highest score. The Top-5% error is the percentage of the time that the classifier did not include the correct class among its top 5 guesses. In both cases, the top score is computed as the times a predicted label matched the target label, divided by the number of data-points evaluated.


|                   |  Solr    |   TF Analysis   |
|-------------------|----------|-----------------|
| Top 5% error rate |  12.46%  |    15.92%       |
| Top 1% error rate |  15.38%  |    19.51%       |
    
From the above comparision, we observed that Solr gave us slightly better results as compared to TF analysis.

We obtained the below results for the ML models:

| | Multinomial Naive Bayes | Decision Tree | Multi Layer Perceptron
|-|-----|----|----
Precision | 0.56 | 0.12 | 0.73
Recall | 0.65 | 0.34 | 0.66
F1-score | 0.60 | 0.18 | 0.69
Accuracy | 87.5 | 43.6 | 86.9
