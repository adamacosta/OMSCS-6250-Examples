from iputils import ip_parser

def main():
	ips = list(map(ip_parser, ['68.211.6.120', '68.208.0.0/12',
		                       '68.211.0.0/17', '68.211.128.0/19', 
		                       '68.211.160.0/19', '68.211.192.0/18']))
	
	print 'address to match:'
	print ips[0].tostring() + ': ' + ips[0].tobits() + '\n'
	print 'possible matches:'
	for i in range(1, len(ips)):
		print ips[i].tostring() + ': ' + ips[i].tobits()
		print 'matches ... ', ips[i].matches(ips[0]) 

	print '\n' + 'longest match: ' + \
	      str(max([ips[0].lpm(ips[i]) for i in range(1, len(ips))]))

if __name__ == '__main__':
	main()