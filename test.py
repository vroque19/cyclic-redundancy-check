import sys
from sender_side import encode_data
from receiver_side import is_valid

def main(input_file):
    key = "1101" # Polynomial Generator x^3 + x^2 + 1
    with open(input_file) as f:
        lines = f.readlines()
    for line in lines:
        data = line.strip()  # Remove any whitespace/newlines
        encoded_data = encode_data(data, key)
        print(f"Original Data: {data}")
        print(f"Encoded Data: {encoded_data}")
        print(f"Valid Data: {is_valid(encoded_data, key)}")
        error_data = list(encoded_data)
        error_data[3] = '1' if error_data[3] == '0' else '0'
        error_data = ''.join(error_data)
        
        print(f"Data with error: {error_data}")
        print(f"Valid Data after error: {is_valid(error_data, key)}")
        print("\n")

if __name__ == "__main__":
    main(sys.argv[1])
