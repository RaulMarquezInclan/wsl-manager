import subprocess
import os

BACKUP_DIR = 'C:\\WSL_Instances\\Backups\\'

def get_wsl_instances():
    result = subprocess.run(['wsl', '--list', '--verbose'], capture_output=True, text=True, timeout=10)
    decoded_output = result.stdout.encode('utf-8').decode('utf-16').replace('\x00', '')
    
    instances = []

    for line in decoded_output.splitlines()[1:]:  # Skip the header line
        line = line.lstrip('*').strip()  # Remove the leading '*' if present and strip whitespace
        
        # Split the line into name, state, and version
        parts = line.split(maxsplit=2)
        
        if len(parts) == 3:  # Ensure that the line contains all three parts
            name = parts[0].strip()
            state = parts[1].strip()
            instances.append({'name': name, 'state': state})

    return instances

def delete_instance(instance_name):
    subprocess.run(['wsl', '--unregister', instance_name])

def clone_instance(original_instance, new_instance_name):
    # Ensure the backup directory exists
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Export the original WSL instance to a tar file
    export_path = os.path.join(BACKUP_DIR, f'{original_instance}.tar')

    # Check if the new instance name already exists
    existing_instances_output = subprocess.run(['wsl', '--list'], capture_output=True, text=True).stdout.encode('utf-8').decode('utf-16').replace('\x00', '')
    existing_instances = [line.strip().split(' ')[0] for line in existing_instances_output.splitlines() if line.strip()]

    if new_instance_name in existing_instances:
        raise Exception(f"An instance with the name '{new_instance_name}' already exists.")

    # Specify a unique installation directory to avoid conflicts
    install_dir = os.path.join(BACKUP_DIR, new_instance_name)

    # Command to export and import in the same cmd window
    combined_cmd = (
        f'wsl --export {original_instance} {export_path} && '
        f'wsl --import {new_instance_name} {install_dir} {export_path} --version 2'
    )
    
    try:
        # Run the command in a new command prompt window
        subprocess.run(['cmd', '/c', 'start', 'cmd', '/k', combined_cmd], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to clone the WSL instance: {e.stderr}")
    
    print(f"Cloned {original_instance} to {new_instance_name} and installed it without running.")

def get_available_distributions():
    print("Starting get_available_distributions()")
    try:
        result = subprocess.run(['wsl', '--list', '--online'], capture_output=True, text=True, timeout=10)
        print("Subprocess completed successfully")
    except subprocess.TimeoutExpired:
        print("Subprocess timed out.")
        return []
    except Exception as e:
        print(f"Subprocess failed with an error: {e}")
        return []

    # Decoding the output to remove null bytes
    decoded_output = result.stdout.encode('utf-8').decode('utf-16').replace('\x00', '')

    distributions = []
    parsing_started = False

    for line in decoded_output.splitlines():
        line = line.strip()

        if not line:
            continue  # Skip empty lines

        if 'FRIENDLY NAME' in line:
            parsing_started = True
            continue

        if parsing_started and len(line) > 0:
            # Extract everything before the first space (the NAME column)
            distro_name = line.split(maxsplit=1)[0].strip()
            distributions.append({'id': distro_name, 'name': distro_name})

    return distributions

def install_distribution(distribution_id):
    print(f"Starting installation for distribution: {distribution_id}")
    os.system(f'start cmd /k "wsl --install -d {distribution_id}"')
