#!/usr/bin/env python

from epub import ez_epub
import lxml.html

import os
import re

css = {
	'h2': 'font-weight: bold;',
	'em': 'font-style: italic;',
	'strong': 'font-weight: bold;',
	'center': '{text-align: center;',
	'em_strong': 'font-style: italic; font-weight: bold;',
	'center_strong': 'text-align: center; font-weight: bold;',
	'center_em_strong': 'text-align: center; font-style: italic; font-weight: bold;',
}

def main():
	book = ez_epub.Book()
	book.title = 'Tales of MU - Volume 1'
	book.authors = ['Alexandra Erin']

	stylesheet = ''
	for class_name, styles in css.items():
		stylesheet += '.%s {%s}' % (class_name, styles)

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
		section.css = stylesheet

		dom = lxml.html.parse('html/%s' % filename)
		for div in dom.getroot().iterdescendants('div'):
			div_class = div.get('class')
			if div_class not in ['date', 'entry']:
				continue
			last_segments = extract_text(section.text, div, [])
			if last_segments:
				section.text.append(last_segments)
		book.sections.append(section)

	book.make('tomu_vol1')

def extract_text(text, el, styles):
	segments = []
	if el.text:
		segments.append(format_tuple(el.text, styles))
	for sub_el in el:
		style = None
		if sub_el.tag == 'hr': # end of the chapter
			break
		elif sub_el.tag in ['p', 'br']:
			text.append(segments)
			segments = []
		elif sub_el.tag in ['h2', 'em', 'b', 'strong', 'center', 'strike']:
			if sub_el.tag == 'b':
				sub_el.tag = 'strong'
			style = sub_el.tag
		elif sub_el.tag not in ['a', 'span', 'wbr']:
			raise RuntimeError('unhandled tag ' + sub_el.tag)
		if style is not None:
			styles.append(style)
		segments.extend(extract_text(text, sub_el, styles))
		if style is not None:
			styles.pop()
		if sub_el.tag == 'h2':
			text.append(segments)
			segments = []
	if el.tail:
		segments.append(format_tuple(el.tail, styles))
	return segments

def format_tuple(text, styles):
	style = '_'.join(sorted(styles))
	if style and style not in css.iterkeys():
		raise RuntimeError('unhandled style: ' + style)
	return (text, style)

if __name__ == '__main__':
	main()
