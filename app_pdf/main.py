from get_api import data_dict
from render_template import save_rendered_html, generate_rendered_html, render_template
from dir_creation import create_default_readme_file, create_settings_env_file
from create_pdf import convert_to_pdf


def main():
    create_default_readme_file()
    create_settings_env_file()
    template_path = 'templates/template.html'
    rendered_html = render_template(template_path, data_dict)
    save_rendered_html(rendered_html, 'templates/rendered_template.html')
    convert_to_pdf()

if __name__ == "__main__":
    main()