def Consonant(input1, input2):
    input_list = [0 if i in 'aeiou' else 1 for i in input1]

    if sum(input_list) < input2:
        return -1

    index = input2
    start = 0
    while index <= len(input1):
        status, start = validate(input_list, index, input2, start)
        if not status:
            index += 1
        else:
            return index
    return -1


def validate(input_list, index, limit, start):
    for i in range(start, len(input_list) - index):
        if sum(input_list[i: i + index]) < limit:
            return False, i
    return True, 0


if __name__ == "__main__":
    print Consonant("ritikisagoodboy", 4)
