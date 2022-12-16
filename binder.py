#!/usr/bin/env python2

import os
import shutil
import sys

from bs4 import BeautifulSoup
from epub import epub

def main(vol):
	titles = {
		'book1': 'Book I: Lost Things',
	}
	book = epub.EpubBook()
	book.setTitle('Pale Lights - ' + titles[vol])
	book.addCreator('ErraticErrata')
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

	dirname = 'palelights_%s_raw/' % vol
	files = os.listdir(dirname)
	files.sort()

	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		content = soup.find(class_='entry-content')

		process_chapter(vol, filename, content)
		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'palelights_' + vol
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

chapter_link_text = ['Previous Chapter', 'Next Chapter']

def process_chapter(vol, filename, content):
	content.find(id='jp-post-flair').decompose()

if __name__ == '__main__':
	main(*sys.argv[1:])
