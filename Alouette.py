import os
import json
import urllib.request
import time
import random
import sys
import subprocess
from datetime import datetime
# Check if domain parameter is provided
if len(sys.argv) != 2:
    print("Usage: python Alouette.py <domain>")
    print("Example: python Alouette.py jeeja.biz")
    sys.exit(1)

domain = sys.argv[1]
# Define the input and output file paths
urls_dir = 'URLs'
input_file = os.path.join(urls_dir, f'{domain}.json')
output_dir = domain
def check_gem_installed():
    """Check if wayback_machine_downloader_straw gem is installed"""
    try:
        result = subprocess.run(['gem', 'list', 'wayback_machine_downloader_straw'],
                              capture_output=True, text=True, check=True)
        return 'wayback_machine_downloader_straw' in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def generate_wayback_json(domain, urls_dir):
    """Generate JSON file using wayback_machine_downloader"""
    # Create URLs directory if it doesn't exist
    os.makedirs(urls_dir, exist_ok=True)

    json_filename = os.path.join(urls_dir, f'{domain}.json')

    if os.path.exists(json_filename):
        print(f"JSON file '{json_filename}' already exists. Skipping generation.")
        return True

    print(f"Generating wayback machine data for {domain}...")
    cmd = [
        'wayback_machine_downloader',
        f'https://www.{domain}',
        '--list',
        '--only',
        r'/\.(jpg|jpeg|png|gif|bmp|webp)$/i'
    ]

    try:
        with open(json_filename, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, check=True)
        print(f"Successfully generated '{json_filename}'")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running wayback_machine_downloader: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: wayback_machine_downloader command not found")
        return False

# Check if wayback_machine_downloader_straw gem is installed
if not check_gem_installed():
    print("Error: wayback_machine_downloader_straw gem is not installed.")
    print("Please install it using: gem install wayback_machine_downloader_straw")
    sys.exit(1)

print("wayback_machine_downloader_straw gem is installed.")

# Generate the JSON file if needed
if not generate_wayback_json(domain, urls_dir):
    print("Failed to generate wayback machine data. Exiting.")
    sys.exit(1)

# Get the start time of the script
start_time = time.time()
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
def download_with_retry(download_url, filename):
    """Download a file with retry logic"""
    max_attempts = 3
    
    for attempt in range(1, max_attempts + 1):
        try:
            urllib.request.urlretrieve(download_url, filename)
            return "Downloaded" if attempt == 1 else f"Downloaded (retry {attempt})"
                    
        except urllib.error.URLError as e:
            if attempt < max_attempts:
                if attempt == 2:  # Only wait on second retry
                    time.sleep(30)
            else:
                return f"Failed to download. Error: {e}"
                
        except Exception as e:
            if attempt < max_attempts:
                if attempt == 2:  # Only wait on second retry
                    time.sleep(30)
            else:
                return f"An unexpected error occurred: {e}"
    
    return "Failed after maximum attempts"
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        print(f"Reading and parsing all data from '{input_file}'...")
        data = json.load(f)
    
    total_images = len(data)
    print(f"Parsing successful. Found {total_images} URLs. Starting downloads...")
    
    for index, file_info in enumerate(data):
        image_number = index + 1
        elapsed_seconds = time.time() - start_time
        
        hours = int(elapsed_seconds // 3600)
        minutes = int((elapsed_seconds % 3600) // 60)
        seconds = int(elapsed_seconds % 60)
        elapsed_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        file_url = file_info.get('file_url')
        timestamp = file_info.get('timestamp')
        file_id = file_info.get('file_id')
        
        if file_url and timestamp and file_id:
            download_url = f"https://web.archive.org/web/{timestamp}if_/{file_url}"
            filename = os.path.join(output_dir, file_id)
            
            if os.path.exists(filename):
                print(f"[{elapsed_time_str}] ({image_number}/{total_images}) Skipping: {filename} already exists.")
                continue
                
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Download with retry logic
            status_message = download_with_retry(download_url, filename)
            
            # Add a random delay between 0.5 and 2.5 seconds
            sleep_time = random.uniform(0.5, 2.5)
            
            # Now, print the full log line with the final status and the pause at the end.
            print(f"[{elapsed_time_str}] ({image_number}/{total_images}) {status_message}: {file_url} - Pausing for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
            
except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
    print(f"Make sure the wayback_machine_downloader generated the file correctly for domain: {domain}")
    print(f"Expected location: {input_file}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON. The file might be corrupted or not in a valid JSON format. Details: {e}")
    
print(f"\nDownload process complete for domain: {domain}")
print(f"Images saved to: {output_dir}/")
print(f"JSON file location: {input_file}")