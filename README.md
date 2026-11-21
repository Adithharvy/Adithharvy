# Python, machine learning and data analysis

## Project portfolio

| Project | Question and result | Evidence |
| --- | --- | --- |
| [Support queue analysis](projects/support-queue) | Which queue has waited longest? In the fictional sample, Payments has a 36-hour open ticket despite a six-hour average resolution time for closed tickets. | [SQL query](projects/support-queue/report.sql) · [Four boundary tests](projects/support-queue/test_report.py) |
| [Iris classifier evaluation](projects/iris-evaluation) | Can logistic regression beat a simple baseline? It classified 143 of 150 held-out examples correctly across five folds. The baseline classified 50 correctly. | [Evaluation script](projects/iris-evaluation/evaluate.py) · [Error analysis and run instructions](projects/iris-evaluation/README.md) |
| [NumPy practice notebook](https://github.com/Adithharvy/AI-ML-Internship/blob/main/numpy.ipynb) | Internship practice with NumPy. | [Open notebook](https://github.com/Adithharvy/AI-ML-Internship/blob/main/numpy.ipynb) |

To check the queue report's cutoff behavior, run this from the repository root:

```sh
python -m unittest discover -s projects/support-queue -v
```
