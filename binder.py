#!/usr/bin/env python

from bs4 import BeautifulSoup
from epub import epub

import os
import shutil

def main():
	book = epub.EpubBook()
	book.setTitle('A Practical Guide to Evil')
	book.addCreator('erraticerrata')
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
	files.sort()

	for filename in files:
		print 'binding', filename
		with open('raw/' + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		content = soup.find(class_='entry-content')
		content.find(class_='wpcnt').decompose()
		content.find(id='jp-post-flair').decompose()

		n = book.addHtml('', '%s.html' % filename, template % (title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'pgte'
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main()
