#!/usr/bin/env python

import os
import shutil

from bs4 import BeautifulSoup
from epub import epub

def main():
	book = epub.EpubBook()
	book.setTitle('Worm')
	book.addCreator('Wildbow - John C. McCrae')
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

	dirname = 'worm_raw/'
	files = os.listdir(dirname)
	files.sort()

	chapter_link_text = ['Last Chapter', 'Next Chapter', ' Next Chapter']

	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		content = soup.find(class_='entry-content')

		# remove prev/next chapter links
		p_removed = 0
		for el in content.children:
			if el.name == 'p':
				has_chapter_links = has_nontext = False
				for c in el.children:
					if c.name == 'a' and c.string in chapter_link_text:
						el.decompose()
						p_removed += 1
						break
		if p_removed != 2 and filename != '304-moving-on':
			raise Exception('removed %d' % p_removed)

		# remove facebook/twitter share links
		if filename != '000-1-01':
			content.find('div', id='jp-post-flair').decompose()

		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'worm'
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main()
