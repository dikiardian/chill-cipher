from chill import Chill
from collections import Counter

ch = Chill(plain_text_src='file',
		   plain_text_path='../plain.txt',
		   key='itbganeshasepulu',
		   # mode='ECB',
		   # mode='CBC',
		   # mode='CFB',
		   # mode='OFB',
		   mode='CTR',
		   cipher_text_path= '../cipher.txt')

p = Counter(ch.plain_text)
print p
for i in range(256):
	print str(i) + '\t' + str(p[chr(i)])
ch.encrypt()
c = Counter(ch.cipher_text)
print c
for i in range(256):
	print str(c[chr(i)])