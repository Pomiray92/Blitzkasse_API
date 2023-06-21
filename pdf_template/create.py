from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
from get_api import taxProducts

def generate_rendered_html(template_path, data_dict):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    rendered_html = template.render(data_dict)
    return rendered_html


def save_rendered_html(rendered_html, output_file):
    with open(output_file, 'w') as file:
        file.write(rendered_html)


def render_template(template_path, data_dict):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    
    # Create a dictionary to store the consolidated items and their quantities
    rendered_html = template.render(data_dict)
    return rendered_html

