"""
--- Day 14: Extended Polymerization ---
The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H occurs 191 times, and N occurs 865 times; taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
"""

import os
from collections import defaultdict


class LetterFreq:
    def __init__(self, letter, frequency):
        self.letter = letter
        self.frequency = frequency

    def __repr__(self):
        return f"{self.letter}:{self.frequency}"


class Polymer:
    def __init__(self, polymer_string: str, rules: dict[str, str]):
        self.__polymer_string = polymer_string
        self.__rules = rules
        # initialize pair frequencies
        self.__pair_frequencies = defaultdict(int)
        for i in range(len(polymer_string) - 1):
            pair = polymer_string[i : i + 2]
            assert pair in rules
            self.__pair_frequencies[pair] += 1

    def advance(self, steps: int = 1):
        """
        Advances the polymer by the given number of steps.

        Args:
            steps (int): Number of steps to advance the polymer.
        """
        for _ in range(steps):
            # keep track of the frequency of each pair
            new_frequencies = defaultdict(int)
            for pair, freq in self.__pair_frequencies.items():
                new_frequencies[f"{pair[0]}{self.__rules[pair]}"] += freq
                new_frequencies[f"{self.__rules[pair]}{pair[1]}"] += freq
            self.__pair_frequencies = new_frequencies

    def letter_frequencies(self) -> dict[str, int]:
        """
        Returns the frequency of each letter in the polymer.

        Returns:
            dict[str, int]: Dictionary of letter frequencies.
        """
        letter_frequencies = defaultdict(int)
        for pair in self.__pair_frequencies:
            letter_frequencies[pair[0]] += self.__pair_frequencies[pair]
        letter_frequencies[self.__polymer_string[-1]] += 1
        return letter_frequencies

    def most_common_element(self) -> LetterFreq:
        """
        Returns the most common letter in the polymer.

        Returns:
            tuple: (element, frequency)
        """
        letter_frequencies = self.letter_frequencies()
        max_letter = max(letter_frequencies.items(), key=lambda x: x[1])
        return LetterFreq(max_letter[0], max_letter[1])

    def least_common_element(self) -> LetterFreq:
        """
        Returns the least common letter in the polymer.

        Returns:
            tuple: (element, frequency)
        """
        letter_frequencies = self.letter_frequencies()
        min_letter = min(letter_frequencies.items(), key=lambda x: x[1])
        return LetterFreq(min_letter[0], min_letter[1])

    def __repr__(self):
        return self.__polymer_string

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path) as f:
            data = f.read().splitlines()

        polymer_string = data[0]
        rules = data[2:]

        rule_dict = {}
        for rule in rules:
            before, after = rule.split(" -> ")
            rule_dict[before] = after

        return cls(polymer_string, rule_dict)


def main():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")

    polymer = Polymer.from_file(filename)

    polymer.advance(40)

    most_common = polymer.most_common_element()
    least_common = polymer.least_common_element()

    print(most_common.frequency - least_common.frequency)


if __name__ == "__main__":
    main()