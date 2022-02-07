#!/usr/bin/env python2

import os
import shutil
import sys
import xml.sax.saxutils

from bs4 import BeautifulSoup
from epub import epub

def main(bookname):
	titles = {
		'book1': 'Book I',
		'book2': 'Book 2',
		'book3': 'Book 3',
		'book4': 'Book 4',
		'book5': 'Book 5',
		'book6': 'Book 6',
		'book7': 'Book 7',
	}
	book = epub.EpubBook()
	book.setTitle('A Practical Guide to Evil - ' + titles[bookname])
	book.addCreator('erraticerrata')
	book.addTitlePage()
	book.addTocPage()

	template = '''
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">
	<head><title>%s</title></head>
	<body>
		<h2>%s</h2>
		<p>%s</p>
	</body>
	</html>
	'''

	dirname = 'pgte_%s_raw/' % bookname
	files = os.listdir(dirname)
	files.sort()

	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		title_escaped = xml.sax.saxutils.escape(title)
		content = soup.find(class_='entry-content')
		content.find(id='jp-post-flair').decompose()

		n = book.addHtml('', '%s.html' % filename, template % (title_escaped, title_escaped, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'pgte_' + bookname
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main(*sys.argv[1:])
