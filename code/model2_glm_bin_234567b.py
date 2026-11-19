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

    return np, pd


@app.cell
def _():
    from kaggle_api import fetch_dataset

    df_train, df_test = fetch_dataset()
    return df_test, df_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # model overview

    - type - logistic regression
        - implemented as a GLM under a Binomial family
    - predictor selection method - manual
    """)
    return


@app.cell
def _(df_test, df_train, np):
    cols_categorical = "x4 x5 x10 Y".split()

    df_train["Y"] = df_train["Y"].astype("category")

    for df in (df_train, df_test):
        for _col in cols_categorical[:-1]:
            df[_col] = df[_col].astype("category")

        df["x1a"] = (df.x1 >= 0).astype(np.int8).astype("category")
    return


@app.cell
def _(df_train):
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    _model = smf.glm('Y ~ x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x1a', data=df_train, family=sm.families.Binomial()).fit()

    _model.summary()
    return sm, smf


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    now we remove the insignificant ones ($x_{10}, x_1, x_8, x_9$):

    TODO use forward-backward-lasso to select parameters instead
    """)
    return


@app.cell
def _(df_train, sm, smf):
    model = smf.glm('Y ~ x2 + x3 + x4 + x5 + x6 + x7 + x1a', data=df_train, family=sm.families.Binomial()).fit()

    model.summary()
    return (model,)


@app.cell
def _(df_test, model, pd):
    prediction = model.get_prediction(df_test)

    prediction_probs = pd.Series(prediction.predicted, index=df_test.index)
    return (prediction_probs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # model assessment
    """)
    return


@app.cell
def _(df_train, mo, np, prediction_probs):
    import threshold as th

    pos_prediction_count, threshold = th.estimate_optimal_threshold(prediction_probs)

    mo.output.append(pos_prediction_count)
    mo.output.append(threshold)

    mo.output.append(
        th.plot_probs(
            probs=prediction_probs,
            expt_prob=np.mean(df_train.Y.astype(np.int64)),
            threshold=threshold,
            pos_pred_count=pos_prediction_count,
        )
    )
    return pos_prediction_count, th, threshold


@app.cell
def _(np, pos_prediction_count, prediction_probs, th, threshold):
    rng = np.random.default_rng(1)

    th.plot_f_scores(
        empiricals=th.sample_probable_f_scores(rng, 1000, prediction_probs, pos_prediction_count),
        calculated=2 * threshold,
        reported=None,
    )
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
