import subprocess
from flask import Flask, render_template, jsonify, request
from wsl_operations import get_wsl_instances, delete_instance, clone_instance, get_available_distributions, install_distribution
import os

app = Flask(__name__)

@app.route('/')
def index():
    wsl_instances = get_wsl_instances()
    distributions = get_available_distributions()
    return render_template('index.html', instances=wsl_instances, distributions=distributions)

@app.route('/delete', methods=['POST'])
def delete_wsl():
    instances = request.json.get('instances', [])
    for instance in instances:
        delete_instance(instance)
    return jsonify({'status': 'success'})

@app.route('/clone', methods=['POST'])
def clone_wsl():
    original_instance = request.json.get('original_instance')
    new_instance_name = request.json.get('new_instance_name')

    if not original_instance or not new_instance_name:
        return jsonify({'status': 'error', 'message': 'Both original_instance and new_instance_name are required.'}), 400

    try:
        clone_instance(original_instance, new_instance_name)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/install', methods=['POST'])
def install_wsl():
    distribution = request.json.get('distribution')
    install_distribution(distribution)
    return jsonify({'status': 'success'})

@app.route('/fetch-wsl-instances')
def fetch_wsl_instances():
    instances = get_wsl_instances()  # This should now include the cloned instance
    return render_template('instances_list.html', instances=instances)

@app.route('/check-instance-name', methods=['GET'])
def check_instance_name():
    instance_name = request.args.get('instance_name')
    existing_instances_output = subprocess.run(['wsl', '--list'], capture_output=True, text=True).stdout.encode('utf-8').decode('utf-16').replace('\x00', '')

    # Split the output into lines and clean up each line
    existing_instances = [line.strip().split(' ')[0] for line in existing_instances_output.splitlines() if line.strip()]

    # Check if the exact instance name exists in the list
    exists = instance_name in existing_instances
    
    return jsonify({'exists': exists})

if __name__ == '__main__':
    app.run(debug=True)
