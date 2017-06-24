#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^

import markdown
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def generate(src_content):
    html = markdown.markdown(src_content)
#     html = '''<link rel="stylesheet" href="/static/css/monokai-sublime.css">
# <script src="/static/js/highlight.pack.js"></script>
# <script>hljs.initHighlightingOnLoad();</script>
# %s
# ''' % html
    return html


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    generate(input_file, output_file)