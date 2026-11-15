def _inner_iter_branch_lr(lbound, rbound, lr=True):
    if rbound - lbound >= 1:
        if lr:
            yield (lbound, rbound)
    if rbound - lbound <= 1:
        return

    mid = lbound + ((rbound - lbound) // 2)
    yield from _inner_iter_branch_lr(lbound, mid, True)
    yield from _inner_iter_branch_lr(mid, rbound, False)

    return


def iter_branch_lr(n):
    yield from _inner_iter_branch_lr(0, n, True)


def str_range(n, lbound, rbound):
    return "".join(["1" if lbound <= i < rbound else "0" for i in range(n)])


def demo_iter_branch_lr():
    n = 16

    for i, lrrange in enumerate(iter_branch_lr(n)):
        print(f"{i}: {str_range(n, *lrrange)}")


if __name__ == "__main__":
    demo_iter_branch_lr()
