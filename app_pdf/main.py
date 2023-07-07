from get_api import data_dict
from render_template import save_rendered_html, render_template
from dir_creation import create_default_readme_file, create_settings_env_file
from create_pdf import convert_to_pdf
from upload_to_ftp_ import read_from_json_and_upload
from qr_generator import qr_generator

def main(template_path, rendered_html):
    create_default_readme_file()
    create_settings_env_file()
    save_rendered_html(rendered_html, "templates/rendered_template.html")
    convert_to_pdf()
    read_from_json_and_upload()
    qr_generator()

if __name__ == "__main__":
    template_path = "templates/template.html"
    rendered_html = render_template(template_path, data_dict)
    main(template_path, rendered_html)