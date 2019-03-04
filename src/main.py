from chill import Chill
import random

ch = Chill(plain_text_src='file', plain_text_path='../plain.txt', key='kunci gembok kuat')

print ch.plain_text

ch.encrypt()

print ch.cipher_text
