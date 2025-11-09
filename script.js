// Function attached to the "PUSH" button
async function pushToStack() {
    const value = document.getElementById('inputValue').value;
    const response = await fetch('/operate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ op: 'stack_push', val: value })
    });
    const result = await response.json();
    
    // Update the visual representation on the web page
    updateDisplay(result.data); 
}