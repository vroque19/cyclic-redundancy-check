from sender_side import mod2div, xor

def is_valid(data, key)->bool:
  k = len(key)
  appended_data = data + '0'*(k-1)
  remainder = mod2div(appended_data, key)
  
  if remainder == '0'*(k-1):
    return True
  else:
    return False

