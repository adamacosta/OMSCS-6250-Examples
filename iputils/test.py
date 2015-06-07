import unittest
from iputils import *

class TestIPMethods(unittest.TestCase):

	def test_isnotip(self):
		with self.assertRaises(TypeError):
			IP('256.0.0.0')
			IP('0.256.0.0')
			IP('0.0.256.0')
			IP('0.0.0.256')
			IP('192.168.0.1/24')

	def test_getbits(self):
		ip1 = IP('192.168.0.1')
		ip2 = IP('192.168.0.2')
		self.assertEqual(ip1.getbits(),
			             bitarray('11000000101010000000000000000001'))
		self.assertEqual(ip2.getbits(),
			             bitarray('11000000101010000000000000000010'))
		self.assertNotEqual(ip1.getbits(), ip2.getbits())

	def test_tostring(self):
		ip1 = IP('74.125.43.99')
		ip2 = IP('130.68.12.68')
		self.assertEqual(ip1.tostring(), '74.125.43.99')
		self.assertEqual(ip2.tostring(), '130.68.12.68')

	def test_tobitstring(self):
		ip1 = IP('73.148.5.13')
		ip2 = IP('164.79.62.250')
		self.assertEqual(ip1.tobitstring(), 
			             '01001001100101000000010100001101')
		self.assertEqual(ip2.tobitstring(), 
			             '10100100010011110011111011111010')

	def test_lpm(self):
		ip1 = IP('68.211.6.120')
		cidr1 = CIDRBlock('68.211.0.0/17')
		cidr2 = CIDRBlock('68.211.160.0/19')
		self.assertEqual(ip1.lpm(cidr1), 17)
		self.assertEqual(ip1.lpm(cidr2), 0)


class TestCIDRMethods(unittest.TestCase):

	def test_isnotcidr(self):
		with self.assertRaises(TypeError):
			CIDRBlock('192.168.0.1')
			CIDRBlock('192.168.0.1/33')

	def test_tostring(self):
		cidr1 = CIDRBlock('27.190.0.0/18')
		cidr2 = CIDRBlock('66.50.240.0/20')
		self.assertNotEqual(cidr1.tostring(), cidr2.tostring())
		self.assertEqual(cidr1.tostring(), '27.190.0.0/18')
		self.assertEqual(cidr2.tostring(), '66.50.240.0/20')

	def test_getrange(self):
		cidr1 = CIDRBlock('160.4.0.0/15')
		cidr2 = CIDRBlock('56.250.123.0/24')
		self.assertEqual(cidr1.getrange(), ('160.4.0.0', '160.5.255.255'))
		self.assertEqual(cidr2.getrange(), ('56.250.123.0', '56.250.123.255'))

	def test_getmask(self):
		cidr1 = CIDRBlock('190.190.0.0/16')
		cidr2 = CIDRBlock('69.171.240.0/20')
		self.assertEqual(cidr1.getmask(), '255.255.0.0')
		self.assertEqual(cidr2.getmask(), '255.255.240.0')

	def test_matches(self):
		ip1 = IP('74.125.39.254')
		ip2 = IP('225.34.7.2')
		cidr1 = CIDRBlock('74.125.38.0/23')
		cidr2 = CIDRBlock('225.34.0.0/21')
		self.assertTrue(cidr1.matches(ip1))
		self.assertTrue(cidr2.matches(ip2))
		self.assertFalse(cidr1.matches(ip2))
		self.assertFalse(cidr2.matches(ip1))

class TestParser(unittest.TestCase):

	def test_parsesip(self):
		self.assertEqual(ip_parser('192.168.0.1'), 
			             IP('192.168.0.1'))
		self.assertIsInstance(ip_parser('192.168.0.1'), IP)
		self.assertEqual(ip_parser('192.168.0.1/24'), 
			             CIDRBlock('192.168.0.1/24'))
		self.assertIsInstance(ip_parser('192.168.0.1/24'), CIDRBlock)

if __name__ == '__main__':
	unittest.main()