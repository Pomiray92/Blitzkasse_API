# ReprintReceiptApp

## Overview
This app allows you to trigger the printing process by reprinting the last receipt. It provides flexibility to specify the number of times to reprint the receipt using command-line arguments or the .env file.

## Prerequisites
Before using the app, make sure you have the following prerequisites:
- Python installed on your system.
- The required packages are installed. You can install the required packages using the following command:

pip install -r requrements.txt 
    

## Getting Started
To use the app, follow these steps:
1. Download or copy the code into a Python file (e.g., `print_app.py`).
2. Open a terminal or command prompt and navigate to the directory containing the Python file.
3. Run the Python file using the following command:

python print_app.py [num_prints]

- Replace `[num_prints]` with the desired number of times to reprint the last receipt. This argument is optional. If not provided, the app will use the value from the .env file or the default value.
4. The app will trigger the printing process and provide information about the success or failure of each print operation.

## Configuration
The app supports configuration through the following methods:

### Environment Variables
The app uses environment variables for configuration. You can set the following environment variables:
- `SERVER_IP`: Specifies the IP address of the server. If not set, the app will use the default value of "localhost".
- `NUM_PRINTS`: Specifies the default number of times to reprint the last receipt. If not set, the app will use the default value.

### .env File
If the `.env` file is present in the same directory as the Python file, the app will load the environment variables from it. If the file does not exist, a default `.env` file will be created with the default configuration.

To customize the configuration, create or modify the `.env` file using a text editor. Set the environment variables in the format `KEY=VALUE`, with each variable on a separate line. For example:

1. SERVER_IP=192.168.0.1
2. NUM_PRINTS=3


## Output
The app generates the following output files:
- `README.md`: Contains information about the app and its functionality.
- `printing_reports.txt`: Stores a log of the printing process, including success and failure messages for each print operation.

## Error Handling
If an error occurs during the execution of the app, error messages will be displayed in the terminal or command prompt. Additionally, detailed error information will be appended to the `printing_reports.txt` file.

## Example Usage
Here are some examples of how to use the app:
- Trigger the printing process and reprint the last receipt once:

python print_app.py

- Trigger the printing process and reprint the last receipt three times:

Customize the default number of prints using the `.env` file:
1. Create a file named `.env` in the same directory as the Python file.
2. Open the `.env` file with a text editor.
3. Set the `NUM_PRINTS` variable to the desired default value. For example:

NUM_PRINTS=5

4. Save the file.
5. Run the Python file without providing the number of prints as a command-line argument:

python print_app.py

The app will use the default value specified in the `.env` file.

## Conclusion
With this app, you can easily trigger the printing process by reprinting the last receipt. It provides flexibility in specifying the number of times to reprint and supports customization through environment variables and the `.env` file.

## License
This app is distributed under the terms of the MIT License. The MIT License is a permissive open-source license that allows you to use, modify, and distribute the app, both for commercial and non-commercial purposes. It provides flexibility and freedom while ensuring that you include the original license notice in any copies or derivatives of the software.

By using this app, you agree to the terms and conditions of the MIT License. Please see the [LICENSE](LICENSE) file for more information.

## Third-Party Libraries
The app may utilize third-party libraries or dependencies, which may have their own licenses. The licenses for these libraries can be found in the respective `LICENSE` or `README` files within the library's source code or documentation. It's important to review and comply with the licenses of any third-party libraries used in conjunction with this app.
