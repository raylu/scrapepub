#!/usr/bin/env python

from epub import ez_epub

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
		with open('html/%s' % filename) as f:
			html = f.readlines()
		section = ez_epub.Section()
		section.title = filename
		state = None
		for line in html:
			line = line.strip().decode('utf-8')
			if '<div class="date">' in line:
				state = 'date'
			elif '<div class="entry">' in line:
				state = 'entry'
			elif '<hr>' in line:
				state = None
			line = re.sub('&#\d{4};', repl_entity, line)
			if state is not None:
				while True:
					line, subs = re.subn('<.*?>', '', line)
					if subs == 0:
						break
				section.text.append(line)
		book.sections.append(section)

	book.make('tomu_vol1')

def repl_entity(match):
	entity = match.group(0)
	return unichr(int(entity[2:6]))

if __name__ == '__main__':
	main()
