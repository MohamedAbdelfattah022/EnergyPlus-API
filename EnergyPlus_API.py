from flask import Flask, request, jsonify, send_from_directory
import os
from eppy import modeleditor
from eppy.modeleditor import IDF
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

iddfile = "/usr/local/EnergyPlus/Energy+.idd"
IDF.setiddname(iddfile)

OUTPUT_DIR = "/content/simulation_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route('/')
def index():
    return "Welcome to the EnergyPlus API! Use /api/run-simulation to run a simulation."

@app.route('/api/run-simulation', methods=['POST'])
def run_simulation():
    try:
        if 'idf_file' not in request.files or 'epw_file' not in request.files:
            return jsonify({'error': 'Both IDF and EPW files are required'}), 400

        idf_file = request.files['idf_file']
        epw_file = request.files['epw_file']

        if idf_file.filename == '' or epw_file.filename == '':
            return jsonify({'error': 'Empty file upload detected'}), 400

        with tempfile.TemporaryDirectory() as temp_dir:
            idf_path = os.path.join(temp_dir, idf_file.filename)
            epw_path = os.path.join(temp_dir, epw_file.filename)

            idf_file.save(idf_path)
            epw_file.save(epw_path)

            if not idf_path.endswith('.idf') or not epw_path.endswith('.epw'):
                return jsonify({'error': 'Invalid file format. Please upload .idf and .epw files'}), 400

            idf = IDF(idf_path, epw_path)
            idf.run(
                expandobjects=True,
                readvars=True,
                output_directory=OUTPUT_DIR
            )

            eplus_table_path = os.path.join(OUTPUT_DIR, 'eplustbl.htm')
            if not os.path.exists(eplus_table_path):
                return jsonify({
                    'status': 'error',
                    'message': 'Simulation completed but eplustbl.htm was not generated'
                }), 500

            return send_from_directory(
                OUTPUT_DIR,
                'eplustbl.htm',
                as_attachment=True,
                mimetype='text/html'
            )

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/output-files', methods=['GET'])
def list_output_files():
    try:
        files = os.listdir(OUTPUT_DIR)
        return jsonify({
            'status': 'success',
            'files': files
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def start_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    start_server()