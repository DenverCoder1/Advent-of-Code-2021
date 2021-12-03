if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = f.readlines()

    # for each of the 12 bits, count the frequency of each bit
    freqs = [{'0': 0, '1': 0} for _ in range(12)]

    for line in data:
        line = line.strip()
        for i in range(12):
            freqs[i][line[i]] += 1

    # build a string of the most common bits
    result = ""
    for freq in freqs:
        result += max(freq, key=freq.get)
    
    # build a string of the least common bits
    result2 = ""
    for freq in freqs:
        result2 += min(freq, key=freq.get)

    # convert the string of bits to an integer
    result = int(result, 2)
    result2 = int(result2, 2)

    # multiply the two numbers
    print(result * result2)