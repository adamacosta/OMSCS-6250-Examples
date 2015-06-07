import re
from numpy import binary_repr
from bitarray import bitarray


class IP:
	def __init__(self, addr):
		assert(re.match('([0-9]{1,3}\.){3}[0-9]{1,3}', addr))
		self.ip = addr
		self.bits = bitarray()
		for octet in list(map(int, self.ip.split('.'))):
			self.bits.extend(bitarray(binary_repr(octet, width=8)))

	def tostring(self):
		return self.ip

	def tobits(self):
		return ''.join(self.bits.decode({'1':bitarray('1'), 
			                             '0':bitarray('0')}))

	def lpm(self, other):
		assert(isinstance(other, CIDRBlock))
		if (self.bits ^ other.ip.bits).index(True) >= other.mask:
			return other.mask
		else:
			return 0

class CIDRBlock:
	def __init__(self, addr):
		assert(re.match('([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{2}', addr))
		self.ip = IP(addr.split('/')[0])
		self.mask = int(addr.split('/')[1])

	def tostring(self):
		return self.ip.tostring() + '/' + str(self.mask)

	def tobits(self):
		return self.ip.tobits()

	def matches(self, other):
		assert(isinstance(other, IP))
		return self.ip.tobits()[:self.mask] == other.tobits()[:self.mask]

class trie:
	# TODO: implement a trie
	pass

def ip_parser(addr):
	if re.match('([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{2}', addr):
		return CIDRBlock(addr)
	if re.match('([0-9]{1,3}\.){3}[0-9]{1,3}', addr):
		return IP(addr)
	raise TypeError('Not a proper IP address')