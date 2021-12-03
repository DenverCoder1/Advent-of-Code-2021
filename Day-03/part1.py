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
