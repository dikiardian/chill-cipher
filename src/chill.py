import numpy as np
import random

BLOCK_SIZE = 16 # bytes

class Chill:
  def __init__(self, plain_text_src = 'text', plain_text = '', plain_text_path = '', key = 'key'):
    # constructor
    self.key = key
    self.plain_text = plain_text
    self.plain_text_path = plain_text_path
    self.plain_text_src = plain_text_src # ['text', 'file']
    self.cipher_text = ''

  def __to_hex(self, content):
    result = ''
    for c in content:
      result += format(ord(c), '08b')
    return '%08X' % int(result, 2)

  def __plain_padding(self):
    plain_block_size = 2*2*BLOCK_SIZE
    if len(self.plain_text) % plain_block_size != 0:
      padd_length = (plain_block_size - (len(self.plain_text) % plain_block_size)) / 2

    padd_char = '%02X' % padd_length

    for i in range(0, padd_length):
      self.plain_text += padd_char

  def __key_padding(self):
    key_length = len(self.key)
    if key_length == 2*BLOCK_SIZE:
      pass
    elif key_length < 2*BLOCK_SIZE:
      seed = 0
      for idx, k in enumerate(self.key):
        if (idx % 2 == 1):
          seed += ord(k)
      random.seed(seed)
      while len(self.key) < 2*BLOCK_SIZE:
        pos = random.randrange(0, key_length)
        self.key += self.key[pos]
    else:
      seed = 0
      for idx, k in enumerate(self.key):
        if (idx % 2 == 0):
          seed += ord(k)
      random.seed(seed)
      while len(self.key) > 2*BLOCK_SIZE:
        pos = random.randrange(0, key_length)
        self.key = self.key[:pos] + self.key[(pos+1):]

  def __load_plain_text(self):
    # open file
    with open(self.plain_text_path, mode='rb') as file:
      file_content = file.read()

    return file_content

  def __xor(self, hex_string1, hex_string2):
    return format(int(hex(int(hex_string1, 16) ^ int(hex_string2, 16)), 0), 'X')

  def __round_function(self, right_block, round_key):
    # TODO: transform to matrix
    # TODO: SubX+
    # TODO: L Transposition
    # TODO: ShiftCol
    # TODO: transform to string
    return []

  def __generate_round_key(self, round_key):
    # TODO: transform to matrix
    # TODO: RotMod
    # TODO: SubX-
    # TODO: XorCol
    # TODO: transform to string
    return 0

  def __feistel_encrypt(self, round_time):
    done = False
    idx_left_block = BLOCK_SIZE
    idx_right_block = 0
    round_key = self.key
    right_block = self.plain_text[idx_right_block:idx_right_block+BLOCK_SIZE]
    left_block = self.plain_text[idx_left_block:idx_left_block+BLOCK_SIZE]

    while not done:
      round_idx = 0
      while round_idx < round_time:
        right_block_new = self.__xor(left_block, self.__round_function(right_block, round_key))
        left_block_new = right_block
        right_block = right_block_new
        left_block = left_block_new
        round_key = self.__generate_round_key(round_key)
        round_idx += 1
      # TODO: append to cipher text
      # TODO: update block

  def encrypt(self):
    # get plain text
    if self.plain_text_src == 'file':
      self.plain_text = self.__load_plain_text()

    # get feistel round time
    round_time = 5 + (len(self.key) % 6)
    
    # convert plain text and key to hex
    self.plain_text = self.__to_hex(self.plain_text)
    self.key = self.__to_hex(self.key)

    # padding plain text
    self.__plain_padding()
    # padding key
    self.__key_padding()

    # feistel
    self.__feistel_encrypt(round_time)

  def decrypt(self):
    pass
  