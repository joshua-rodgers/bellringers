/**
 * Bell Ringers - Main JavaScript
 * Handles user sessions, API calls, and UI interactions
 */

// ===== User Handle Management =====
function generateHandle() {
    const adjectives = [
        'clever', 'bright', 'swift', 'bold', 'wise', 'keen', 'sharp', 'quick',
        'smart', 'agile', 'creative', 'dynamic', 'electric', 'quantum', 'cyber',
        'digital', 'logical', 'recursive', 'compiled', 'debugged'
    ];

    const nouns = [
        'python', 'query', 'loop', 'function', 'array', 'class', 'method', 'variable',
        'algorithm', 'compiler', 'parser', 'buffer', 'stack', 'heap', 'tree',
        'graph', 'node', 'pointer', 'thread', 'cache'
    ];

    const adj = adjectives[Math.floor(Math.random() * adjectives.length)];
    const noun = nouns[Math.floor(Math.random() * nouns.length)];
    const num = Math.floor(Math.random() * 999) + 1;

    return `${adj}-${noun}-${num}`;
}

function getUserHandle() {
    let handle = localStorage.getItem('user_handle');
    if (!handle) {
        handle = generateHandle();
        localStorage.setItem('user_handle', handle);
        // Register user on backend
        fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ handle: handle })
        });
    }
    return handle;
}

function displayUserHandle() {
    const handle = getUserHandle();
    const displayElement = document.getElementById('userHandleDisplay');
    if (displayElement) {
        displayElement.textContent = `👤 ${handle}`;
    }
}

// ===== Navigation Toggle (Mobile) =====
function setupNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
}

// ===== Generator Page Logic =====
let lockedSlots = {
    topic: false,
    format: false,
    constraint: false
};

let currentGeneration = null;

function setupGenerator() {
    const topicLock = document.getElementById('topicLock');
    const formatLock = document.getElementById('formatLock');
    const constraintLock = document.getElementById('constraintLock');
    const spinBtn = document.getElementById('spinBtn');
    const generateBtn = document.getElementById('generateBtn');

    if (!topicLock) return; // Not on generator page

    // Lock button handlers
    topicLock.addEventListener('click', () => toggleLock('topic'));
    formatLock.addEventListener('click', () => toggleLock('format'));
    constraintLock.addEventListener('click', () => toggleLock('constraint'));

    // Spin button handler
    spinBtn.addEventListener('click', spinSlots);

    // Generate button handler
    generateBtn.addEventListener('click', generateBellRinger);
}

function toggleLock(slotName) {
    lockedSlots[slotName] = !lockedSlots[slotName];
    const lockBtn = document.getElementById(`${slotName}Lock`);
    const slot = document.getElementById(`${slotName}Slot`);

    if (lockedSlots[slotName]) {
        lockBtn.textContent = '🔒';
        slot.classList.add('locked');
    } else {
        lockBtn.textContent = '🔓';
        slot.classList.remove('locked');
    }
}

async function spinSlots() {
    const spinBtn = document.getElementById('spinBtn');
    spinBtn.disabled = true;
    spinBtn.textContent = '🎰 Spinning...';

    // Visual spinning animation
    const slots = ['topic', 'format', 'constraint'];
    slots.forEach(slot => {
        if (!lockedSlots[slot]) {
            const select = document.getElementById(`${slot}Select`);
            select.classList.add('spinning');
        }
    });

    try {
        const response = await fetch('/api/spin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ locked: lockedSlots })
        });

        const data = await response.json();

        // Update unlocked slots with new values
        setTimeout(() => {
            if (data.topic) {
                document.getElementById('topicSelect').value = data.topic;
            }
            if (data.format) {
                document.getElementById('formatSelect').value = data.format;
            }
            if (data.constraint) {
                document.getElementById('constraintSelect').value = data.constraint;
            }

            // Remove spinning animation
            slots.forEach(slot => {
                const select = document.getElementById(`${slot}Select`);
                select.classList.remove('spinning');
            });

            spinBtn.disabled = false;
            spinBtn.textContent = '🎰 Spin Unlocked';
        }, 500);

    } catch (error) {
        console.error('Spin error:', error);
        alert('Error spinning slots');
        spinBtn.disabled = false;
        spinBtn.textContent = '🎰 Spin Unlocked';
    }
}

async function generateBellRinger() {
    const generateBtn = document.getElementById('generateBtn');
    const resultContainer = document.getElementById('resultContainer');
    const resultContent = document.getElementById('resultContent');

    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner"></span> Generating...';

    const topic = document.getElementById('topicSelect').value;
    const format = document.getElementById('formatSelect').value;
    const constraint = document.getElementById('constraintSelect').value;

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: topic,
                format: format,
                constraint: constraint
            })
        });

        const data = await response.json();

        if (data.success) {
            currentGeneration = data;
            resultContent.textContent = data.content;
            resultContainer.classList.add('active');
            resultContainer.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + data.error);
        }

    } catch (error) {
        console.error('Generation error:', error);
        alert('Error generating bell ringer');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = '✨ Generate!';
    }
}

