from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import traceback
from werkzeug.utils import secure_filename
from combine import combine_images

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
PORT = 5001  # Changed port to 5001

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/combine', methods=['POST'])
def combine():
    try:
        print("Received combine request")
        
        if 'image1' not in request.files or 'image2' not in request.files:
            print("Missing image files in request")
            return jsonify({'error': 'Both images are required'}), 400
        
        image1 = request.files['image1']
        image2 = request.files['image2']
        
        print(f"Received files: {image1.filename}, {image2.filename}")
        
        # Save files
        image1_path = os.path.join(UPLOAD_FOLDER, secure_filename(image1.filename))
        image2_path = os.path.join(UPLOAD_FOLDER, secure_filename(image2.filename))
        
        print(f"Saving files to: {image1_path}, {image2_path}")
        
        image1.save(image1_path)
        image2.save(image2_path)
        
        print("Files saved successfully")
        
        # Process images
        print("Starting image combination...")
        combine_images(image1_path, image2_path, OUTPUT_FOLDER)
        print("Image combination completed")
        
        # Return paths with the correct URL format
        base_url = f'http://localhost:{PORT}'
        results = {
            'xor_result': f'{base_url}/output/xor_result.png',
            'add_result': f'{base_url}/output/add_result.png',
            'sub_result': f'{base_url}/output/sub_result.png',
            'avg_result': f'{base_url}/output/avg_result.png',
            'max_result': f'{base_url}/output/max_result.png',
            'min_result': f'{base_url}/output/min_result.png',
            'and_result': f'{base_url}/output/and_result.png',
            'or_result': f'{base_url}/output/or_result.png'
        }
        
        print("Returning results:", results)
        return jsonify(results)
        
    except Exception as e:
        print("Error occurred:")
        print(traceback.format_exc())  # This will print the full error traceback
        return jsonify({'error': str(e)}), 500

@app.route('/output/<filename>')
def serve_output(filename):
    try:
        print(f"Attempting to serve file: {filename}")
        file_path = os.path.join(os.path.abspath(OUTPUT_FOLDER), filename)
        print(f"Full file path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        return send_from_directory(os.path.abspath(OUTPUT_FOLDER), filename)
    except Exception as e:
        print(f"Error serving file {filename}:")
        print(traceback.format_exc())
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("\nServer starting...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Output folder: {os.path.abspath(OUTPUT_FOLDER)}")
    print(f"Server will be available at http://localhost:{PORT}")
    app.run(debug=True, port=PORT) 