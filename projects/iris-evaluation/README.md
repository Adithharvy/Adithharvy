# Evaluating an Iris classifier

This portfolio exercise compares logistic regression to a majority-class baseline on the 150 labeled examples in scikit-learn's built-in Iris dataset. Four sepal and petal measurements are available for each flower.

## Run

From this directory, with Python 3.11 or newer:

```sh
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