async function saveBellRinger() {
    if (!currentGeneration) return;

    const saveBtn = document.getElementById('saveBtn');
    saveBtn.disabled = true;

    try {
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentGeneration)
        });

        const data = await response.json();

        if (data.success) {
            showAlert('Saved to your binder!', 'success');
        } else {
            showAlert('Error: ' + data.error, 'error');
        }

    } catch (error) {
        console.error('Save error:', error);
        showAlert('Error saving bell ringer', 'error');
    } finally {
        saveBtn.disabled = false;
    }
}

async function publishBellRinger() {
    if (!currentGeneration) return;

    const publishBtn = document.getElementById('publishBtn');
    publishBtn.disabled = true;

    try {
        const response = await fetch('/api/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentGeneration)
        });

        const data = await response.json();

        if (data.success) {
            showAlert(data.message, 'info');
        } else {
            showAlert('Error: ' + data.error, 'error');
        }

    } catch (error) {
        console.error('Publish error:', error);
        showAlert('Error publishing bell ringer', 'error');
    } finally {
        publishBtn.disabled = false;
    }
}

function printBellRinger() {
    if (!currentGeneration) return;
    // Create a temporary print window
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bell Ringer - ${currentGeneration.topic}</title>
            <style>
                body {
                    font-family: Georgia, serif;
                    line-height: 1.8;
                    max-width: 8.5in;
                    margin: 0.5in auto;
                    padding: 1in;
                }
                h1 { color: #333; }
                pre { white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <pre>${currentGeneration.content}</pre>
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => printWindow.print(), 500);
}

// ===== Feed & Binder Functions =====
async function addToBinder(bellRingerId, button) {
    button.disabled = true;
    const originalText = button.textContent;
    button.textContent = 'Adding...';

    try {
        const response = await fetch(`/api/add-to-binder/${bellRingerId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showAlert(data.message, 'success');
            button.textContent = '✓ In Binder';
        } else {
            showAlert(data.message, 'info');
            button.textContent = originalText;
            button.disabled = false;
        }

    } catch (error) {
        console.error('Add to binder error:', error);
        showAlert('Error adding to binder', 'error');
        button.textContent = originalText;
        button.disabled = false;
    }
}

// ===== Admin Functions =====
async function adminLogin(event) {
    event.preventDefault();

    const username = document.getElementById('adminUsername').value;
    const password = document.getElementById('adminPassword').value;

    try {
        const response = await fetch('/admin/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            window.location.href = '/admin/dashboard';
        } else {
            showAlert('Invalid credentials', 'error');
        }

    } catch (error) {
        console.error('Login error:', error);
        showAlert('Login error', 'error');
    }
}

async function approveBellRinger(bellRingerId, button) {
    button.disabled = true;

    try {
        const response = await fetch(`/admin/api/approve/${bellRingerId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            button.textContent = '✓ Approved';
            button.classList.remove('btn-primary');
            button.classList.add('btn-secondary');
        } else {
            showAlert('Error: ' + data.error, 'error');
            button.disabled = false;
        }

    } catch (error) {
        console.error('Approve error:', error);
        showAlert('Error approving', 'error');
        button.disabled = false;
    }
}

async function deleteBellRinger(bellRingerId, button) {
    if (!confirm('Are you sure you want to delete this bell ringer?')) {
        return;
    }

    button.disabled = true;

    try {
        const response = await fetch(`/admin/api/delete/${bellRingerId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            button.closest('.card').remove();
            showAlert('Deleted successfully', 'success');
        } else {
            showAlert('Error: ' + data.error, 'error');
            button.disabled = false;
        }

    } catch (error) {
        console.error('Delete error:', error);
        showAlert('Error deleting', 'error');
        button.disabled = false;
    }
}

// ===== Utility Functions =====
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.maxWidth = '300px';

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// ===== Initialize on Page Load =====
document.addEventListener('DOMContentLoaded', () => {
    displayUserHandle();
    setupNavigation();
    setupGenerator();

    // Attach global functions for inline handlers
    window.saveBellRinger = saveBellRinger;
    window.publishBellRinger = publishBellRinger;
    window.printBellRinger = printBellRinger;
    window.addToBinder = addToBinder;
    window.approveBellRinger = approveBellRinger;
    window.deleteBellRinger = deleteBellRinger;
    window.adminLogin = adminLogin;
});
