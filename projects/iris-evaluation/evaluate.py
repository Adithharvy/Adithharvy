"""Compare a baseline with scaled logistic regression using out-of-fold predictions."""
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def main():
    iris = load_iris()
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    models = {
        "Majority baseline": DummyClassifier(strategy="most_frequent"),
        "Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=500)),
    }
    for name, model in models.items():
        predicted = cross_val_predict(model, iris.data, iris.target, cv=folds)
        print(f"{name}: {accuracy_score(iris.target, predicted):.1%} accuracy")
        print("Rows = observed, columns = predicted:", ", ".join(iris.target_names))
        print(confusion_matrix(iris.target, predicted))


if __name__ == "__main__":
    main()
