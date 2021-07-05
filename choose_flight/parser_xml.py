from lxml import etree


xml = '<a xmlns="test"><b xmlns="test"/></a>'

root = etree.fromstring(xml)
etree.tostring(root)
print(root)

# b'<a xmlns="test"><b xmlns="test"/></a>'



