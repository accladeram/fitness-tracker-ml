# Fitness Tracker - Machine Learning Project

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── data
│   ├── external       <- Data from third party sources
│   ├── interim        <- Intermediate data that has been transformed
│   ├── processed      <- The final, canonical data sets for modeling
│   └── raw            <- The original, immutable data dump
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    │
    ├── modeling
    │   ├── __init__.py
    │   ├── predict.py          <- Code to run model inference with trained models
    │   └── train.py            <- Code to train models
    │
    ├── plots.py                <- Code to create visualizations
    │
    └── services                <- Service classes to connect with external platforms, tools, or APIs
        └── __init__.py
```

---

## 📚 Learning Purpose & Project Inspiration

This repository is part of my learning process in building end-to-end machine learning projects with a more professional structure. It follows a tutorial by Dave Ebbelaar, which you can find [here](https://youtube.com/playlist?list=PL-Y17yukoyy0sT2hoSQxn1TdV0J7-MX4K&si=10x92eoLpNchFECN).

I was intrigued by how Dave bridged machine learning with fitness, using training data to generate practical insights. His structured approach showed how technical tools can be applied to real-world routines in a meaningful way.

Through this project, I aim to gain practical experience in organizing code beyond notebooks, managing environments, and developing reproducible workflows. While I follow the general structure of the tutorial, this implementation reflects my own learning journey and personal adaptations.
