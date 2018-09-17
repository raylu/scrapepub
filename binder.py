#!/usr/bin/env python

from epub import epub
import lxml.etree
import lxml.html

import os
import shutil

def main():
	book = epub.EpubBook()
	book.setTitle('Pact')
	book.addCreator('Wildbow - J.McCrae')
	book.addTitlePage()
	book.addTocPage()

	template = '''
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">
	<head><title>%s</title></head>
	<body><p>%s</p></body>
	</html>
	'''

	files = os.listdir('pact_raw')
	files.sort(key=lambda n: int(n[:3]))

	for filename in files:
		print 'binding', filename
		with open('pact_raw/' + filename, 'r') as f:
			html = f.read()
		html = html.replace('\r', '')
		dom = lxml.html.document_fromstring(html)

		h1s = list(dom.iterdescendants('h1'))
		if filename == '150-pact-sealed':
			title = h1s[0].text
		else:
			if len(h1s) < 2:
				raise RuntimeError('expected at least 2 h1')
			title = h1s[1].text

		for div in dom.iterdescendants('div'):
			if div.get('class') == 'entry-content':
				break
			if filename == '150-pact-sealed' and div.get('class') == 'entry clear':
				break
		else:
			raise RuntimeError('could not find class="entry-content"')

		content = ''
		for el in div.iterchildren():
			el_str = lxml.etree.tostring(el)
			el_str = el_str.replace('<strike>', '<del>')
			el_str = el_str.replace('</strike>', '</del>')
			content += el_str

		n = book.addHtml('', '%s.html' % filename, template % (title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'pact'
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main()
