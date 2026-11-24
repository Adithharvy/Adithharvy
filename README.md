# Python, SQL and machine learning

## Start here · Iris classifier evaluation

[Open the one-minute demo and reproduce the results](https://github.com/Adithharvy/Adithharvy/tree/main/projects/iris-evaluation)

On the Iris dataset, logistic regression classified **143 of 150** held-out examples correctly across five stratified folds. The majority-class baseline classified **50 of 150** on the same splits. All seven errors were between versicolor and virginica. The evaluation script fits the scaler inside each training fold and prints both confusion matrices.

## SQL project

### Which support queue needs attention first?

The oldest open Payments ticket in this eight-ticket fictional dataset had waited **36 hours**. Its one completed ticket took **6 hours**. Looking only at completed tickets hides the longest wait. The report reconstructs each queue at a chosen UTC cutoff and tests how tickets opened or closed exactly at that time are counted.

[Read the analysis](https://github.com/Adithharvy/Adithharvy/tree/main/projects/support-queue) · [Inspect the SQL](https://github.com/Adithharvy/Adithharvy/blob/main/projects/support-queue/report.sql) · [See the boundary tests](https://github.com/Adithharvy/Adithharvy/blob/main/projects/support-queue/test_report.py)

## Run the SQL report tests

From the repository root:

```sh
python -m unittest discover -s projects/support-queue -v
```

## Practice notebooks

[NumPy array practice](https://github.com/Adithharvy/AI-ML-Internship/blob/main/numpy.ipynb) covers vectors, matrices, numeric sequences and repeatable random samples.

## Selected job simulations

Completed through Forage on 30 June 2026.

- **Quantium · Data Analytics** — Prepared customer data and used experimentation and uplift testing to evaluate commercial impact. Credential ID `65GbAMZ3Sk3qXYDB8`.
- **Quantium · Software Engineering** — Processed data, built a Python Dash application and tested its behavior. Credential ID `4cHjB3Cct6TZq7gLv`.
