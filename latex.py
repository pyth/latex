#!/usr/bin/env python

import os
import re
import json
import jinja2
import argparse

class Model:
    latex_env = jinja2.Environment(
        variable_start_string = '{{',
        variable_end_string = '}}',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )

    conv = {
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

    def tex_escape(self, text):
        regex = re.compile('|'.join(re.escape(str(key))
        for key in sorted(self.conv.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: self.conv[match.group()], text)

    def load_data(self, path):
        with open(path, "r") as js:
            data = json.load(js)
        for d in data:
            data[d] = self.tex_escape(data[d])
        return data

    def load_template(self, path):
        return self.latex_env.get_template(args.template)
    
    def render(self, out = None):
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
