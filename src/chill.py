import numpy as np
import random

BLOCK_SIZE_IN_BYTE = 16 # bytes
BLOCK_SIZE_IN_HEX = BLOCK_SIZE_IN_BYTE*2 # hex

class Chill:
  def __init__(self, plain_text_src = 'text', plain_text = '', plain_text_path = '', key = 'key'):
    # constructor
    self.key = key
    self.plain_text = plain_text
    self.plain_text_path = plain_text_path
    self.plain_text_src = plain_text_src # ['text', 'file']
    self.cipher_text = ''

    # get plain text from file
    if self.plain_text_src == 'file':
      self.plain_text = self.__load_plain_text()

  def __to_hex(self, content):
    result = ''
    for c in content:
      result += format(ord(c), '08b')
    return '%08X' % int(result, 2)

  def __from_hex(self, content):
    result = ''
    for idx in range (0, len(content), 2):
      c = content[idx]+content[idx+1]
      result += chr(int(c, 16))
    
    return result

  def __plain_padding(self):
    plain_block_size = 2*BLOCK_SIZE_IN_HEX
    if len(self.plain_text) % plain_block_size != 0:
      padd_length = (plain_block_size - (len(self.plain_text) % plain_block_size)) / 2

    padd_char = '%02X' % padd_length

    for i in range(0, padd_length):
      self.plain_text += padd_char

  def __key_padding(self):
    key_length = len(self.key)
    if key_length == BLOCK_SIZE_IN_HEX:
      pass
    elif key_length < BLOCK_SIZE_IN_HEX:
      seed = 0
      for idx, k in enumerate(self.key):
        if (idx % 2 == 1):
          seed += ord(k)
      random.seed(seed)
      while len(self.key) < BLOCK_SIZE_IN_HEX:
        pos = random.randrange(0, key_length)
        self.key += self.key[pos]
    else:
      seed = 0
      for idx, k in enumerate(self.key):
        if (idx % 2 == 0):
          seed += ord(k)
      random.seed(seed)
      while len(self.key) > BLOCK_SIZE_IN_HEX:
        pos = random.randrange(0, key_length)
        self.key = self.key[:pos] + self.key[(pos+1):]

  def __load_plain_text(self):
    # open file
    with open(self.plain_text_path, mode='rb') as file:
      file_content = file.read()

    return file_content

  def __xor(self, hex_string1, hex_string2):
    return format(int(hex(int(hex_string1, 16) ^ int(hex_string2, 16)), 0), '02X')

  def __xor_matrix(self, hex_matrix1, hex_matrix2):
    # matrix size are equal, return matrix
    result = []
    for idx_row, rows in enumerate(hex_matrix1):
      row_result = []
      for idx_col, cols in enumerate(rows):
        row_result.append(self.__xor(hex_matrix1[idx_row][idx_col], hex_matrix2[idx_row][idx_col]))
      result.append(row_result)

    return np.asarray(result)

  def __transform_to_matrix(self, data):
    # data is string, return matrix
    result = np.zeros((4, 4), 'U2')
    result[0, 0] = data[0] + data[1]
    result[0, 1] = data[4] + data[5]
    result[0, 2] = data[6] + data[7]
    result[0, 3] = data[18] + data[19]
    result[1, 0] = data[2] + data[3]
    result[1, 1] = data[8] + data[9]
    result[1, 2] = data[16] + data[17]
    result[1, 3] = data[20] + data[21]
    result[2, 0] = data[10] + data[11]
    result[2, 1] = data[14] + data[15]
    result[2, 2] = data[22] + data[23]
    result[2, 3] = data[28] + data[29]
    result[3, 0] = data[12] + data[13]
    result[3, 1] = data[24] + data[25]
    result[3, 2] = data[26] + data[27]
    result[3, 3] = data[30] + data[31]

    return result

  def __transform_to_string(self, input):
    # input is matrix, return string
    result = input[0, 0] + input[1, 0] + input[0, 1] + input[0, 2] + input[1, 1] + input[2, 0] + input[3, 0] + input[2, 1] + input[1, 2] + input[0, 3] + input[1, 3] + input[2, 2] + input[3, 1] + input[3, 2] + input[2, 3] + input[3, 3]
    
    return result

  def __subX(self, mode, input):
    # input is matrix
    # return matrix
    result = np.copy(input)
    for idx_row, rows in enumerate(result):
      for idx_col, cols in enumerate(rows):
        if mode == 'plus':
          int_result = ((int(result[idx_row][idx_col][0]+'0', 16) - 16) % 256) + ((int(result[idx_row][idx_col][1], 16) - 1) % 16)
        else: # mode == 'minus'
          int_result = ((int(result[idx_row][idx_col][0]+'0', 16) - 16) % 256) - ((int(result[idx_row][idx_col][1], 16) - 1) % 16)
        result[idx_row][idx_col] = format(int(hex(int_result), 0), '02X')

    return result

  def __l_transposition(self, input):
    # input is matrix
    # return matrix
    result = np.copy(input)
    result[0, 0], result[3, 1] = result[3, 1], result[0, 0]
    result[0, 1], result[3, 0] = result[3, 0], result[0, 1]
    result[0, 2], result[3, 3] = result[3, 3], result[0, 2]
    result[0, 3], result[3, 2] = result[3, 2], result[0, 3]
    result[1, 0], result[2, 3] = result[2, 3], result[1, 0]
    result[2, 0], result[1, 3] = result[1, 3], result[2, 0]
    result[1, 1], result[2, 2] = result[2, 2], result[1, 1]

    return result

  def __shift_col(self, input):
    # input is matrix
    # return matrix
    sum_col = [0, 0, 0, 0]
    for idx_row, rows in enumerate(input):
      for idx_col, cols in enumerate(rows):
        sum_col[idx_col] += int(input[idx_row][idx_col], 16)
    result_temp = np.copy(input.T)
    # shift
    result = []
    for idx_row, rows in enumerate(result_temp):
      if idx_row % 2 == 1:
        result.append(np.roll(rows, sum_col[idx_row] % 4))
      else:
        result.append(np.roll(rows, (sum_col[idx_row] % 4) * -1))
    return np.asarray(result).T

  def __rot_mod(self, key, key_length):
    # key is matrix, return matrix
    return np.rot90(key, -1 * (key_length % 4))

  def __xor_col(self, input):
    # input is matrix, return matrix
    result = np.copy(input)
    for idx_row, rows in enumerate(input):
      idx_col2 = 1
      for idx_col1, cols in enumerate(rows):
        result[idx_row][idx_col1] = self.__xor(input[idx_row][idx_col1], input[idx_row][idx_col2])
        if idx_col2 == len(rows)-1:
          idx_col2 = 0
        else:
          idx_col2 += 1

    return result

  def __round_function(self, right_block, round_key):
    # right_block and round_key are matrix
    # return matrix

    # SubX+
    result = self.__subX('plus', right_block)
    # L Transposition
    result = self.__l_transposition(result)
    # ShiftCol
    result = self.__shift_col(result)
    # XOR with key
    result = self.__xor_matrix(result, round_key)

    return result

  def __generate_round_key(self, round_key, key_length):
    # round_key is matrix, return matrix

    # RotMod
    result = self.__rot_mod(round_key, key_length)
    # SubX-
    result = self.__subX('minus', result)
    # XorCol
    result = self.__xor_col(result)
    
    return result

  def __feistel_encrypt(self, original_key_length):
    # init key
    round_key = self.key
    round_key_matrix = self.__transform_to_matrix(round_key)

    # get feistel round time
    round_time = 5 + (original_key_length % 6)

    # init feistel loop
    done = False
    idx_left_block = BLOCK_SIZE_IN_HEX
    idx_right_block = 0
    processed_block = 2

    while not done:
      # init round
      round_idx = 0
      right_block = self.plain_text[idx_right_block:idx_right_block+BLOCK_SIZE_IN_HEX]
      right_block_matrix = self.__transform_to_matrix(right_block)
      left_block = self.plain_text[idx_left_block:idx_left_block+BLOCK_SIZE_IN_HEX]
      left_block_matrix = self.__transform_to_matrix(left_block)

      while round_idx < round_time:        
        right_block_matrix_new = self.__xor_matrix(left_block_matrix, self.__round_function(right_block_matrix, round_key_matrix))
        left_block_matrix_new = np.copy(right_block_matrix)
        right_block_matrix = np.copy(right_block_matrix_new)
        left_block_matrix = np.copy(left_block_matrix_new)

        round_key_matrix = self.__generate_round_key(round_key_matrix, original_key_length)
        round_idx += 1

      self.cipher_text += self.__transform_to_string(right_block_matrix) + self.__transform_to_string(left_block_matrix)

      if processed_block == (len(self.plain_text) / BLOCK_SIZE_IN_HEX):
        done = True
      else:
        idx_left_block += 2*BLOCK_SIZE_IN_HEX
        idx_right_block += 2*BLOCK_SIZE_IN_HEX
        processed_block += 1

    # remove '-' char if exist
    self.cipher_text = self.cipher_text.replace('-', '')

  def encrypt(self):
    # get original key length before padding
    original_key_length = len(self.key)

    # convert plain text and key to hex
    self.plain_text = self.__to_hex(self.plain_text)
    self.key = self.__to_hex(self.key)

    # padding plain text
    self.__plain_padding()
    # padding key
    self.__key_padding()

    # feistel
    self.__feistel_encrypt(original_key_length)

    # convert cipher text from hex to string
    self.cipher_text = self.__from_hex(self.cipher_text)

  def decrypt(self):
    pass
  