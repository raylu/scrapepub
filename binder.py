#!/usr/bin/env python

import os
import shutil
import sys

from bs4 import BeautifulSoup
from epub import epub

def main(vol):
	titles = {
		'vol1': 'Volume 1',
		'vol2': 'Volume 2',
		'vol3': 'Volume 3',
	}
	book = epub.EpubBook()
	book.setTitle('The Wandering Inn - ' + titles[vol])
	book.addCreator('pirateaba')
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

	dirname = 'inn_%s_raw/' % vol
	files = os.listdir(dirname)
	files.sort()

	chapter_link_text = ['Previous Chapter', 'Next Chapter']

	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		content = soup.find(class_='entry-content')
		content.find(class_='wpcnt').decompose()

		# remove prev/next chapter links and random ad stylesheet
		p_removed = 0
		for el in content.children:
			if el.name == 'style':
				el.decompose()
			elif el.name == 'p':
				has_chapter_links = has_nontext = False
				for c in el.children:
					if (c.name == 'a' and c.string in chapter_link_text) or (c.name == 'span' and \
							any(cc.name == 'a' and cc.string in chapter_link_text for cc in c.children)):
						el.decompose()
						p_removed += 1
						break
					elif c.name == 'span' and c.attrs['style'] == 'color:#8ae8ff;':
						c.attrs['style'] = 'color:#444477;'
		if p_removed not in (1, 2):
			raise Exception('removed %d' % p_removed)

		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'inn_' + vol
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main(*sys.argv[1:])
