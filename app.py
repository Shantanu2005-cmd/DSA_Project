# app.py

from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

# NOTE: Make sure this name matches the executable you compile!
C_PLUS_PLUS_EXECUTABLE = "./simulator_cli" 

# --- Helper Function to Run C++ ---
def run_cpp_command(command, value=None):
    """Executes the C++ program with given command and optional value."""
    args = [C_PLUS_PLUS_EXECUTABLE, command]
    if value is not None:
        args.append(str(value))
        
    try:
        # Check=True will raise CalledProcessError if C++ returns non-zero (i.e., an error)
        result = subprocess.run(
            args, capture_output=True, text=True, check=True
        )
        
        output_data = result.stdout.strip()
        
        # Convert the comma-separated string to a list of integers
        if output_data:
            # Handles errors printed to stderr by C++ for overflow/underflow
            if result.stderr:
                 raise ValueError(result.stderr.strip())

            # Split the string by comma and convert each part to an integer
            data_list = [int(x.strip()) for x in output_data.split(',') if x.strip().isdigit()]
        else:
            data_list = []

        return data_list

    except subprocess.CalledProcessError as e:
        # Capture the error message printed to stderr by the C++ code
        error_msg = e.stderr.strip() or "Unknown C++ execution error."
        return {'error': error_msg}
    except FileNotFoundError:
        return {'error': f"C++ executable '{C_PLUS_PLUS_EXECUTABLE}' not found. Did you compile it?"}
    except ValueError as e:
        # Capture errors thrown by C++ (e.g., OVERFLOW/UNDERFLOW)
        return {'error': str(e)}
    except Exception as e:
        return {'error': f"An unexpected server error occurred: {str(e)}"}

# --- Web Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/operate', methods=['POST'])
def operate():
    """Handles all PUSH/POP/ENQUEUE/DEQUEUE requests."""
    
    req_data = request.get_json()
    command = req_data.get('command')
    value = req_data.get('value')

    result = run_cpp_command(command, value)
    
    if isinstance(result, dict) and 'error' in result:
        # Return HTTP 500 status for errors
        return jsonify({'success': False, 'message': result['error']}), 500
    
    # Success: Send the new data structure state back
    return jsonify({'success': True, 'data': result})

if __name__ == '__main__':
    # Ensure the templates directory exists
    if not os.path.exists('./index.html'):
        os.makedirs('./index.html')
        
    # Set executable permissions on Linux/macOS
    if os.name != 'nt' and os.path.exists(C_PLUS_PLUS_EXECUTABLE): 
         os.chmod(C_PLUS_PLUS_EXECUTABLE, 0o755)

    print("Starting Flask server...")
    app.run(debug=True)