#-*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# pip install pycrypto‎
# pip install binascii(python2不用安装，自带)

from Crypto.Cipher import AES
from binascii import hexlify,unhexlify

class prpcrypt(object):
	"""docstring for prpcrypt"""
	def __init__(self, key):
		super(prpcrypt, self).__init__()
		self.key = key
		self.mode = AES.MODE_CBC

	def encrypt(self, text):
		cryptor = AES.new(self.key, self.mode, b'0000000000000000')
		length = 16
		count = len(text)
		if count < length:
			add = (length - count)
			text = text + (' ' * add)
		elif count > length:
			add = (length-(count % length))
			text = text + (' ' * add)
		self.ciphertext = cryptor.encrypt(text)
		# return b2a_hex(self.ciphertext)
		return hexlify(self.ciphertext)

	def decrypt(self, text):
		cryptor = AES.new(self.key, self.mode, b'0000000000000000')
		plain_text = cryptor.decrypt(unhexlify(text))
		return plain_text.rstrip()


if __name__ == '__main__':
	pc = prpcrypt('Czmfbcuw46FtsaOgtrtVn?az96sjiw5R')
	e = pc.encrypt('helloworld')
	d = pc.decrypt(e)
	print("加密：",e)
	print("解密：",d)