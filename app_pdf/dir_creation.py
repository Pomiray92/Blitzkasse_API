from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


def create_settings_env_file():
    DEFAULT_SERVER_IP = "localhost"
    settings_env_file = "settings.env"

    if not os.path.isfile(settings_env_file):
        with open(settings_env_file, "w") as env_file:
            env_file.write(f"SERVER_IP={DEFAULT_SERVER_IP}\n")


def create_default_readme_file():
    readme_file = "README.txt"

    if not os.path.isfile(readme_file):
        with open(readme_file, "w") as file:
            file.write("---------------------------------------\n")
            file.write("APP for creating PDF from retrieved receipt information:\n")
            file.write("\n")
            file.write(
                "This app allows you to create a PDF from retrieved receipt data, store it, or send it via email.\n"
            )
            file.write(".\n")
            file.write("\n")