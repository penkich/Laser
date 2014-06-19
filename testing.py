import xml.etree.ElementTree as ET
a=ET.parse("F.svg")
root=a.getroot()
ns={'ns': 'http://www.w3.org/2000/svg'}
#root.find('ns:g',namespaces=ns)
for i,x in enumerate(root):
	if x.find('ns:g',namespaces=ns) is not None:
		print i,"hit"
	else:
		print i,"xx"
