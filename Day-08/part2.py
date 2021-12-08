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


def substitute(pattern: str, mapping: dict[str, str]) -> str:
    """
    Substitute each character in pattern with the corresponding value in mapping and sort alphabetically

    Args:
        pattern: The pattern to substitute.
        mapping: The mapping to use.

    Returns:
        The substituted pattern.
    """
    return "".join(sorted(mapping[char] for char in pattern))


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read().splitlines()

    """
    Patterns follow the following configuration:

     aaaa 
    b    c
    b    c
     dddd 
    e    f
    e    f
     gggg 
    """
    patterns = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }

    total = 0

    for line in data:
        ten_patterns, four_digits = line.split(" | ")
        ten_patterns = ten_patterns.split(" ")
        four_digits = four_digits.split(" ")
        # find which of the patterns each corresponds to
        perms = itertools.permutations("abcdefg")
        for perm in perms:
            mapping = dict(zip(perm, "abcdefg"))
            reverse_mapping = {v: k for k, v in mapping.items()}
            # substitute each pattern with the corresponding value
            decoded_set = set(
                substitute(pattern, mapping) for pattern in patterns.keys()
            )
            ten_pattern_set = set("".join(sorted(pattern)) for pattern in ten_patterns)

            if decoded_set == ten_pattern_set:
                # determine which digits each pattern corresponds to
                output = "".join(patterns[substitute(digit, reverse_mapping)] for digit in four_digits)
                total += int(output)

    print(total)


if __name__ == "__main__":
    main()
