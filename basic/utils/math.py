import traceback

class TailRecursionException(Exception):
    def __init__(self, args):
        self.args = args

def recursingInFn(fnName):
    stack = traceback.extract_stack()
    stackFnNames = list(reversed([ frameSummary.name for frameSummary in stack ]))
    return stackFnNames.count(fnName) > 1

def tailRecursionWithExceptions(f):
    def g(*args):
        while True:
            if recursingInFn(f.__name__):
                raise TailRecursionException(args)
            else:
                try:
                    return f(*args)
                except TailRecursionException as e:
                    args = e.args
    return g

@tailRecursionWithExceptions
def fact(n, tally=1):
    # This version is changed so that it does use tail recursion!
    if n == 0:
        return tally
    else:
        return fact(n-1, n*tally)