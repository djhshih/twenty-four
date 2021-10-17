#!/usr/bin/env python3

# Solve the game of 24
# Rules: Given 4 numbers (1 to 13), find a combination of operations that
#        uses each number once in order to yield the number 24.

import argparse
import itertools

OPS = '+-*/'

# Expression tree
class etree:
    def __init__(self, lchild, rchild, op, value=None):
        self.lchild = lchild   # etree
        self.rchild = rchild   # etree
        self.op = op           # operation (character)
        self.value = value
    def evaluate(self):
        if self.value is None:
            self.value = operate(self.op, self.lchild.evaluate(), self.rchild.evaluate())
        return self.value
    def __str__(self):
        if self.op is None:
            return '%s' % self.value
        else:
            return '(%s %s %s)' % (str(self.lchild), self.op, str(self.rchild))

# Make a leaf node
def eleaf(value):
    return etree(None, None, None, value)

# Perform binary operation `x op y`
# @param op operation ('+', '-', '*', '/')
# @param x  number
# @param y  number
def operate(op, x, y):
    if x is None: return None
    if y is None: return None
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        if y == 0:
            return None
        else:
            return x / y
    else:
        return None


# Given a list of leaves ys, generate a list of all possible trees ts
def enumerate(ys, ts):

    if len(ys) == 1:
        ts.append(ys[0])
        return 

    for values in itertools.permutations(ys, 2):
        for op in '+-*/':
            y = etree(values[0], values[1], op)
            ys_new = [y for y in ys if not y in values]
            ys_new.append(y)
            enumerate(ys_new, ts)

# Find operations on numbers xs that produce the target
def solve_for_target(xs, target):

    # initialize leaves
    ys = [eleaf(x) for x in xs]

    # generate all possible trees
    ts = []
    enumerate(ys, ts)

    # identify trees that evaluate to the target value
    solutions = []
    for tree in ts:
        if tree.evaluate() == target:
            solutions.append(tree)

    return solutions

# Print the solutions if any
def main(numbers, target=24):
    solutions = solve_for_target(numbers, target)
    if solutions == []:
        print('No solution')
    else:
        for s in solutions:
            print('%s = %s' % (str(s), s.evaluate()))


if __name__ == '__main__':

    pr = argparse.ArgumentParser('Solve the 24 game')

    pr.add_argument('numbers', metavar='numbers', type=int, nargs='+',
        help='numbers to solve for the 24 game')

    pr.add_argument('--target', type=int, default=24,
        help='target value [default: 24]')

    argv = pr.parse_args()

    main(argv.numbers, argv.target)
    
