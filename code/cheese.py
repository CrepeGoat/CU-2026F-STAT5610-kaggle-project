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


def demo_iter_branch_lr():
    n = 22

    for i, lrrange in enumerate(iter_branch_lr(n)):
        print(f"{i}: {str_range(n, *lrrange)}")


if __name__ == "__main__":
    demo_iter_branch_lr()
