import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt  # noqa: F401
    import numpy as np
    import pandas as pd
    import seaborn as sns  # noqa: F401

    return np, pd


@app.cell
def _(np):
    from kaggle_api import fetch_dataset

    df_train, df_test = fetch_dataset()

    for df in (df_train, df_test):
        df.insert(
            1, column="x1a", value=(df.x1 >= 0).astype(np.int8).astype("category")
        )
    return df_test, df_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # https://pygam.readthedocs.io/en/latest/reference/_autosummary/pygam.pygam.LogisticGAM.html

    from pygam import LogisticGAM, f, s, te

    _col_idx = lambda col: df_train.columns.get_loc(col)
    _col_func = lambda col: f if col in "x4 x5 x10 x1a".split() else s
    _col = lambda col: _col_func(col)(_col_idx(col))

    model = LogisticGAM(
        # _col("x1")
        te(_col("x7"), _col("x2"))
        + te(_col("x7"), _col("x3"))
        + te(_col("x4"), _col("x5"), _col("x10"), _col("x1a"))
        + te(_col("x7"), _col("x6"))
        # + _col("x8")
        + te(_col("x7"), _col("x9"))
    )

    mo.output.append(model.terms)
    mo.output.append(model.terms.n_coefs)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    gam = model.fit(df_train.drop("Y", axis=1), df_train.Y)

    mo.output.append(gam.terms)
    mo.output.append(gam.terms.n_coefs)
    gam.summary()
    mo.output.append(gam.statistics_)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # model overview

    - type - GAM logistic regression
    - predictor selection method - manual
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## forward iteration for tensor terms

    goal - devise a procedure for performing forward iteration on GAM's, s.t. it also considers _tensors of predictors_

    note
    - zero-interaction formulas are characterized by a string of bits, one for each predictor - 1 = the predictor is included, 0 = the predictor is not included
    - tensor formulas are characterized by _a set of bit strings_
        - each bit string represents a tensor / additive term
        - no bit string is a subset of another; i.e., `bs1 and bs2 != bs1`
            - if so, the subset term would be redundant with the superset tensor, and would not provide any additional predictive power

    e.g. - suppose we're performing forward selection, and at one step have the following model on a dataset with three predictors:

    ```python
    LogisticGAM(s(0) + s(1))
    ```

    i.e., predictors 0, 1 are in the model, but predictor 2 is not

    -> the next iteration should consider:

    1. the model with predictor 2 - `LogisticGAM(s(0) + s(1) + s(2))`
    2. the model with tensors involving predictor 0 - `LogisticGAM(te(s(0), s(1)))`
    3. the model with tensors involving predictor 1 (generates the same model as 2.)
    4. the model with tensors involving predictor 2:
        - `LogisticGAM(te(s(0), s(2)) + s(1))`
        - `LogisticGAM(s(0) + te(s(1), s(2)))`

    this example highlights some complexity that is not present in zero-interaction forward selection:

    - any tensor set that is a subset of another can be removed w/ no effect
    - including different parameters in tensors can result in the same formula (e.g., 0 and 1)
    - there are potentially multiple ways to include a given predictor into a formula; up to one for each additive term
    """)
    return


@app.cell
def _(df_test, df_train, np):
    import functools
    import itertools
    import operator

    from pygam import LogisticGAM, f, s, te
    from sortedcontainers import SortedList

    _col_idx = lambda col: df_train.columns.get_loc(col)
    _col_func = (
        lambda col: f
        if col in "x4 x5 x10 x1a".split()
        else functools.partial(s, n_splines=5)
    )
    _col = lambda col: _col_func(col)(_col_idx(col))

    def iter_lots(*lots):
        lots_iters = [iter(lot) for lot in lots]
        lots_vals = tuple(next(lot) for lot in lots_iters)

        while True:
            i_next = None
            while i_next is None:
                i_next = yield lots_vals

            assert i_next in range(len(lots))
            try:
                i_next_lot_val = next(lots_iters[i_next])
            except StopIteration:
                return        

            lots_vals = tuple(
                lot if i != i_next else i_next_lot_val
                for i, lot in enumerate(lots_vals)
            )

    def intersect_term(term1, term2):
        result = SortedList([])

        try:
            iter_both = iter_lots(term1, term2)
            while True:
                val1, val2 = next(iter_both)
                if val1 == val2:
                    result.add(val1)
                    iter_both.send(0)
                    iter_both.send(1)
                elif val1 < val2:
                    iter_both.send(0)
                else:
                    iter_both.send(1)
        except StopIteration:
            pass
        return tuple(result)

    def add_col_to_term(terms, i, col):
        if col in terms[i]:
            return None
        result_i = tuple(sorted(list(terms[i]) + [col]))
        result = [term if j != i else result_i for j, term in enumerate(terms)]

        return tuple(
            sorted(
                [
                    term
                    for j, term in enumerate(result)
                    if i == j or intersect_term(term, result_i) != term
                ]
            )
        )

    def add_col_term(terms, col):
        if any(col in term for term in terms):
            return None
        return tuple(sorted(list(terms) + [(col,)]))

    def remove_term(terms, i):
        assert i in range(len(terms))
        return tuple(term for j, term in enumerate(terms) if j != i)

    @functools.cache
    def make_term(col_names):
        assert len(col_names) > 0
        if len(col_names) == 1:
            return _col(col_names[0])
        return te(*(_col(col_name) for col_name in col_names))

    @functools.cache
    def make_formula(terms):
        assert len(terms) > 0
        return functools.reduce(operator.add, (make_term(term) for term in terms))

    @functools.cache
    def score_model_AIC(terms):
        formula = make_formula(terms)
        model = LogisticGAM(formula)
        gam = model.fit(df_train.drop("Y", axis=1), df_train.Y)
        return gam.statistics_["AIC"]

    # _terms: "tuple[tuple[str]]" = (('x1', 'x2', 'x3', 'x6', 'x7'), ('x1a', 'x5', 'x6', 'x7'))
    _terms: "tuple[tuple[str]]" = ()
    _score = np.inf

    for iteration_number in itertools.count():
        print(f"iteration {iteration_number}")
        print(f"terms: {_terms}")
        print(f"AIC: {_score}")

        candidate_terms = (
            [
                x
                for x in (
                    add_col_to_term(_terms, i, col)
                    for col in df_test.columns
                    for i in range(len(_terms))
                )
                if x is not None
            ]
            + [
                x
                for x in (add_col_term(_terms, col) for col in df_test.columns)
                if x is not None
            ]
            + (
                [remove_term(_terms, i) for i in range(len(_terms))]
                if len(_terms) > 1
                else []
            )
        )
        candidate_terms = tuple(tcand for tcand in candidate_terms if tcand != _terms)
        candidate_scores = tuple(score_model_AIC(terms) for terms in candidate_terms)
        i_min = min(enumerate(candidate_scores), key=lambda x: x[1])[0]
        if candidate_scores[i_min] >= _score:
            break
        _terms = candidate_terms[i_min]
        _score = candidate_scores[i_min]
    return LogisticGAM, make_formula


@app.cell
def _(LogisticGAM, df_train, make_formula):
    model = LogisticGAM(
        make_formula((('x1', 'x2', 'x3', 'x6', 'x7'), ('x1a', 'x5', 'x6', 'x7')))
    )

    gam = model.fit(df_train.drop("Y", axis=1), df_train.Y)
    return (gam,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # make prediction
    """)
    return


@app.cell
def _(df_test, gam, pd):
    prediction = gam.predict_proba(df_test)

    prediction_probs = pd.Series(prediction, index=df_test.index)
    prediction_probs.describe()
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
def _(mo, np, pos_prediction_count, prediction_probs, th, threshold):
    rng = np.random.default_rng(1)

    mo.output.append(
        th.plot_f_scores(
            empiricals=th.sample_probable_f_scores(
                rng,
                1000,
                prediction_probs,
                pos_prediction_count,
                # reported score uses 30% of the test data
                report_count=(3 * len(prediction_probs)) // 10,
            ),
            calculated=2 * threshold,
            reported=None,
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## conclusion

    - ✅ the modeled average response rate (mostly) matches the training average
    - the optimal F-score is:
        - larger than the GAM model that doesn't use tensors on $x_7$
        - somewhat low, compared to e.g. random forests
    """)
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
    import os
    import os.path
    import pathlib

    submission_filepath = pathlib.Path(
        f"./submissions/{os.path.splitext(os.path.basename(__file__))[0]}.csv"
    )
    print(f"saving submission file to {submission_filepath}")
    predictions.to_csv(submission_filepath)
    return


if __name__ == "__main__":
    app.run()
