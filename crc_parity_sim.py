from typing import List
import matplotlib.pyplot as plt
import random

def calculate_crc(data: str, polynomial: str) -> str:
    n = len(polynomial)
    padded_data = data + '0' * (n - 1)
    remainder = int(padded_data, 2)
    poly = int(polynomial, 2)
    
    for i in range(len(data)):
        if remainder & (1 << (len(data) + n - 2 - i)):
            remainder ^= poly << (len(data) - 1 - i)
    
    return bin(remainder)[2:].zfill(n - 1)

def encode_message(data: str, polynomial: str) -> str:
    crc = calculate_crc(data, polynomial)
    parity = '0' if data.count('1') % 2 == 0 else '1'
    return data + crc + parity

def introduce_errors(encoded_message: str) -> str:
    encoded_list = list(encoded_message)
    index = random.randint(0, len(encoded_message) - 1)
    encoded_list[index] = '1' if encoded_list[index] == '0' else '0'
    return ''.join(encoded_list)

def check_parity(data: str, group_size: int) -> List[int]:
    groups = [data[i:i+group_size] for i in range(0, len(data), group_size)]
    return [i for i, group in enumerate(groups) if group.count('1') % 2 != 0]

def crc_check(data: str, polynomial: str) -> bool:
    crc_received = data[-len(polynomial)+1:]
    message = data[:-len(polynomial)+1]
    crc_calculated = calculate_crc(message, polynomial)
    return crc_received == crc_calculated

def correct_errors(corrupted_message: str, polynomial: str, group_size: int) -> str:
    """Attempt to correct errors in the corrupted message."""
    main_message = corrupted_message[:-1]  # Exclude parity bit
    parity_bit = corrupted_message[-1]    # Extract parity bit
    error_groups = check_parity(main_message, group_size)
    group_bits = group_size

    # Try correcting errors using parity groups
    corrupted_list = list(main_message)
    for group in error_groups:
        group_start = group * group_bits
        group_end = group_start + group_bits
        for i in range(group_start, group_end):
            # Flip a bit and test CRC validity
            corrupted_list[i] = '1' if corrupted_list[i] == '0' else '0'
            test_message = ''.join(corrupted_list) + parity_bit
            if crc_check(test_message, polynomial):
                print(f"Corrected bit at position {i}.")
                main_message = ''.join(corrupted_list)
                break
            # Revert bit flip if CRC is still invalid
            corrupted_list[i] = '1' if corrupted_list[i] == '0' else '0'

    # Verify and correct parity bit
    if parity_bit != ('0' if main_message.count('1') % 2 == 0 else '1'):
        print("Parity bit mismatch detected. Correcting parity bit.")
        parity_bit = '0' if parity_bit == '1' else '1'

    return main_message + parity_bit


def simulate_error_correction(iterations: int, data_length: int, polynomial: str, group_size: int):
    """Simulate error correction over multiple iterations and plot success rate."""
    success_count = 0
    success_rates = []

    for i in range(1, iterations + 1):
        data = ''.join(random.choice('01') for _ in range(data_length))
        encoded_message = encode_message(data, polynomial)
        corrupted_message = introduce_errors(encoded_message)
        corrected_message = correct_errors(corrupted_message, polynomial, group_size)
        crc_valid = crc_check(corrected_message, polynomial)
        correction_success = crc_valid and corrected_message == encoded_message
        if correction_success:
            success_count += 1

        success_rates.append(success_count / i)

    # Plot results
    plt.plot(range(1, iterations + 1), success_rates, label="Success Rate")
    plt.title(f"Error Correction Success Rate over {iterations} Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Success Rate")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"parity-crc/fig{i}.png")


def main():
    data = "110101"
    polynomial = "1101"
    group_size = 3

    print("Original Data:", data)
    encoded_message = encode_message(data, polynomial)
    print("Encoded Message:", encoded_message)

    corrupted_message = introduce_errors(encoded_message)
    print("Corrupted Message:", corrupted_message)

    corrected_message = correct_errors(corrupted_message, polynomial, group_size)
    print("Corrected Message:", corrected_message)

    crc_valid = crc_check(corrected_message, polynomial)
    print("Final CRC Valid:", crc_valid)
    print("Correction Success:", corrected_message == encoded_message)

    simulate_error_correction(
    iterations=1000,
    data_length=6,       # Length of the data (e.g., 6 bits)
    polynomial="1101",   # Example CRC polynomial
    group_size=3         # Group size for parity check
)
if __name__ == "__main__":
    main()
