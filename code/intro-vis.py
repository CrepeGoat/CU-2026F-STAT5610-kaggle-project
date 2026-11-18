import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # setup
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import seaborn as sns

    return np, sns


@app.cell
def _():
    from kaggle_api import fetch_dataset

    df_train, df_test = fetch_dataset()
    return (df_train,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # data formatting
    """)
    return


@app.cell
def _(df_train):
    cols_categorical = "x4 x5 x10 Y".split()
    for _col in cols_categorical:
        df_train[_col] = df_train[_col].astype("category")
    return (cols_categorical,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # summary stats
    """)
    return


@app.cell
def _(cols_categorical, df_train, mo):
    mo.output.append(df_train.describe())
    mo.output.append(df_train.head())
    for _col in cols_categorical:
        mo.output.append(df_train[_col].value_counts())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # categorical interactions
    """)
    return


@app.cell
def _(cols_categorical, df_train, mo):
    for _col in cols_categorical[:-1]:
        mo.output.append(
            df_train.loc[df_train["Y"] == 1, _col].value_counts()
            / df_train[_col].value_counts()
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `x5:2` seems to be correlated with a higher response rate, where `x5:0, x5:1` seem to correlate with a lower response rate
    - `x4` and `x10` seem to have little interaction with `Y`
    """)
    return


