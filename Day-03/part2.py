def extract_with_bit(numbers: list[str], index: int, bit_value: str) -> list[str]:
    """
    Extracts the numbers with the given bit value at the given index

    Args:
        numbers (list[str]): The list of numbers
        index (int): The index of the bit
        bit_value (str): The bit value to extract

    Returns:
        list[str]: The list of numbers with the given bit value at the given index
    """
    return [number for number in numbers if number[index] == bit_value]


def count_frequencies(numbers: list[str], index: int) -> dict[str, int]:
    """
    Count the frequencies of 1's and 0's within a specific index of the list of numbers

    Args:
        numbers (list[str]): A list of strings representing binary numbers

    Returns:
        list[dict[str, int]]: A list of dictionaries with the frequencies of 1's and 0's
    """
    frequencies = {"0": 0, "1": 0}
    for num in numbers:
        frequencies[num[index]] += 1
    return frequencies


def most_common_bit(numbers: list[str], index: int) -> str:
    """
    Count the frequencies of 1's and 0's within a specific index of the list of numbers and return the most common bit

    Args:
        numbers (list[str]): A list of strings representing binary numbers
        index (int): The index of the bit

    Returns:
        str: The most common bit value
    """
    freqs = count_frequencies(numbers, index)
    return "1" if freqs["1"] >= freqs["0"] else "0"


def least_common_bit(numbers: list[str], index: int) -> str:
    """
    Count the frequencies of 1's and 0's within a specific index of the list of numbers and return the least common bit

    Args:
        numbers (list[str]): A list of strings representing binary numbers
        index (int): The index of the bit

    Returns:
        str: The least common bit value
    """
    freqs = count_frequencies(numbers, index)
    return "0" if freqs["1"] >= freqs["0"] else "1"


def extract_until_one_remains(numbers: list[str], most_common: bool) -> str:
    """
    Extracts the numbers with the given bit value at the current index until there is only one number left

    The index is incremented by one after each iteration

    Args:
        numbers (list[str]): The list of numbers
        most_common (bool): Whether to extract the most common bit or the least common bit

    Returns:
        str: The remaining number
    """
    index = 0
    while len(numbers) > 1:
        bit_value = (
            most_common_bit(numbers, index)
            if most_common
            else least_common_bit(numbers, index)
        )
        numbers = extract_with_bit(numbers, index, bit_value)
        index += 1
    return numbers[0]


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.read().splitlines()

    oxygen_generator_rating = extract_until_one_remains(data, True)

    co2_scrubber_rating = extract_until_one_remains(data, False)

    # convert to decimal and multiply together
    print(int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2))
