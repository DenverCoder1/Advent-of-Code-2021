"""
--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly, can tell you many useful things about the conditions of the submarine. The first parameter to check is the power consumption.

You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all numbers in the diagnostic report. For example, given the following diagnostic report:

00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010

Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)
"""


def count_frequencies(numbers: list[str]) -> list[dict[str, int]]:
    """
    Count the frequencies of 1's and 0's within each index of the list of numbers

    Args:
        numbers (list[str]): A list of strings representing binary numbers

    Returns:
        list[dict[str, int]]: A list of dictionaries with the frequencies of 1's and 0's
    """
    num_length = len(numbers[0])
    frequencies = [{"0": 0, "1": 0} for _ in range(num_length)]
    for num in numbers:
        for i, digit in enumerate(num):
            frequencies[i][digit] += 1
    return frequencies


def most_common_bits(frequencies: list[dict[str, int]]) -> str:
    """
    Find the most common bits within each index of the list of frequencies

    Args:
        frequencies (list[dict[str, int]]): A list of dictionaries with the frequencies of 1's and 0's

    Returns:
        str: A string representing the most common bits
    """
    return "".join(
        [max(frequencies[i], key=frequencies[i].get) for i in range(len(frequencies))]
    )


def invert_bits(bits: str) -> str:
    """
    Invert the bits within the string

    Args:
        bits (str): A string representing the bits

    Returns:
        str: A string representing the inverted bits
    """
    return "".join(["0" if bit == "1" else "1" for bit in bits])


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read().splitlines()

    # for each of the bits, count the frequency of 1's and 0's
    freqs = count_frequencies(data)

    # build a string of the most common bits
    gamma_rate = most_common_bits(freqs)

    # build a string of the least common bits
    epsilon_rate = invert_bits(gamma_rate)

    # convert the string of bits to decimal and multiply
    print(int(gamma_rate, 2) * int(epsilon_rate, 2))
