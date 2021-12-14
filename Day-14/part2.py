"""
--- Part Two ---
The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
"""

import os
from collections import defaultdict
from typing import Callable


class LetterFreq:
    def __init__(self, letter, frequency):
        self.letter = letter
        self.frequency = frequency

    def __repr__(self):
        return f"{self.letter}:{self.frequency}"


class memoized_property(object):
    """
    Decorator to create a memoized property that will be retreived
    from cache if the class instance has not changed
    """

    def __init__(self, factory: Callable):
        self._attr_name = factory.__name__
        self._factory = factory
        self._value = None
        self._instance_hash = None

    def __get__(self, instance: object, owner: type):
        # Check if the instance has changed
        if instance.__hash__() != self._instance_hash:
            # Update the instance hash
            self._instance_hash = instance.__hash__()
            # Call the method to get the value
            self._value = self._factory(instance)
        return self._value


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

    @memoized_property
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

    def most_common_letter(self) -> LetterFreq:
        """
        Returns the most common letter in the polymer.

        Returns:
            tuple: (element, frequency)
        """
        max_letter = max(self.letter_frequencies.items(), key=lambda x: x[1])
        return LetterFreq(letter=max_letter[0], frequency=max_letter[1])

    def least_common_letter(self) -> LetterFreq:
        """
        Returns the least common letter in the polymer.

        Returns:
            tuple: (element, frequency)
        """
        min_letter = min(self.letter_frequencies.items(), key=lambda x: x[1])
        return LetterFreq(letter=min_letter[0], frequency=min_letter[1])

    def __repr__(self):
        return self.__polymer_string

    def __hash__(self):
        return hash(tuple(self.__pair_frequencies.items()))

    @classmethod
    def from_file(cls, file_path: str) -> "Polymer":
        """
        Creates a polymer from a file where the first line is the polymer
        template and the following lines (starting from line 3) are the
        rules in the form of "XX -> Y"

        Args:
            file_path (str): Path to the file.
        """

        with open(file_path) as f:
            data = f.read().splitlines()

        polymer_string = data[0]

        rules = {}
        for rule in data[2:]:
            before, after = rule.split(" -> ")
            rules[before] = after

        return cls(polymer_string, rules)


def main():
    filename = os.path.join(os.path.dirname(__file__), "input.txt")

    polymer = Polymer.from_file(filename)

    polymer.advance(40)

    most_common = polymer.most_common_letter()
    least_common = polymer.least_common_letter()

    print(most_common.frequency - least_common.frequency)


if __name__ == "__main__":
    main()
