def retry(f, n, *fargs, **fkwargs):
    for t in range(n):
        try:
            res = f(*fargs, **fkwargs)
            return res
        except ValueError:
            print(f"Failed {t} time(s); trying again {n-t} more time(s).")
            continue
