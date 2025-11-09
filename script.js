// script.js

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

// --- Main API Request Handler ---
async function apiRequest(command, value = null) {
    messageArea.style.display = 'none'; 
    messageArea.textContent = ''; 

    try {
        const response = await fetch('/api/operate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ command: command, value: value })
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            // Error handling for Overflow, Underflow, etc.
            throw new Error(result.message || 'Operation failed on the server side.');
        }
        
        // Return the structured result object: { type: 'structure'/'value', data: ... }
        return result.result; 

    } catch (error) {
        // Display error message from C++ or network failure
        messageArea.textContent = 'ERROR: ' + error.message;
        messageArea.style.backgroundColor = '#f9e3e1';
        messageArea.style.color = '#c0392b';
        messageArea.style.display = 'block';
        return null; // Return null on failure
    }
}

// --- 1. Structure-Changing Operations (PUSH, POP, ENQUEUE, DEQUEUE) ---
async function operate(command) {
    let value = null;

    if (command.includes('push') || command.includes('enqueue')) {
        value = parseInt(inputValue.value);
        if (isNaN(value) || value === null) {
            messageArea.textContent = "Please enter a valid number for the operation.";
            messageArea.style.backgroundColor = '#f9e3e1';
            messageArea.style.color = '#c0392b';
            messageArea.style.display = 'block';
            return;
        }
    }

    const result = await apiRequest(command, value);

    if (result && result.type === 'structure') {
        const typeName = command.includes('stack') ? 'Stack' : 'Queue';
        const container = command.includes('stack') ? stackContainer : queueContainer;
        renderStructure(container, result.data, typeName);
        
        // Display success
        let opName = command.split('_')[1].toUpperCase();
        messageArea.textContent = `✅ ${opName} successful.`;
        messageArea.style.backgroundColor = '#d4edda';
        messageArea.style.color = '#155724';
        messageArea.style.display = 'block';
    }
}

// --- 2. Value-Returning Operations (PEEK, SIZE, CAPACITY) ---
async function operateValue(command, displayTitle) {
    const result = await apiRequest(command);
    
    if (result && result.type === 'value') {
        messageArea.textContent = `👉 ${displayTitle}: ${result.data}`;
        messageArea.style.backgroundColor = '#dbe5f7';
        messageArea.style.color = '#1f3c6e';
        messageArea.style.display = 'block';
    }
}

// Initialize display on page load by fetching current state
window.onload = () => {
     operate('stack_display');
     operate('queue_display');
}