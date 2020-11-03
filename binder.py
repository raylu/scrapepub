#!/usr/bin/env python2

import os
import shutil
import sys

from bs4 import BeautifulSoup
from epub import epub

def main(year):
	titles = {
		'year1': 'Year 1',
		'year2': 'Year 2',
	}
	book = epub.EpubBook()
	book.setTitle('Heretical Edge - ' + titles[year])
	book.addCreator('Cerulean')
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

	dirname = 'hedge_%s_raw/' % year
	files = os.listdir(dirname)
	if year == 'year1':
		files.remove('024-christmas')
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

		# remove prev/next chapter links
		p_removed = 0
		for el in content.children:
			if is_ch_nav(el):
				el.decompose()
				p_removed += 1
		if p_removed != 2 and filename not in ['040-a-few-quick-notes',
				'177-quick-clarificationexplanation', '306-mini-interlude-51-pace',
				'000-fusion-1-01-heretical-edge-2']:
			raise Exception('removed %d' % p_removed)

		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'hedge_' + year
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
