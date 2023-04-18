from jinja2 import Template


def make_template(filename):
    with open(filename, 'r') as f:
        template_text = f.read()
    template = Template(template_text)
    return template
