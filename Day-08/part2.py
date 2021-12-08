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


def check_mapping(mapping: dict[str, str], wire_map: dict[str, str]) -> bool:
    """
    Check if mapping contradicts wire_map.

    Args:
        mapping (dict[str, str]): mapping that is being attempted
        wire_map (dict[str, str]): mapping that must not be contradicted

    Returns:
        True if mapping does not contradict wire_map
    """
    # Check that all wires in mapping don't map to something else in wire_map
    for unknown, match in mapping.items():
        if unknown in wire_map.keys() and wire_map[unknown] != match:
            return False
    # Check that all wires mapped to in mapping aren't mapped to by something else in wire_map
    for unknown, match in wire_map.items():
        if match in mapping.values() and mapping.get(unknown, "") != match:
            return False
    return True


def substitute(pattern: str, mapping: dict[str, str]) -> str:
    """
    Substitute each character in pattern with the corresponding value in mapping and sort alphabetically

    Args:
        pattern (str): pattern to be substituted
        mapping (dict[str, str]): mapping of letters to letters in standard configuration

    Returns:
        The substituted pattern.
    """
    return "".join(sorted(mapping[char] for char in pattern))


def identify_digits(
    patterns: dict[int, str],
    unknown_patterns: list[str],
    wire_map: dict[str, str],
    identified: list[int],
) -> list[str]:
    """
    Given a list of patterns, recursively identify which digits correspond to which patterns with backtracking.

    Args:
        patterns (dict[int, str]): mapping of digit to pattern in standard configuration
        unknown_patterns (list[str]): list of patterns that have not yet been identified
        wire_map (dict[str, str]): mapping of letters to letters in standard configuration
        identified (list[int]): list of digits that have already been identified

    Returns:
        list of digits that correspond to the unknown patterns
    """
    if not unknown_patterns:
        return identified

    unidentifed_patterns = {
        num: pattern for num, pattern in patterns.items() if num not in identified
    }

    unknown_pattern = unknown_patterns[0]

    for num, pattern in unidentifed_patterns.items():
        if len(pattern) == len(unknown_pattern):
            unknown_wires = [w for w in unknown_pattern if w not in wire_map.keys()]
            unknown_in_pattern = [w for w in pattern if w not in wire_map.values()]
            for perm in itertools.permutations(unknown_wires):
                mapping = {
                    **dict(zip(unknown_wires, perm)),
                    **dict(zip(perm, unknown_in_pattern)),
                }
                # check if permutation is valid
                if not check_mapping(mapping, wire_map):
                    continue
                # check if mapping contradicts wire_map
                if substitute(unknown_pattern, {**wire_map, **mapping}) != pattern:
                    continue
                identified_copy = identified.copy()
                # recursively identify digits
                identified = identify_digits(
                    patterns,
                    unknown_patterns[1:],
                    {**wire_map, **mapping},
                    identified + [num],
                )
                if identified:
                    return identified
                identified = identified_copy

    return []


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
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "abdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg",
    }

    total = 0

    for line in data:
        before, after = line.split(" | ")
        before = before.split()
        after = after.split()
        # sort each pattern alphabetically
        before = sorted(["".join(sorted(p)) for p in before], key=len)
        identified = identify_digits(patterns, before, {}, [])
        code = dict(zip(before, identified))
        output = ""
        for pattern in after:
            pattern = "".join(sorted(pattern))
            output += str(code[pattern])
        total += int(output)

    print(total)


if __name__ == "__main__":
    main()
