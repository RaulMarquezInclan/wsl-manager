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
    instances = request.json.get('instances', [])
    for instance in instances:
        clone_instance(instance)
    return jsonify({'status': 'success'})

@app.route('/install', methods=['POST'])
def install_wsl():
    distribution = request.json.get('distribution')
    install_distribution(distribution)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
