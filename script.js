const modeSelect = document.getElementById("mode");
const valueInput = document.getElementById("valueInput");
const pushBtn = document.getElementById("pushBtn");
const popBtn = document.getElementById("popBtn");
const peekBtn = document.getElementById("peekBtn");
const displayBtn = document.getElementById("displayBtn");
const checkEmptyBtn = document.getElementById("checkEmptyBtn");
const checkFullBtn = document.getElementById("checkFullBtn");
const container = document.getElementById("visual-container");
const message = document.getElementById("message");
const outputBox = document.getElementById("output");

let data = [];
const MAX_SIZE = 7;

function render() {
  container.innerHTML = "";
  data.forEach((val) => {
    const div = document.createElement("div");
    div.className = "element";
    div.textContent = val;
    container.appendChild(div);
  });
}

function setMessage(msg, color = "red") {
  message.textContent = msg;
  message.style.color = color;
}

function setOutput(text) {
  outputBox.textContent = text;
}

function pushOrEnqueue() {
  const value = valueInput.value.trim();
  if (!value) return setMessage("⚠️ Please enter a value!");
  if (data.length >= MAX_SIZE) return setMessage("🚫 Overflow! Structure full.");

  setMessage("");

  if (modeSelect.value === "stack") {
    data.push(value);
    setOutput(`Pushed ${value} → Stack: [${data.join(", ")}]`);
  } else {
    data.push(value);
    setOutput(`Enqueued ${value} → Queue: [${data.join(", ")}]`);
  }

  valueInput.value = "";
  render();
}

function popOrDequeue() {
  if (data.length === 0) return setMessage("⚠️ Underflow! Structure empty.");
  setMessage("");

  let removed;
  if (modeSelect.value === "stack") {
    removed = data.pop();
    setOutput(`Popped ${removed} → Stack: [${data.join(", ")}]`);
  } else {
    removed = data.shift();
    setOutput(`Dequeued ${removed} → Queue: [${data.join(", ")}]`);
  }
  render();
}

function peekOrFront() {
  if (data.length === 0) return setMessage("⚠️ Structure empty.");
  setMessage("");

  if (modeSelect.value === "stack") {
    const top = data[data.length - 1];
    setOutput(`Top element: ${top}`);
  } else {
    const front = data[0];
    const rear = data[data.length - 1];
    setOutput(`Front: ${front}, Rear: ${rear}`);
  }
}

function displayAll() {
  if (data.length === 0) return setOutput("Structure is empty.");
  setMessage("");
  setOutput(`Elements: [${data.join(", ")}]`);
}

function checkEmpty() {
  if (data.length === 0) setOutput("✅ Structure is empty.");
  else setOutput("❌ Structure is not empty.");
}

function checkFull() {
  if (data.length >= MAX_SIZE) setOutput("🚫 Structure is full.");
  else setOutput("🟢 Structure has space.");
}

pushBtn.addEventListener("click", pushOrEnqueue);
popBtn.addEventListener("click", popOrDequeue);
peekBtn.addEventListener("click", peekOrFront);
displayBtn.addEventListener("click", displayAll);
checkEmptyBtn.addEventListener("click", checkEmpty);
checkFullBtn.addEventListener("click", checkFull);
