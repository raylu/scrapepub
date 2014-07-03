#!/usr/bin/env python

from epub import epub
import lxml.etree
import lxml.html

import os
import shutil

def main():
	book = epub.EpubBook()
	book.setTitle('Ra')
	book.addCreator('qntm - Ed MacPherson')
	book.addTitlePage()
	book.addTocPage()

	template = '''
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">
	<head><title>%s</title></head>
	<body><p>%s</p></body>
	</html>
	'''

	files = os.listdir('raw')
	files.sort(key=int)

	for filename in files:
		print 'binding', filename
		with open('raw/' + filename, 'r') as f:
			html = f.read()
		html = html.replace('\r', '')
		dom = lxml.html.document_fromstring(html)

		h2s = list(dom.iterdescendants('h2'))
		if len(h2s) != 1:
			raise RuntimeError('expected 1 h2')
		title = h2s[0].text

		for div in dom.iterdescendants('div'):
			if div.get('id') == 'content':
				break
		else:
			raise RuntimeError('could not find id="content"')

		content = ''
		for el in div.iterchildren():
			el_str = lxml.etree.tostring(el)
			el_str = el_str.replace('<strike>', '<del>')
			el_str = el_str.replace('</strike>', '</del>')
			content += el_str

		n = book.addHtml('', '%s.html' % filename, template % (title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'ra'
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main()
