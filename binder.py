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
		'vol4': 'Volume 4',
		'vol5': 'Volume 5',
		'bonus': 'Bonus Chapters',
	}
	book = epub.EpubBook()
	book.setTitle('The Gods are Bastards - ' + titles[vol])
	book.addCreator('D. D. Webb')
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

	dirname = 'gab_%s_raw/' % vol
	files = os.listdir(dirname)
	if vol == 'vol2':
		files.remove('16-interruption')
	elif vol == 'vol5':
		files.remove('025-pausing-to-move')
		files.remove('057-bonus-49-continued')
	files.sort()


	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		content = soup.find(class_='entry-content')
		content.find(id='jp-post-flair').decompose()
		wpcnt = content.find(class_='wpcnt')
		if wpcnt is not None:
			wpcnt.decompose()

		# remove prev/next chapter links and random ad stylesheet
		p_removed = 0
		for el in content.children:
			if el.name == 'style':
				el.decompose()
			elif is_ch_nav(el):
				el.decompose()
				p_removed += 1
		if p_removed not in (1, 2) and filename != '165-site-announcement':
			raise Exception('removed %d' % p_removed)

		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'gab_' + vol
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

chapter_link_text = ['< Previous Chapter', 'Next Chapter >']

def is_ch_nav(el):
	if el.name != 'p':
		return False

	for c in el.children:
		if c.name == 'a':
			if c.string in chapter_link_text:
				return True
			for cc in c.children:
				if cc.name == 'strong' and cc.string in chapter_link_text:
					return True
		if c.name == 'strong':
			for cc in c.children:
				if cc.name == 'a' and cc.string in chapter_link_text:
					return True
	return False

if __name__ == '__main__':
	main(*sys.argv[1:])
