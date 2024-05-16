import numpy as np


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def generate_codeword(gen_matrix: np.ndarray, num: int) -> str:
    num_info_bits, num_extra_bits = gen_matrix.shape
    num_extra_bits -= num_info_bits

    bin_str = bin(num)[2:]  # [2:] cuts the "0b" from the beginning
    bin_str = (num_info_bits - len(bin_str)) * "0" + bin_str

    # result matrix has rows from gen_matrix that correspond with the coded message
    result_matrix = np.zeros(gen_matrix.shape, dtype=int)
    for index, row in enumerate(gen_matrix):
        if bin_str[index] == "1":
            result_matrix[index] = row

    result = ""
    for i in range(len(result_matrix[0])):
        temp_sum = np.sum(result_matrix[:, i])
        if temp_sum % 2 == 0:
            result += "0"
        else:
            result += "1"

    return result


def test_matrix(original_matrix: np.ndarray, num_info_bits: int, num_extra_bits: int, num: int,
                desired_hamming_weight=3, show_codewords=False, show_failed_matrices=False):
    # this part tries to construct the Generator matrix G and rejects it if there is some 0 column
    # it assumes that original_matrix will always have only non-zero columns
    matrix: np.ndarray = original_matrix.copy()
    sequence = []
    bin_str = bin(num)[2:]  # [2:] cuts the "0b" from the beginning
    num_places = num_info_bits * num_extra_bits  # how much places in the matrix there is to fill
    bin_str = (num_places - len(bin_str)) * "0" + bin_str
    for bit in bin_str:
        if bit == "1":
            sequence.append(1)
        else:
            sequence.append(0)
    added_part = np.array(sequence)  # part of the Generator array responsible for parity bits
    added_part = np.reshape(added_part, (num_info_bits, num_extra_bits))

    # iterates through added_part's columns and checks if any is only zeroes
    for i in range(len(added_part[0])):
        if np.count_nonzero(added_part[:, i]) == 0:  # if in some COLUMN there are only 0 the matrix is useless
            if show_failed_matrices is True:
                print(f"There is some 0 column! - matrix with num: {num} is useless ")
            return

    matrix[:, num_info_bits:] = added_part
    # if this function came to this point, then there is already constructed the G matrix
    if show_codewords is True:
        print("Rozpoczyna generowanie slow kodowych...\n")
    min_hamming_weight = num_info_bits + num_extra_bits + 1  # it always begins bigger that it has any right to be
    for i in range(2 ** num_info_bits):
        temp_codeword = generate_codeword(matrix, i)
        if show_codewords is True:
            print(temp_codeword)
        if min_hamming_weight > temp_codeword.count("1") > 0:
            min_hamming_weight = temp_codeword.count("1")

    if show_failed_matrices is True and min_hamming_weight < desired_hamming_weight:
        print(f"Minimal Hamming weight is {min_hamming_weight}")
    if min_hamming_weight >= desired_hamming_weight:
        print(f"For number {num} there was achieved desired hamming weight: {min_hamming_weight}")


def main():
    num_info_bits: int = 4
    num_extra_bits: int = 3
    matrix = np.zeros((num_info_bits, num_info_bits + num_extra_bits), dtype=int)
    for i in range(num_info_bits):
        matrix[i, i] = 1
    for i in range(2 ** (num_extra_bits * num_info_bits)):
        test_matrix(matrix, num_info_bits, num_extra_bits, i)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
