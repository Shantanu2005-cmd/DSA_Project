# app.py - Standalone version without a 'templates' folder

from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# NOTE: Set this to the name of your compiled C++ executable
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
        
        # Capture errors thrown by C++ (e.g., OVERFLOW/UNDERFLOW/Peek fail)
        if result.stderr:
             raise ValueError(result.stderr.strip())

        # Determine the response type based on the command
        if command.endswith(('_peek', '_size', '_capacity')):
            # Single value commands (e.g., "10" or "5")
            return {'type': 'value', 'data': int(output_data)}
        else:
            # Data structure display commands (e.g., "10,20,30" or "")
            if output_data:
                # Convert the comma-separated string to a list of integers
                data_list = [int(x.strip()) for x in output_data.split(',') if x.strip().isdigit()]
            else:
                data_list = []
            return {'type': 'structure', 'data': data_list}

    except subprocess.CalledProcessError as e:
        # Capture the error message printed to stderr by the C++ code
        error_msg = e.stderr.strip() or "Unknown C++ execution error."
        return {'error': error_msg}
    except FileNotFoundError:
        return {'error': f"C++ executable '{C_PLUS_PLUS_EXECUTABLE}' not found. Did you compile it?"}
    except Exception as e:
        return {'error': f"An unexpected server error occurred: {str(e)}"}

# --- Web Routes ---

# 1. Main Page Route (HTML content merged here)
@app.route('/')
def index():
    """Serves the main HTML page directly from a string."""
    # We use f-string formatting here to make the large HTML block readable.
    return HTML_CONTENT

# 2. API Operation Route
@app.route('/api/operate', methods=['POST'])
def operate():
    """Handles all operations and returns the result in JSON."""
    
    req_data = request.get_json()
    command = req_data.get('command')
    value = req_data.get('value')

    result = run_cpp_command(command, value)
    
    if isinstance(result, dict) and 'error' in result:
        # Return HTTP 500 status for errors
        return jsonify({'success': False, 'message': result['error']}), 500
    
    # Success: Send the result (either structure list or single value)
    return jsonify({'success': True, 'result': result})

if __name__ == '__main__':
    # Set executable permissions on Linux/macOS
    if os.name != 'nt' and os.path.exists(C_PLUS_PLUS_EXECUTABLE): 
         os.chmod(C_PLUS_PLUS_EXECUTABLE, 0o755)

    print("Starting Flask server...")
    app.run(debug=True)


