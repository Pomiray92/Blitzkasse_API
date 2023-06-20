from get_api import data_dict
from create import save_rendered_html, generate_rendered_html, render_template
from settings import create_default_readme_file, create_settings_env_file

def main():
    create_default_readme_file()
    create_settings_env_file()
    template_path = 'templates/template.html'
    rendered_html = render_template(template_path, data_dict)
    save_rendered_html(rendered_html, 'templates/rendered_template.html')

if __name__ == "__main__":
    main()