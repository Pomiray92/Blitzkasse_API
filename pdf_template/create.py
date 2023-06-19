from jinja2 import Environment, FileSystemLoader, Template
from get_api import data_dict



def render_template(template_path, data_dict):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    rendered_html = template.render(data_dict)
    return rendered_html

template_path = 'template.html'    
rendered_html = render_template(template_path, data_dict)
print(rendered_html)