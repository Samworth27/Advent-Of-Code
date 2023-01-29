import itertools
import math
from aoc_util.inputs import parse_input

DAY = 24
YEAR = 2015


def combinations_3(packages):
    target = sum(packages)//3
    print(target)
    for i in range(1, len(packages)-1):
        compartment_1 = [set(x) for x in itertools.combinations(
            sorted(packages, reverse=True), i)]
        for c1 in compartment_1:
            if sum(c1) != target:
                continue
            leftover = packages - c1

            for j in range(1, len(leftover)):
                compartment_2 = [set(x) for x in itertools.combinations(
                    sorted(leftover, reverse=True), j)]
                for c2 in compartment_2:
                    if sum(c2) != target:
                        continue
                    c3 = leftover - c2
                    yield c1, c2, c3


def combinations_4(packages):
    target = sum(packages)//4
    print(target)
    for i in range(1, len(packages)-1):
        compartment_1 = [set(x) for x in itertools.combinations(
            sorted(packages, reverse=False), i)]
        for c1 in compartment_1:
            if sum(c1) != target:
                continue
            leftover_1 = packages - c1
            for j in range(1, len(leftover_1)-1):
                compartment_2 = [set(x) for x in itertools.combinations(
                    sorted(leftover_1, reverse=True), j)]
                for c2 in compartment_2:
                    if sum(c2) != target:
                        continue
                    leftover_2 = leftover_1 - c2
                    for k in range(1,len(leftover_2)-1):
                        compartment_3 = [set(x) for x in itertools.combinations(
                            sorted(leftover_2, reverse=True),k)]
                        for c3 in compartment_3:
                            if sum(c3) != target:
                                continue
                            c4 = leftover_2 - c3
                            yield c1, c2, c3, c4


def qe(compartment):
    return math.prod(compartment)


def part1():
    packages = set(parse_input((DAY, YEAR), int))
    best_qe = float('inf')
    best_length = float('inf')
    for combo in combinations_3(packages):
        c1, c2, c3 = combo
        c1_len = len(c1)
        if c1_len > best_length:
            break
        c1_qe = qe(c1)
        print(c1_qe, best_qe)
        if c1_qe < best_qe:
            best_qe = c1_qe
            best_length = c1_len
    print(best_qe)

def part2():
    packages = set(parse_input((DAY,YEAR), int))
    best_qe = float('inf')
    best_length = float('inf')
    for combo in combinations_4(packages):
        c1, c2, c3, c4 = combo
        c1_len = len(c1)
        if c1_len > best_length:
            break
        c1_qe = qe(c1)
        print(c1_qe, best_qe)
        if c1_qe < best_qe:
            best_qe = c1_qe
            best_length = c1_len
    print(best_qe)
    
part2()