@app.cell
def _(cols_categorical, df_train, mo):
    mo.output.append(
        df_train.loc[df_train["Y"] == 1, cols_categorical[:-1]].value_counts()
        / df_train[cols_categorical[:-1]].value_counts()
    )
    # mo.output.append(df_train[cols_categorical].value_counts())
    mo.output.append(min(df_train[cols_categorical[:-1]].value_counts()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## napkin math

    -> from the table:
    - `x4, x5, x10` move the average `Y` rate from ~0.24 to ~0.35
    - `Y`'s rate is notably highest at 0.352 for `x4=0, x5=2, x10=2`
    - `Y`'s rate is notably lowest at 0.248 for `x4=1, x5=0, x10=2`
    - there are some $3+$-variable interactions among the categorical variables `x4, x5, x10, Y`; some of these interactions may be significant
        - $Y \mid X_i$ can be considered a Bernoulli variable, with dependence on the predictors $X_i$
        - -> the variance of a Bernoulli is $\sigma^2 := p (1 - p)$, where $p$ is the average
        - each set of predictor value combinations has at least 442 samples (see printed value above)
        - -> the variance of the average of these values would be $\frac{\sigma^2}{n} < \frac{\sigma^2}{442} < \frac{(1/4)}{442} \approx 5.656 \times 10^{-4}$
        - -> the standard deviation of these would be $\approx \sqrt{\frac{\sigma^2}{n}} < 0.0238$
        - a 95% CI generally considers values within $\sim \pm 1.96 \sigma \approx 0.0476$ of the sample mean
            - (this is true of normal distributions; here we use it as a rule-of-thumb for easy math)
        - => any two sample means above that are more than $\sim 0.0951$ apart are likely statistically significantly different
        - the difference between the largest and smallest values exceeds this threshold: $0.351695 - 0.247682 \approx 0.1040 > 0.0951$ -> there is likely some significance here
        - however, the differences between most of the value pairs are within this threshold -> much of the variation may not be significant
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # correlation table
    """)
    return


@app.cell
def _(df_train, mo):
    mo.output.append(df_train.corr())
    return


@app.cell
def _(df_train, mo, sns):
    mo.output.append(
        sns.heatmap(
            df_train.corr() * 100,
            cmap=sns.color_palette("vlag_r", as_cmap=True),
            center=0,
            annot=True,
            fmt=".0f",
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    -> from the table:

    - `x1`, `x9` are highly correlated - 0.747
    - `Y` is most highly correlated with `x1`, followed by `x9`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # plots - response vs. single predictor
    """)
    return


@app.cell
def _(cols_categorical, df_train, mo, sns):
    for _col in df_train.columns:
        if _col in cols_categorical:
            continue
        mo.output.append(sns.displot(df_train, x=_col, hue="Y"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `x1` has a notable imbalance to it; specifically, it bears the general normal-distribution shape, but has a piecewise-looking divide about $x_1 = 0$
    - `x3` has a skewed shape to it, almost like a [Gamma distribution](https://en.wikipedia.org/wiki/Gamma_distribution)
    - `x2` and `x9` have some asymmetry about zero
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # $X_1$ as a binary classifier
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    TODO take `x1`, then:
    - take some portion of the points where $x_1 > 0, Y = 1$ and set $Y = 0$
    - then do the same for $x_1 < 0, Y = 0$, setting $Y = 1$

    -> check: do we get effectively a normal distribution for both $Y$ values?
    """)
    return


@app.cell
def _(cols_categorical, df_train, mo):
    df_train["x11"] = (df_train.x1 > 0).astype("category")
    cols_categorical.insert(-2, "x11")

    mo.output.append(
        df_train.loc[df_train["Y"] == 1, "x11"].value_counts()
        / df_train["x11"].value_counts()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    -> discretizing `x11` produces a result much stronger than any of the other categorical predictors, with a prediction range of $[0.14, 0.41]$.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ❌ transform $X_3$
    """)
    return


@app.cell
def _(df_train, mo, np, sns):
    mo.output.append(sns.displot(x=np.log(df_train.x3 + 2), hue=df_train.Y))
    mo.output.append(sns.displot(x=np.cbrt(df_train.x3 + 2), hue=df_train.Y))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    we can try to "even out" `x3`, but it still doesn't quite look right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # predictor interactions via pairwise plots
    """)
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train)
    _g.map_offdiag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train, hue="Y")
    _g.map_offdiag(sns.histplot)
    _g.map_diag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## $x_7$
    """)
    return


@app.cell
def _(df_train, mo, sns):
    mo.output.append(
        sns.jointplot(
            df_train,
            x="x1",
            y="x7",
            hue="Y",
            kind="kde",
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **-> $x_1, x_7$ seem to have some multivariate interaction w.r.t. $y$**
    """)
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train["x1 x2 x3 x7 x9 Y".split()], hue="Y", kind="kde")
    _g.map_diag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


@app.cell
def _(df_train, mo, sns):
    mo.output.append(
        sns.jointplot(
            df_train,
            x="x2",
            y="x7",
            hue="Y",
            kind="kde",
        )
    )
    return


@app.cell
def _(df_train, mo, sns):
    mo.output.append(
        sns.jointplot(
            df_train,
            x="x9",
            y="x7",
            hue="Y",
            kind="kde",
        )
    )
    return


@app.cell
def _(df_train, mo, sns):
    mo.output.append(
        sns.jointplot(
            df_train,
            x="x7",
            y="x3",
            hue="Y",
            kind="kde",
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $x_7$ generally has some interactions with $x_1, x_2, x_3, x_9$ w.r.t. $y$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## categorical predictors are independent from numerical predictors
    """)
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train, hue="x4")
    _g.map_offdiag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train, hue="x5")
    _g.map_offdiag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train, hue="x10")
    _g.map_offdiag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    -> in all of the above pair plots:
    - the diagonal distribution plots are invariant w.r.t. the categorical predictor
    - the off-diagonal plots show no asymmetry in colors

    **-> the categorical predictors seem to be independent of the numerical predictors**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # conditional distributions $\mid y = 0$
    """)
    return


@app.cell
def _(df_train, mo, sns):
    mo.output.append(
        sns.heatmap(
            df_train[df_train.Y == 0].corr() * 100,
            cmap=sns.color_palette("vlag_r", as_cmap=True),
            center=0,
            annot=True,
            fmt=".0f",
        )
    )
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train[df_train.Y == 0], kind="kde")
    # g.map_offdiag(sns.kdeplot)
    _g.map_diag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # conditional distributions $\mid y = 1$
    """)
    return


@app.cell
def _(df_train, mo, sns):
    mo.output.append(
        sns.heatmap(
            df_train[df_train.Y == 1].corr() * 100,
            cmap=sns.color_palette("vlag_r", as_cmap=True),
            center=0,
            annot=True,
            fmt=".0f",
        )
    )
    return


@app.cell
def _(df_train, mo, sns):
    _g = sns.pairplot(df_train[df_train.Y == 1], kind="kde", hue="Y")
    # g.map_offdiag(sns.kdeplot)
    _g.map_diag(sns.histplot)
    # g.map_lower(sns.kdeplot, fill=True)
    mo.output.append(_g)
    return


if __name__ == "__main__":
    app.run()
