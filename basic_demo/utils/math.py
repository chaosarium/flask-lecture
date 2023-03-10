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
def fact(n: int, tally=1) -> int:
    # This version is changed so that it does use tail recursion!
    if n == 0:
        return tally
    else:
        return fact(n-1, n*tally)
    



# === Cryptarithm solver from class as API ===

from itertools import *

def makeSolutionString(puzzle, map):
    result = [ ]
    for char in puzzle:
        if char.isalpha():
            result.append(str(map[char]))
        else:
            result.append(char)
    return ''.join(result)

def fasterCryptarithm(puzzle):
    # we sure hope it's faster.  It will use backtracking.  Ooooh.
    words = puzzle.replace('=','+').split('+')
    letters = ''.join(sorted(set(''.join(words))))
    colishLetters = list(reversed(getColishLetters(words)))
    firstLetters = ''.join(sorted(set([word[0] for word in words])))
    assignedDigits = set()
    map = dict()
    def solvePuzzleWithBacktracking():
        if len(colishLetters) == 0:
            return map
        else:
            nextLetter = colishLetters.pop()
            for nextDigit in range(10):
                if nextDigit not in assignedDigits:
                    map[nextLetter] = nextDigit
                    assignedDigits.add(nextDigit)
                    if isLegalPartialSolution(words, firstLetters, map):
                        solution = solvePuzzleWithBacktracking()
                        if solution != None:
                            return solution
                    assignedDigits.remove(nextDigit)
                    del map[nextLetter]
            colishLetters.append(nextLetter)
        return None
    if solvePuzzleWithBacktracking() == None:
        return None
    return makeSolutionString(puzzle, map)

def isLegalPartialSolution(words, firstLetters, map):
    # first verify first letters are non-zero
    for letter in firstLetters:
        if (letter in map) and map[letter] == 0:
            return False
    # add colishly from ones digit upwards
    carry = 0
    for col in range(len(words[2])):
        digits = [ ]
        for i in range(3):
            word = words[i]
            if col < len(word):
                letter = word[-1-col]
                if letter not in map:
                    return True
                else:
                    digit = map[letter]
            else:
                digit = 0
            digits.append(digit)
        if ((carry + digits[0] + digits[1])%10) != digits[2]:
            return False
        carry = (carry + digits[0] + digits[1]) // 10
    return True

def getColishLetters(words):
    colishLetters = [ ]
    for col in range(len(words[2])):
        for word in words:
            if col < len(word):
                letter = word[-1-col]
                if letter not in colishLetters:
                    colishLetters.append(letter)
    return colishLetters
