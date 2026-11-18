import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    return np, sns


@app.cell
def _():
    from kaggle_api import fetch_dataset

    df_train, df_test = fetch_dataset()
    return df_test, df_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # model overview

    predictors:

    - categorical - $x_4, x_5, x_{10}$
    - create new predictor $x_{11} := \mathbb{1} \{x_1 >= 0\}$

    model type: manual regression / classification tree
    """)
    return


@app.cell
def _(df_test, df_train, np):
    df_train["x11"] = (df_train.x1 >= 0).astype(np.int8)
    df_test["x11"] = (df_test.x1 >= 0).astype(np.int8)

    active_pred_names = "x4 x5 x10 x11".split()
    return (active_pred_names,)


@app.cell
def _(active_pred_names, df_test, df_train, mo):
    model_weights = (
        df_train.loc[df_train.Y == 1, active_pred_names].value_counts()
        / df_train[active_pred_names].value_counts()
    )

    prediction_probs = model_weights[
        (row for i, row in df_test[active_pred_names].iterrows())
    ]

    mo.output.append(df_test.loc[15001:15005, active_pred_names])
    mo.output.append(prediction_probs.index[0:5])

    prediction_probs.index = df_test.index
    return (prediction_probs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # model assessment
    """)
    return


@app.cell
def _(mo, prediction_probs):
    import threshold as th

    pos_prediction_count, threshold = th.estimate_optimal_threshold(prediction_probs)

    mo.output.append(pos_prediction_count)
    mo.output.append(threshold)
    return pos_prediction_count, th, threshold


@app.cell
def _(np, pos_prediction_count, prediction_probs, sns, th, threshold):
    rng = np.random.default_rng(1)

    # sns.set_theme(style="whitegrid")

    ax = sns.violinplot(
        y=th.sample_probable_f_scores(rng, 1000, prediction_probs, pos_prediction_count)
    )
    ax.yaxis.set_label_text("F-score")

    ax.hlines(2 * threshold, xmin=-0.5, xmax=0.5, colors="cyan", linestyles="--")
    ax.hlines(0.54023, xmin=-0.5, xmax=0.5, colors="red", linestyles="-.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # make submission
    """)
    return


@app.cell
def _(np, pos_prediction_count, prediction_probs):
    predictions = prediction_probs.sort_values(ascending=False)
    predictions.iloc[0:pos_prediction_count] = 1
    predictions.iloc[pos_prediction_count:] = 0
    predictions = predictions.astype(np.int8).sort_index()

    predictions
    return (predictions,)


@app.cell
def _(predictions):
    import os.path
    import pathlib

    submission_filepath = pathlib.Path(
        f"./submissions/{os.path.splitext(os.path.basename(__file__))[0]}.csv"
    )
    print(f"saving submission file to {submission_filepath}")
    predictions.to_csv(submission_filepath)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
