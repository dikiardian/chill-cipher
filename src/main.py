from chill import Chill

ch = Chill(plain_text_src='file',
		   plain_text_path='../plain.txt',
		   key='kunci gembok kuad',
		   # mode='ECB',
		   mode='CBC',
		   cipher_text_path= '../cipher.txt')

print '-----------------------------'
print 'Plain text:'
print len(ch.plain_text), ch.plain_text
print '-----------------------------'

ch.encrypt()
print 'Cipher text:'
print len(ch.cipher_text), ch.cipher_text
print '-----------------------------'

# reset plain text for testing
print 'Plain text:'
ch.plain_text = ''
ch.decrypt()
print len(ch.plain_text), ch.plain_text
print '-----------------------------'
