"""
--- Part Two ---
Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
So, the unique signal patterns would correspond to the following digits:

acedgfb: 8
cdfbe: 5
gcdfa: 2
fbcad: 3
dab: 7
cefabd: 9
cdfgeb: 6
eafb: 4
cagedb: 0
ab: 1
Then, the four digits of the output value can be decoded:

cdfeb: 5
fcadb: 3
cdfeb: 5
cdbaf: 3
Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

fdgacbe cefdb cefbgd gcbe: 8394
fcgedb cgb dgebacf gc: 9781
cg cg fdcagb cbg: 1197
efabcd cedba gadfec cb: 9361
gecf egdcabf bgf bfgea: 4873
gebdcfa ecba ca fadegcb: 8418
cefg dcbef fcge gbcadfe: 4548
ed bcgafe cdgba cbgef: 1625
gbdfcae bgc cg cgb: 8717
fgae cfgab fg bagce: 4315
Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?
"""

import os
import itertools
from typing import Optional


def alpha_sort(pattern: str) -> str:
    """
    Sort the pattern alphabetically

    Args:
        pattern (str): pattern to be sorted

    Returns:
        The sorted pattern.
    """
    return "".join(sorted(pattern))


def substitute(pattern: str, mapping: dict[str, str]) -> str:
    """
    Substitute each character in the pattern with the corresponding value in the mapping and sort alphabetically

    Args:
        pattern (str): pattern to be substituted
        mapping (dict[str, str]): mapping of letters

    Returns:
        The substituted pattern.
    """
    return alpha_sort(mapping[char] for char in pattern)


def identify_digits(
    patterns: dict[int, str],
    unknown_patterns: list[str],
    wire_map: dict[str, str],
    identified: list[str],
) -> Optional[list[str]]:
    """
    Given a list of patterns, recursively identify which digits correspond to which patterns with backtracking.

    Args:
        patterns (dict[int, str]): mapping of digit to pattern in standard configuration
        unknown_patterns (list[str]): list of patterns that have not yet been identified
        wire_map (dict[str, str]): mapping of letters to letters in standard configuration
        identified (list[str]): list of digits that have already been identified

    Returns:
        list of digits that correspond to the unknown patterns
    """
    if not unknown_patterns:
        return identified

    # take the first unknown pattern and try to identify it
    unknown_pattern = unknown_patterns[0]

    for num, pattern in patterns.items():
        # skip if the digit has been identified already or the patterns are different lengths
        if num in identified or len(pattern) != len(unknown_pattern):
            continue
        # extract the letters from unknown_pattern that have not been identified yet
        unknown_wires = [w for w in unknown_pattern if w not in wire_map.keys()]
        # extract the letters from pattern that don't have a corresponding wire yet
        unknown_in_pattern = [w for w in pattern if w not in wire_map.values()]
        # skip if the number of unknown wires in the patterns are not equal
        if len(unknown_wires) != len(unknown_in_pattern):
            continue
        for perm in itertools.permutations(unknown_wires):
            mapping = dict(zip(perm, unknown_in_pattern))
            # skip permutation if mapping contradicts wire_map
            if substitute(unknown_pattern, {**wire_map, **mapping}) != pattern:
                continue
            # recursively identify digits
            result = identify_digits(
                patterns,
                unknown_patterns[1:],
                {**wire_map, **mapping},
                identified + [num],
            )
            # if the result is not None, return it, otherwise backtrack
            if result:
                return result

    # if no mapping was found, return None
    return None


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read().splitlines()

    """
    Patterns following the following configuration:

     aaaa 
    b    c
    b    c
     dddd 
    e    f
    e    f
     gggg 
    """
    patterns = {
        "0": "abcefg",
        "1": "cf",
        "2": "acdeg",
        "3": "acdfg",
        "4": "bcdf",
        "5": "abdfg",
        "6": "abdefg",
        "7": "acf",
        "8": "abcdefg",
        "9": "abcdfg",
    }

    total = 0

    for line in data:
        # parse the line
        all_patterns, output_patterns = line.split(" | ")
        all_patterns = all_patterns.split()
        output_patterns = output_patterns.split()

        # sort each pattern alphabetically and sort the list by length
        all_patterns = sorted(map(alpha_sort, all_patterns), key=len)

        # identify digits for each pattern
        identified = identify_digits(patterns, all_patterns, {}, [])
        assert identified is not None

        # map each pattern to its corresponding digit
        code = dict(zip(all_patterns, identified))

        # decode the output pattern
        output = "".join(code[alpha_sort(pattern)] for pattern in output_patterns)

        # add the output value to the total
        total += int(output)

    print(total)


if __name__ == "__main__":
    main()
