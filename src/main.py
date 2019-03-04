from chill import Chill

ch = Chill(plain_text_src='file',
		   plain_text_path='../plain.txt',
		   key='kunci gembok kuad',
		   cipher_text_path= '../cipher.txt')

print len(ch.plain_text), ch.plain_text
ch.encrypt()
print len(ch.cipher_text), ch.cipher_text
# reset plain text for testing
ch.plain_text = ''

ch.decrypt()
print len(ch.plain_text), ch.plain_text
