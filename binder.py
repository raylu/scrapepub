#!/usr/bin/env python

from epub import epub
import lxml.etree
import lxml.html

import os
import shutil

def main():
	book = epub.EpubBook()
	book.setTitle('Tales of MU - Volume 1')
	book.addCreator('Alexandra Erin')
	book.addTitlePage()
	book.addTocPage()

	template = '''
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">
	<head><title>%s</title></head>
	<body><p>%s</p></body>
	</html>
	'''

	files = []
	for filename in os.listdir('html'):
		if '.' in filename:
			files.append(float(filename))
		else:
			files.append(int(filename))
	files.sort()

	for filename in files:
		print 'binding', filename
		with open('html/%s' % filename, 'r') as f:
			html = f.read()
		html = html.replace('\r', '')
		dom = lxml.html.document_fromstring(html)
		for div in dom.iterdescendants('div'):
			if div.get('class') == 'post':
				break
		else:
			raise RuntimeError('could not find div with class="post"')

		content = ''
		for el in div.iterchildren():
			el_str = lxml.etree.tostring(el)
			el_str = el_str.replace('<strike>', '<del>')
			el_str = el_str.replace('</strike>', '</del>')
			content += el_str
		h2s = list(div.itertext('h2'))
		if len(h2s) != 2:
			raise RuntimeError("expected 2 h2's got %d" % len(h2s))
		title = h2s[0]

		n = book.addHtml('', '%s.html' % filename, template % (filename, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'tomu_vol1'
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main()
