#!/usr/bin/env python

import os
import shutil
import sys

from bs4 import BeautifulSoup
from epub import epub

def main(vol):
	titles = {
		'book1': 'Book 1',
	}
	book = epub.EpubBook()
	book.setTitle('Unsong - ' + titles[vol])
	book.addCreator('Scott Alexander')
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

	dirname = 'unsong_%s_raw/' % vol
	files = os.listdir(dirname)
	files.sort()

	chapter_link_text = ['Previous Chapter', 'Next Chapter']

	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='pjgm-posttitle').string
		content = soup.find(class_='pjgm-postcontent')
		content.find(class_='sharedaddy').decompose()

		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'unsong_' + vol
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main(*sys.argv[1:])
