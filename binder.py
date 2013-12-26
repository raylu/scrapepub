#!/usr/bin/env python

from epub import ez_epub
import lxml.html

import os
import re

def main():
	book = ez_epub.Book()
	book.title = 'Tales of MU - Volume 1'
	book.authors = ['Alexandra Erin']

	files = []
	for filename in os.listdir('html'):
		if '.' in filename:
			files.append(float(filename))
		else:
			files.append(int(filename))
	files.sort()

	for filename in files:
		print 'binding', filename
		section = ez_epub.Section()
		section.title = filename
		section.css = '''
			.h2 { font-size: 24pt; font-weight: bold; }
			.em { font-style: italic; }
			.strong { font-weight: bold; }
			.em_strong { font-style: italic; font-weight: bold; }
		'''

		dom = lxml.html.parse('html/%s' % filename)
		for div in dom.getroot().iterdescendants('div'):
			div_class = div.get('class')
			if div_class not in ['date', 'entry']:
				continue
			last_segments = extract_text(section.text, div, [])
			if last_segments:
				section.text.append(last_segments)
		book.sections.append(section)
		break

	book.make('tomu_vol1')

def extract_text(text, el, styles):
	segments = []
	if el.text:
		segments.append((el.text, '_'.join(sorted(styles))))
	for sub_el in el:
		style = None
		if sub_el.tag == 'hr': # end of the chapter
			break
		elif sub_el.tag in ['p', 'br']:
			text.append(segments)
			segments = []
		elif sub_el.tag in ['h2', 'em', 'b', 'strong']:
			if sub_el.tag == 'b':
				sub_el.tag = 'strong'
			style = sub_el.tag
		elif sub_el.tag not in ['a', 'span', 'center']:
			print 'unhandled tag', sub_el.tag
		if style is not None:
			styles.append(style)
		segments.extend(extract_text(text, sub_el, styles))
		if style is not None:
			styles.pop()
	if el.tail:
		segments.append((el.tail, '_'.join(sorted(styles))))
	return segments

if __name__ == '__main__':
	main()
