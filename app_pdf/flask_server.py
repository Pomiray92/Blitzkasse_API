import os
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__)

UPLOADS_DIR = 'uploads'

@app.route('/postPDF', methods=['PUT'])
def post_pdf():
    file = request.files['file']
    
    # Create the uploads directory if it doesn't exist
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    
    # Process the uploaded file and save it to the uploads directory
    file.save(os.path.join(UPLOADS_DIR, 'receipt.pdf'))
    
    # Perform additional operations on the file
    # ...
    
    # Return a response to indicate success
    return 'PDF file received and processed successfully'

@app.route('/qr_code.png')
def get_qr_code():
    return send_from_directory('', 'qr_code.png')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getPDF')
def get_pdf():
    filename = 'receipt.pdf'
    return send_from_directory(UPLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='localhost', port=8080)