# --- HTML Content (Merged from index.html) ---

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSA Stack/Queue Simulator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f4f4f9; }
        .container { max-width: 1200px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); }
        .data-structure-box { border: 1px solid #ddd; padding: 20px; margin-bottom: 25px; border-radius: 8px; background-color: #fcfcff; }
        h1, h2 { color: #2c3e50; }
        .structure-display { 
            display: flex; min-height: 100px; padding: 15px; border: 1px dashed #bbb; border-radius: 4px; 
            background-color: #e8f5e9; 
            justify-content: flex-start; 
        }
        .element { 
            background-color: #388e3c; 
            color: white; padding: 10px 15px; margin: 0 5px; border-radius: 5px; 
            font-weight: bold; min-width: 60px; text-align: center; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: all 0.3s ease; 
        }
        #stack-container { flex-direction: column-reverse; align-items: center; background-color: #fbecec; }
        #stack-container .element { width: 100px; margin: 5px 0; }
        #queue-container { flex-direction: row; align-items: center; }
        input[type="number"], button { padding: 10px 15px; margin-right: 10px; border-radius: 5px; border: 1px solid #ccc; font-size: 16px; }
        button { background-color: #3498db; color: white; cursor: pointer; border: none; transition: background-color 0.2s; }
        button:hover { background-color: #2980b9; }
        .controls { margin-top: 15px; display: flex; align-items: center; flex-wrap: wrap; }
        #message-area { color: #c0392b; font-weight: bold; margin-top: 15px; border: 1px solid #e74c3c; padding: 10px; border-radius: 4px; background-color: #f9e3e1; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Stack & Queue DSA Simulator</h1>
        <p>Backend Logic: **C++** | Web Interface: **Python Flask + HTML/JS** | Max Size: **5**</p>

        <div style="margin-bottom: 30px; padding: 10px; border: 1px solid #ccc; border-radius: 8px;">
            <label for="inputValue" style="font-size: 1.1em; font-weight: 600;">Value to PUSH/ENQUEUE:</label>
            <input type="number" id="inputValue" value="10" min="1" max="999">
        </div>

        <div class="data-structure-box">
            <h2>STACK (LIFO)</h2>
            <p>Elements are added and removed from the **Top**.</p>
            <div class="structure-display" id="stack-container">
                <p>Stack is empty. Push an element!</p>
            </div>
            <div class="controls">
                <button onclick="operate('stack_push')">PUSH</button>
                <button onclick="operate('stack_pop')">POP</button>
                <button onclick="operateValue('stack_peek', 'Stack Peek')">PEEK</button>
                <button onclick="operateValue('stack_size', 'Stack Size')">SIZE</button>
                <button onclick="operateValue('stack_capacity', 'Stack Capacity')">CAPACITY</button>
            </div>
        </div>

        <div class="data-structure-box">
            <h2>QUEUE (FIFO)</h2>
            <p>Elements are ENQUEUED at the **Rear** and DEQUEUED from the **Front**.</p>
            <div class="structure-display" id="queue-container">
                <p>Queue is empty. Enqueue an element!</p>
            </div>
            <div class="controls">
                <button onclick="operate('queue_enqueue')">ENQUEUE</button>
                <button onclick="operate('queue_dequeue')">DEQUEUE</button>
                <button onclick="operateValue('queue_peek', 'Queue Peek')">PEEK</button>
                <button onclick="operateValue('queue_size', 'Queue Size')">SIZE</button>
                <button onclick="operateValue('queue_capacity', 'Queue Capacity')">CAPACITY</button>
            </div>
        </div>

        <div id="message-area"></div>
    </div>

    <script>
        const stackContainer = document.getElementById('stack-container');
        const queueContainer = document.getElementById('queue-container');
        const inputValue = document.getElementById('inputValue');
        const messageArea = document.getElementById('message-area');

        // --- RENDER LOGIC ---
        function renderStructure(container, data, type) {
            container.innerHTML = '';
            if (data.length === 0) {
                container.innerHTML = `<p>${type} is empty.</p>`;
                return;
            }

            data.forEach((item, index) => {
                const element = document.createElement('div');
                element.className = 'element';
                element.textContent = item;
                
                // Highlight the Top/Front element
                if ((type === 'Stack' && index === data.length - 1) || (type === 'Queue' && index === 0)) {
                    element.style.backgroundColor = '#e67e22'; // Orange
                    element.textContent += (type === 'Stack' ? ' (TOP)' : ' (FRONT)');
                }
                
                container.appendChild(element);
            });
        }

        // --- API CALL LOGIC for PUSH/POP/ENQUEUE/DEQUEUE (Structure-changing operations) ---
        async function operate(command) {
            let value = null;
            messageArea.style.display = 'none'; 
            messageArea.textContent = ''; 

            if (command.includes('push') || command.includes('enqueue')) {
                value = parseInt(inputValue.value);
                if (isNaN(value) || value === null) {
                    messageArea.textContent = "Please enter a valid number for the operation.";
                    messageArea.style.display = 'block';
                    return;
                }
            }

            try {
                const response = await fetch('/api/operate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ command: command, value: value })
                });

                const result = await response.json();

                if (!response.ok || !result.success) {
                    throw new Error(result.message || 'Operation failed on the server side.');
                }
                
                // Expects: result.result = { type: 'structure', data: [10, 20] }
                if (result.result.type === 'structure') {
                    const typeName = command.includes('stack') ? 'Stack' : 'Queue';
                    const container = command.includes('stack') ? stackContainer : queueContainer;
                    renderStructure(container, result.result.data, typeName);
                    
                    // Display success message for clarity
                    if (command.includes('push')) messageArea.textContent = `✅ PUSH successful.`;
                    if (command.includes('pop')) messageArea.textContent = `✅ POP successful.`;
                    if (command.includes('enqueue')) messageArea.textContent = `✅ ENQUEUE successful.`;
                    if (command.includes('dequeue')) messageArea.textContent = `✅ DEQUEUE successful.`;
                    messageArea.style.backgroundColor = '#d4edda';
                    messageArea.style.color = '#155724';
                    messageArea.style.display = 'block';
                }

            } catch (error) {
                messageArea.textContent = 'ERROR: ' + error.message;
                messageArea.style.backgroundColor = '#f9e3e1';
                messageArea.style.color = '#c0392b';
                messageArea.style.display = 'block';
            }
        }
        
        // --- API CALL LOGIC for PEEK/SIZE/CAPACITY (Value-returning operations) ---
        async function operateValue(command, displayTitle) {
            messageArea.style.display = 'none'; 
            messageArea.textContent = ''; 
            
            try {
                const response = await fetch('/api/operate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ command: command })
                });

                const result = await response.json();

                if (!response.ok || !result.success) {
                    throw new Error(result.message || 'Operation failed on the server side.');
                }
                
                // Expects: result.result = { type: 'value', data: 5 }
                if (result.result.type === 'value') {
                    messageArea.textContent = `👉 ${displayTitle}: ${result.result.data}`;
                    messageArea.style.backgroundColor = '#dbe5f7';
                    messageArea.style.color = '#1f3c6e';
                    messageArea.style.display = 'block';
                }

            } catch (error) {
                messageArea.textContent = 'ERROR: ' + error.message;
                messageArea.style.backgroundColor = '#f9e3e1';
                messageArea.style.color = '#c0392b';
                messageArea.style.display = 'block';
            }
        }

        // Initialize display on page load
        window.onload = () => {
             operate('stack_display');
             operate('queue_display');
        }
    </script>
</body>
</html>
"""