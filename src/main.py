from chill import Chill

ch = Chill(plain_text_src='file', plain_text_path='../plain.txt', key='kunci gembok kuat', cipher_text_path= '../cipher.txt')

print ch.plain_text
print len(ch.plain_text)

ch.encrypt()

# reset plain text for testing
ch.plain_text = ''

ch.decrypt()

print ch.plain_text
print len(ch.plain_text)
