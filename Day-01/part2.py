def sums_of_threes(numbers: list[int]) -> list[int]:
    """Returns the sums of each set of three consecutive numbers in a list."""
    return [sum(numbers[i : i + 3]) for i in range(len(numbers) - 2)]


def count_increasing(numbers: list[int]) -> int:
    """Returns the number of times the sequence of numbers increases."""
    return sum(numbers[i] < numbers[i + 1] for i in range(len(numbers) - 1))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = list(map(int, f.readlines()))

    print(count_increasing(sums_of_threes(data)))
