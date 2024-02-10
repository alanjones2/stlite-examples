import markdown

name = "text"
with open(f'./{name}.md', 'r') as reader:
    md = reader.read()
html = markdown.markdown(md, extensions=['fenced_code'])
o = open(f'./{name}.html','w')
o.write(html)
o.close()