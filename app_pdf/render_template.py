from jinja2 import Environment, FileSystemLoader
from get_api import taxProducts
from get_api import data_dict

template_path = "templates/template.html"

def render_template(template_path, data_dict, output_file=None):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_path)
    rendered_html = template.render(data_dict)

    if output_file:
        save_rendered_html(rendered_html, output_file)

    return rendered_html

rendered_html = render_template(template_path, data_dict)

def save_rendered_html(rendered_html, output_file):
    with open(output_file, "w") as file:
        file.write(rendered_html)