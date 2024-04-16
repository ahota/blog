#!/usr/local/bin/python3

import bs4
import markdown
import os

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from bs4.builder import HTMLTreeBuilder
from bs4.builder._htmlparser import HTMLParserTreeBuilder

# prevent prettify() from adding newlines to <code> tags
class CodeAwareTreeBuilder(HTMLParserTreeBuilder):
    DEFAULT_PRESERVE_WHITESPACE_TAGS = set(['pre', 'textarea', 'code'])

def make_post(filename):
    with open(filename, 'r') as f:
        md = f.read()

    html = markdown.markdown(md, extensions=['fenced_code', 'codehilite', 'footnotes'])

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('post.html')
    rendered = template.render(post=html)

    soup = BeautifulSoup(rendered, features='html.parser', builder=CodeAwareTreeBuilder())
    try:
        soup.main.h2.string.wrap(soup.new_tag('code'))
    except:
        print('Could not find h2? Dumping the file')
        with open('make_post_error.html', 'w') as f:
            f.write(soup.prettify(formatter='html5'))
        return
    soup.main.h2.code.string.insert_before('~$ ')

    formatter = bs4.formatter.HTMLFormatter(indent=2)
    post = soup.prettify(formatter=formatter)

    dirname, ext = os.path.splitext(os.path.basename(filename))
    dirpath = os.path.join('blog', dirname)
    try:
        os.mkdir(dirpath)
    except FileExistsError as e:
        print('overwriting existing post!')
    outname = os.path.join(dirpath, 'index.html')

    with open(outname, 'w') as f:
        f.write(post)

    print('created', outname)

'''
def add_post(dirpath):
    with open('blog/index.html', 'rw') as bp:
'''

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()

    make_post(args.input)
