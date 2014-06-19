import xml.etree.ElementTree as ET
a=ET.parse("F.svg")
root=a.getroot()
ns={'ns': 'http://www.w3.org/2000/svg'}
#root.find('ns:g',namespaces=ns)
for i,x in enumerate(root):
	if root[i].find('ns:g',namespaces=ns) is not None:
		print i,"hit"
		for j,y in enumerate(root[i]):
			print j,"hit"
	else:
		print i,"xx"

for x in root.iter('{http://www.w3.org/2000/svg}path'):
	print x.get('d')

for x in root.iter('{http://www.w3.org/2000/svg}path'):
	print "path-transform=", x.get('transform')

for x in root.iter('{http://www.w3.org/2000/svg}g'):
	print "g-transform=", x.get('transform')

