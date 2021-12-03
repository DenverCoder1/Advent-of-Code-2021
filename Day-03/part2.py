NUM_LEN = 12

def extract_with_bit(numbers, index, bit_value):
    return [number for number in numbers if number[index] == bit_value]


def count_frequencies(numbers):
    # for each of the NUM_LEN bits, count the frequency of each bit
    freqs = [{"0": 0, "1": 0} for _ in range(NUM_LEN)]

    for number in numbers:
        number = number.strip()
        for i in range(NUM_LEN):
            freqs[i][number[i]] += 1

    return freqs


def most_common_bit(numbers, index):
    freqs = count_frequencies(numbers)
    return "1" if freqs[index]["1"] >= freqs[index]["0"] else "0"

def least_common_bit(numbers, index):
    freqs = count_frequencies(numbers)
    return "0" if freqs[index]["1"] >= freqs[index]["0"] else "1"

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.readlines()

    numbers = [line.strip() for line in data]

    index = 0

    while len(numbers) > 1:
        bit = most_common_bit(numbers, index)
        numbers = extract_with_bit(numbers, index, bit)
        index = (index + 1) % NUM_LEN

    print(numbers)

    num1 = numbers[0]

    numbers = [line.strip() for line in data]

    index = 0

    while len(numbers) > 1:
        bit = least_common_bit(numbers, index)
        numbers = extract_with_bit(numbers, index, bit)
        index = (index + 1) % NUM_LEN
        print(numbers)

    print(numbers)

    num2 = numbers[0]

    # convert num1 and num2 from binary string to decimal
    num1 = int(num1, 2)
    num2 = int(num2, 2)

    # multiply the two numbers
    print(num1 * num2)

