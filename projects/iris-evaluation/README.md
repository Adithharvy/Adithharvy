# Evaluating an Iris classifier

This portfolio exercise compares logistic regression to a majority-class baseline on the 150 labeled examples in scikit-learn's built-in Iris dataset. Four sepal and petal measurements are available for each flower.

## One-minute demo

Can four flower measurements predict the species? I built a Python comparison that scores a simple baseline and logistic regression on the same held-out flowers. I standardized the measurements inside each training fold and inspected the confusion matrix to see where the model struggled.

| Actual species | Predicted setosa | Predicted versicolor | Predicted virginica |
| --- | ---: | ---: | ---: |
| Setosa | 50 | 0 | 0 |
| Versicolor | 0 | 47 | 3 |
| Virginica | 0 | 4 | 46 |

Read across the last row: of 50 virginica flowers, the model identified 46 and called four versicolor. Overall it got 93 more predictions right than the baseline. [See the evaluation script](./evaluate.py).

## Reproduce the demo

With Git and Python 3.11 or newer, run these commands in a terminal:

```sh
git clone https://github.com/Adithharvy/Adithharvy.git
cd Adithharvy/projects/iris-evaluation
python -m pip install -r requirements.txt
python evaluate.py
```

## Results

Both models use the same five stratified folds and fixed shuffle seed. The scaler is fitted inside the training pipeline for each fold. Each example contributes one held-out prediction.

| Model | Correct | Accuracy |
| --- | ---: | ---: |
| Majority baseline | 50 / 150 | 33.3% |
| Logistic regression | 143 / 150 | 95.3% |

All 50 setosa flowers were classified correctly. Three versicolor flowers were predicted as virginica, and four virginica flowers as versicolor. The script prints both confusion matrices so you can check the direction of each mistake. This small benchmark measures performance on these examples; it cannot establish accuracy for field photographs or other populations.
