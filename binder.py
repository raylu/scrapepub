#!/usr/bin/env python2

import os
import shutil
import sys

from bs4 import BeautifulSoup
from epub import epub

def main(act):
	titles = {
		'act1': 'Act 1',
	}
	book = epub.EpubBook()
	book.setTitle('Katalepsis - ' + titles[act])
	book.addCreator('HY')
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

	dirname = 'katalepsis_%s_raw/' % act
	files = os.listdir(dirname)
	files.sort()

	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		content = soup.find(class_='entry-content')

		# remove prev/next chapter links
		p_removed = 0
		for el in content.children:
			if is_ch_nav(el):
				el.decompose()
				p_removed += 1
		if p_removed != 2 and filename < '188-':
			raise Exception('removed %d' % p_removed)

		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'katalepsis_' + act
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

chapter_link_text = ['Previous Chapter', 'Next Chapter']

def is_ch_nav(el):
	if el.name != 'p':
		return False

	for c in el.children:
		if c.name == 'a' and c.string in chapter_link_text:
			return True
		if c.name == 'strong':
			for cc in c.children:
				if cc.name == 'a' and cc.string in chapter_link_text:
					return True
	return False

if __name__ == '__main__':
	main(*sys.argv[1:])
