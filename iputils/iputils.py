import re
from numpy import binary_repr
from bitarray import bitarray


def _gen_octet(bits):
	exec('b = ' + '0b' + bits)
	return str(b)

def _bits_to_string(bits):
	return bits.to01()

def _bits_to_dotted_quad(bits):
	return '.'.join(list(map(_gen_octet, [bits[:8].to01(), 
		                                  bits[8:16].to01(), 
	                                      bits[16:24].to01(), 
	                                      bits[24:32].to01()])))

def _dotted_quad_to_bits(quad):
	return bitarray(''.join(list(map(binary_repr,
		                    list(map(int, quad.split('.'))), [8] * 4))))

def _is_valid_ip(addr):
	if not re.match('([0-9]{1,3}\.){3}[0-9]{1,3}', addr):
		return False
	if sum([int(i)<0 or int(i)>255 for i in addr.split('.')]):
		return False
	return True

def _is_valid_cidr(addr):
	if not re.match('([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{2}', addr):
		return False
	if not _is_valid_ip(addr.split('/')[0]):
		return False
	if int(addr.split('/')[1])<0 or int(addr.split('/')[1])>32:
		return False
	return True


class IP:
	"""Return an IP object.

	Attributes
	----------
	bits -- A 32-bit bitarray formed by concatenating the binary 
	    representations of each octet of the IP address.

	Methods
	-------
	getbits() -> bitarray
	tostring() -> string
	tobitstring() -> string
	lpm() -> int
	"""
	def __init__(self, addr):
		"""Initialize an IP object.

		The argument to IP must be a string in dotted quad format
		consisting of four integers in the range 0 to 255, 
		separated by a single dot.
		"""
		if not _is_valid_ip(addr):
			raise TypeError('Not a valid IP')
		self.bits = _dotted_quad_to_bits(addr)

	def getbits(self):
		"""Return the 32-bit bitarray representing the IP address."""
		return self.bits

	def tostring(self):
		"""Return a string representation in dotted quad format."""
		return _bits_to_dotted_quad(self.bits)

	def tobitstring(self):
		"""Return a 32-bit string showing hardware layout of address."""
		return _bits_to_string(self.bits)

	def lpm(self, other):
		"""Return the longest prefix match with a CIDR block."""
		assert(isinstance(other, CIDRBlock))
		if (self.bits ^ other.first).index(True) >= other._mask:
			return other._mask
		else:
			return 0

	def __eq__(self, other):
		return self.getbits() == other.getbits()

class CIDRBlock:
	"""Return a CIDRBlock object.

	Attributes
	----------
	first -- First valid IP address in the range.
	last -- Last valid IP address in the range.
	bitmask -- Bit representation of subnet mask

	Methods
	-------
	tostring() -> string
	getrange() -> (string, string)
	getmask() -> string
	matches() -> boolean
	"""
	def __init__(self, addr):
		"""Initialize a CIDRBlock object.

		The argument to CIDRBlock must be a string in dotted quad format
		consisting of four integers in the range 0 to 255, each separated 
		by a single dot, with a trailing slash and subnet mask length that 
		must be in the range 0 to 32.

		It is possible to pass an invalid CIDR block, e.g. a block with 1
		bits set past the length of the subnet mask, and the constructor 
		will return a valid CIDR block by zeroing all invalid 1 bits.
		"""
		if not _is_valid_cidr(addr):
			raise TypeError('Not a valid CIDR')
		self.first = _dotted_quad_to_bits(addr.split('/')[0])
		self._mask = int(addr.split('/')[1])
		self.bitmask = bitarray('1'*self._mask + '0'*(32 - self._mask))
		self.first &= self.bitmask
		self.last = self.first | ~self.bitmask

	def tostring(self):
		"""Return string representation in CIDR format."""
		return _bits_to_dotted_quad(self.first) + '/' + str(self._mask)

	def getrange(self):
		"""Return the first and last address in the block."""
		return _bits_to_dotted_quad(self.first), _bits_to_dotted_quad(self.last)

	def getmask(self):
		"""Return the subnet mask associated with this CIDR block."""
		return _bits_to_dotted_quad(self.bitmask)

	def matches(self, other):
		"""Return True if IP address is in block."""
		assert(isinstance(other, IP))
		return self.first[:self._mask] == other.getbits()[:self._mask]

	def __eq__(self, other):
		return self.tostring() == other.tostring()

class trie:
	# TODO: implement a trie
	pass

def ip_parser(addr):
	"""Try to parse a string in dotted quad format.

	Arguments
	---------
	addr -- A string representing an IP address.

	Returns
    -------
	IP -- An IP object is returned if the input string has no trailing
	    slash and mask.
	CIDRBlock -- A CIDRBlock object is returned if the input string does
	    have a trailing slash and mask.

	Raises 
    ------
	TypeError if string is not parsable to either format. 
	"""
	if re.match('([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{2}', addr):
		return CIDRBlock(addr)
	if re.match('([0-9]{1,3}\.){3}[0-9]{1,3}', addr):
		return IP(addr)
	raise TypeError('Not a proper IP address')