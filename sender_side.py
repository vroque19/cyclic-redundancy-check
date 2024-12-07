import sys

def xor(a, b):
    result = ""
    for i in range(1, len(a)):
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"
    return result

def mod2div(dividend, divisor):
    dividend = list(dividend)
    divisor_len = len(divisor)
    for i in range(len(dividend) - divisor_len + 1):

        if dividend[i] == '1':
            for j in range(divisor_len):
                if divisor[j] == '1':
                    dividend[i+j] = '1' if dividend[i+j] == '0' else '0'
    
    return ''.join(dividend[-(divisor_len-1):])  # Return the last k-1 bits as remainder

def encode_data(data, key):
    k = len(key)
    appended_data = data + '0'*(k-1)
    remainder = mod2div(appended_data, key)
    encoded_data = data + remainder
    return encoded_data

def main():
    # key = "1101" 
  
    # with open(input_file) as f:
    #     data = f.read().strip()
    
   
    # encoded_data = encode_data(data, key)
    # print(f"Original Data: {data}")
    # print(f"Encoded Data: {encoded_data}")

if __name__ == "__main__":
    main()
