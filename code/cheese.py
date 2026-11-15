from pathlib import Path

import numpy as np
import pandas as pd


def _inner_iter_branch_lr(lbound, rbound, lr=True):
    if rbound - lbound >= 1:
        if lr:
            yield (lbound, rbound)
    if rbound - lbound <= 1:
        return

    mid = lbound + ((rbound - lbound) // 2)

    iterl = _inner_iter_branch_lr(lbound, mid, True)
    iterr = _inner_iter_branch_lr(mid, rbound, False)

    try:
        yield next(iterl)
    except StopIteration:
        pass

    fails = 0
    while fails < 2:
        fails = 0
        try:
            yield next(iterl)
        except StopIteration:
            fails += 1
        try:
            yield next(iterr)
        except StopIteration:
            fails += 1

    return


def iter_branch_lr(n):
    yield from _inner_iter_branch_lr(0, n, True)


def str_range(n, lbound, rbound):
    return "".join(["1" if lbound <= i < rbound else "0" for i in range(n)])


def main_demo_iter_branch_lr():
    n = 22

    for i, lrrange in enumerate(iter_branch_lr(n)):
        print(f"{i}: {str_range(n, *lrrange)}")


def np_array_range(n, lbound, rbound):
    result = np.zeros(n, dtype=np.int8)
    result[lbound:rbound] = 1
    return result


def make_prediction_series(df_test_index, preds):
    return pd.Series(preds, index=df_test_index, name="Y")


def iter_write_preds():
    test_path = Path("./data/test.csv")
    df_test = pd.read_csv(test_path, index_col="ID")

    # Kaggle is currently bugging the test data, so its index is truncated
    # -> workaround - start from the first index value, and extend it
    #   by its full untruncated length, which we know in advance

    n = len(df_test.index)
    index = df_test.index
    # index = pd.Series(
    #     np.arange(df_test.index[0], df_test.index[0] + n, dtype=np.int64), name="ID"
    # )

    for i, lrrange in enumerate(iter_branch_lr(n)):
        pred_vals = np_array_range(n, *lrrange)
        preds = make_prediction_series(index, pred_vals)
        preds.to_csv(
            Path(f"./cheese_guesses/guess{i:02}_({lrrange[0]}_{lrrange[1]}).csv")
        )

        yield


def write_preds(n):
    iter_writes = iter_write_preds()

    for _ in range(n):
        next(iter_writes)


if __name__ == "__main__":
    write_preds(40)
