import random
import subprocess
import matplotlib.pyplot as plt
from sender_side import encode_data
from receiver_side import is_valid

def generate_random_binary_string(length):
    return ''.join(random.choice('01') for _ in range(length))

def introduce_random_errors(data, num_errors):
    data_list = list(data)
    for _ in range(num_errors):
        index = random.randint(0, len(data_list) - 1)
        data_list[index] = '1' if data_list[index] == '0' else '0'
    return ''.join(data_list)

def simulate_crc_detection(iterations, data_length, key, num_errors):
    detected_errors = 0
    for _ in range(iterations):
        data = generate_random_binary_string(data_length)
        encoded_data = encode_data(data, key)
        corrupted_data = introduce_random_errors(encoded_data, num_errors)
        if not is_valid(corrupted_data, key):
            detected_errors += 1
    
    # Calculate detection efficiency
    return detected_errors / iterations

def main():
    keys = ["1001", "1101", "100000111", "10001000000100001"]
    iterations = 10000
    data_length = 16
    num_errors_list = range(1, 6)
    
    for key in keys:
      efficiencies = []
      for num_errors in num_errors_list:
            efficiency = simulate_crc_detection(iterations, data_length, key, num_errors)
            efficiencies.append(efficiency)
      # Plotting the results
      plt.figure(figsize=(10, 6))
      plt.plot(num_errors_list, efficiencies, marker='o', linestyle='-', color='b')
      plt.title(f"CRC Error Detection Efficiency, n={iterations}, key={key}")
      plt.xlabel("Number of Errors")
      plt.ylabel("Detection Efficiency")
      plt.grid(True)
      plt.savefig(f"crc_efficiency1_{key}.png")
      # subprocess.run(["code", "crc_efficiency.png"])
      plt.close()
if __name__ == "__main__":
    main()
