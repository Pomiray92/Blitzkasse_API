from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


def create_settings_env_file():
    DEFAULT_SERVER_IP = "localhost"

    if not os.path.isfile("settings.env"):
        with open("settings.env", "w") as env_file:
            env_file.write(f"SERVER_IP={DEFAULT_SERVER_IP}\n")


def create_default_readme_file():
    if not os.path.isfile("README.txt"):
        with open("README.txt", "w") as file:
            file.write("---------------------------------------\n")
            file.write("APP for creating pdf from retrieve receipt Information:\n")
            file.write("\n")
            file.write(
                "This app allows you to create a PDF from retrieve receipt data, store it or send via email.\n"
            )
            file.write(".\n")
            file.write("\n")
