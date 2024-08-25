import subprocess
import os
import re

BACKUP_DIR = 'C:\\WSL_Instances\\Backups\\'

def get_wsl_instances():
    result = subprocess.run(['wsl', '--list', '--verbose'], capture_output=True, text=True, timeout=10)
    decoded_output = result.stdout.encode('utf-8').decode('utf-16').replace('\x00', '')
    
    instances = []

    print(decoded_output)

    for line in decoded_output.splitlines()[1:]:  # Skip the header line
        line = line.lstrip('*').strip()  # Remove the leading '*' if present and strip whitespace
        
        # Split the line into name, state, and version
        parts = line.split(maxsplit=2)
        
        if len(parts) == 3:  # Ensure that the line contains all three parts
            name = parts[0].strip()
            state = parts[1].strip()
            instances.append({'name': name, 'state': state})
    
    print("Final list of instances:")
    print(instances)

    return instances

def delete_instance(instance_name):
    subprocess.run(['wsl', '--unregister', instance_name])

def clone_instance(instance_name):
    export_path = os.path.join(BACKUP_DIR, f'{instance_name}.tar')
    subprocess.run(['wsl', '--export', instance_name, export_path])
    new_instance_name = f'{instance_name}_clone'
    subprocess.run(['wsl', '--import', new_instance_name, BACKUP_DIR, export_path])

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

    print("Final list of distributions:")
    print(distributions)

    return distributions

def install_distribution(distribution_id):
    print(f"Starting installation for distribution: {distribution_id}")
    os.system(f'start cmd /k "wsl --install -d {distribution_id}"')
