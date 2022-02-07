#!/usr/bin/env python

import os
import re
import json
import jinja2
import argparse

class Model:
	latex_env = jinja2.Environment(
#	block_start_string = '\BLOCK{',
#	block_end_string = '}',
#	variable_start_string = '\VAR{',
#	variable_end_string = '}',
		trim_blocks = True,
		autoescape = False,
		loader = jinja2.FileSystemLoader(os.path.abspath('.'))
	)

	conv = {
		'\n': r'\\ ',
		'&': r'\&',
		'%': r'\%',
		'$': r'\$',
		'#': r'\#',
		'_': r'\_',
		'{': r'\{',
		'}': r'\}',
		'~': r'\textasciitilde{}',
		'^': r'\^{}',
		'\\': r'\textbackslash{}',
		'<': r'\textless{}',
		'>': r'\textgreater{}',
	}

	def __init__(self, template, data):
		self.template = self.load_template(template)
		self.data = self.load_data(data)

	def tex_escape(self, data):
		regex = re.compile('|'.join(re.escape(str(key))
		for key in sorted(self.conv.keys(), key=lambda item: - len(item))))
		
		if isinstance(data, list):
			for i,d in enumerate(data):
				if isinstance(d, str):
					data[i] = regex.sub(lambda match: self.conv[match.group()], d)
				elif isinstance(d, dict):
					data[i] = self.tex_escape(d)
				elif isinstance(d, list):
					data[i] = self.tex_escape(d)
		else:
			for d in data:
				if isinstance(data[d], str):
					data[d] = regex.sub(lambda match: self.conv[match.group()], data[d])
				elif isinstance(data[d], dict):
					data[d] = self.tex_escape(data[d])
				elif isinstance(data[d], list):
					data[d] = self.tex_escape(data[d])
		return data

	def load_data(self, path):
		with open(path, "r") as js:
			data = json.load(js)
		data = self.tex_escape(data)
		return data

	def load_template(self, path):
		return self.latex_env.get_template(path)
    
	def render(self, out = None):
		# print(self.data)
		document = self.template.render(self.data)
		if out:
			with open(args.output, 'w') as out:
				out.write(document)
		else:
			return document




if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(description = "Generates a pdf from a .tex template and a json data source")
	arg_parser.add_argument("-o", "--output")
	arg_parser.add_argument("-t", "--template", required = True)
	arg_parser.add_argument("-j", "--json", required = True)
	args = arg_parser.parse_args()

	model = Model(args.template, args.json)
	doc = model.render(args.output)
	if not args.output:
		print(doc)
