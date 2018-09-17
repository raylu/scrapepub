#!/usr/bin/env python

import os
import shutil

from bs4 import BeautifulSoup
from epub import epub

def main():
	book = epub.EpubBook()
	book.setTitle('Ward (Worm 2)')
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

	dirname = 'worm2_raw/'
	files = os.listdir(dirname)
	files.sort()

	chapter_link_text = ['Last Chapter', 'Previous Chapter', 'Next Chapter']

	for filename in files:
		print 'binding', filename
		with open(dirname + filename, 'r') as f:
			soup = BeautifulSoup(f, 'lxml')
		title = soup.find(class_='entry-title').string
		content = soup.find(class_='entry-content')

		# remove prev/next chapter links
		p_removed = 0
		for p in content.children:
			if p.name != 'p':
				continue
			for strong in p.children:
				if strong.name != 'strong':
					continue
				found_p = False
				for el in strong.children:
					if el.name == 'a' and el.string in chapter_link_text:
						p.decompose()
						p_removed += 1
						found_p = True
						break
				if found_p:
					break
		assert p_removed == 2, 'found %d chapter links' % p_removed

		# remove facebook/twitter share links
		share_divs = content.find_all("div", class_='sharedaddy')
		assert len(share_divs) == 2, 'found %d share divs' % len(share_divs)
		for div in share_divs:
			div.decompose()

		n = book.addHtml('', '%s.html' % filename, template % (title, title, content))
		book.addSpineItem(n)
		book.addTocMapNode(n.destPath, title)

	output_name = 'worm2'
	shutil.rmtree(output_name, ignore_errors=True)
	book.createBook(output_name)
	epub.EpubBook.createArchive(output_name, output_name + '.epub')

if __name__ == '__main__':
	main()
