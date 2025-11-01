/**
 * QuickWork - Bell Ringers
 * Modern dark theme with prompt-based generation
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

async function getUserHandle() {
    let handle = localStorage.getItem('user_handle');
    if (!handle) {
        handle = generateHandle();
        localStorage.setItem('user_handle', handle);
        console.log('Generated new user handle:', handle);
    } else {
        console.log('Found existing handle:', handle);
    }

    // ALWAYS register/update session on backend
    console.log('Registering session for:', handle);
    try {
        const response = await fetch('/bellringers/api/register', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ handle: handle })
        });

        if (!response.ok) {
            console.error('Registration HTTP error:', response.status, response.statusText);
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        console.log('Registration response:', data);

        if (!data.success) {
            console.error('Registration failed:', data);
        } else {
            console.log('Session created successfully!');
        }
    } catch (error) {
        console.error('Registration error:', error);
    }

    return handle;
}

async function displayUserHandle() {
    const handle = await getUserHandle();
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
let advancedOptionsVisible = false;

function setupGenerator() {
    const topicLock = document.getElementById('topicLock');
    const formatLock = document.getElementById('formatLock');
    const constraintLock = document.getElementById('constraintLock');
    const generateBtn = document.getElementById('generateBtn');
    const randomizeBtn = document.getElementById('randomizeBtn');
    const advancedToggleBtn = document.getElementById('advancedToggleBtn');
    const clearStandardsBtn = document.getElementById('clearStandardsBtn');

    if (!topicLock) return; // Not on generator page

    // Advanced options toggle
    if (advancedToggleBtn) {
        advancedToggleBtn.addEventListener('click', toggleAdvancedOptions);
    }

    // Lock button handlers
    topicLock.addEventListener('click', () => toggleLock('topic'));
    formatLock.addEventListener('click', () => toggleLock('format'));
    constraintLock.addEventListener('click', () => toggleLock('constraint'));

    // Randomize button handler
    if (randomizeBtn) {
        randomizeBtn.addEventListener('click', randomizeUnlocked);
    }

    // Generate button handler
    generateBtn.addEventListener('click', generateBellRinger);

    // Clear standards button handler
    if (clearStandardsBtn) {
        clearStandardsBtn.addEventListener('click', () => {
            document.querySelectorAll('.standards-checkbox').forEach(cb => cb.checked = false);
        });
    }

    // Initialize with random values
    randomizeUnlocked();
}

function toggleAdvancedOptions() {
    const advancedOptions = document.getElementById('advancedOptions');
    const toggleIcon = document.getElementById('toggleIcon');

    advancedOptionsVisible = !advancedOptionsVisible;

    if (advancedOptionsVisible) {
        advancedOptions.classList.add('show');
        toggleIcon.textContent = '∧'; // Up arrow
    } else {
        advancedOptions.classList.remove('show');
        toggleIcon.textContent = '∨'; // Down arrow
    }
}

function toggleLock(slotName) {
    lockedSlots[slotName] = !lockedSlots[slotName];
    const lockBtn = document.getElementById(`${slotName}Lock`);
    const item = document.getElementById(`${slotName}Item`);

    if (lockedSlots[slotName]) {
        lockBtn.textContent = '🔒';
        item.classList.add('locked');
    } else {
        lockBtn.textContent = '🔓';
        item.classList.remove('locked');
    }
}

function randomizeUnlocked() {
    const topicSelect = document.getElementById('topicSelect');
    const formatSelect = document.getElementById('formatSelect');
    const constraintSelect = document.getElementById('constraintSelect');

    // Randomize unlocked dropdowns
    if (!lockedSlots.topic) {
        const randomTopic = Math.floor(Math.random() * topicSelect.options.length);
        topicSelect.selectedIndex = randomTopic;
    }

    if (!lockedSlots.format) {
        const randomFormat = Math.floor(Math.random() * formatSelect.options.length);
        formatSelect.selectedIndex = randomFormat;
    }

    if (!lockedSlots.constraint) {
        const randomConstraint = Math.floor(Math.random() * constraintSelect.options.length);
        constraintSelect.selectedIndex = randomConstraint;
    }
}

async function generateBellRinger() {
    const generateBtn = document.getElementById('generateBtn');
    const resultContainer = document.getElementById('resultContainer');
    const resultContent = document.getElementById('resultContent');
    const promptInput = document.getElementById('promptInput');

    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner"></span> Generating...';

    // If advanced options are hidden, randomize everything
    if (!advancedOptionsVisible) {
        randomizeUnlocked();
    }

    const topic = document.getElementById('topicSelect').value;
    const format = document.getElementById('formatSelect').value;
    const constraint = document.getElementById('constraintSelect').value;
    const prompt = promptInput.value.trim();

    // Get all checked standards
    const standardCheckboxes = document.querySelectorAll('.standards-checkbox:checked');
    const standards = Array.from(standardCheckboxes).map(cb => cb.value);

    console.log('Generating bell ringer:', { topic, format, constraint, prompt, standards });

    try {
        const response = await fetch('/bellringers/api/generate', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: topic,
                format: format,
                constraint: constraint,
                prompt: prompt,
                standards: standards
            })
        });

        console.log('Generate response status:', response.status);

        if (!response.ok) {
            if (response.status === 401) {
                const errorMsg = 'Session expired or not found. Reloading page to create new session...';
                console.error(errorMsg);
                alert(errorMsg);
                setTimeout(() => location.reload(), 1000);
                return;
            }
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Generate response data:', data);

        if (data.success) {
            currentGeneration = data;
            resultContent.innerHTML = data.content;
            resultContainer.classList.add('active');
            resultContainer.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }

    } catch (error) {
        console.error('Generation error:', error);
        alert('Error generating bell ringer: ' + error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate';
    }
}

async function saveBellRinger() {
    if (!currentGeneration) return;

    const saveBtn = document.getElementById('saveBtn');
    saveBtn.disabled = true;

    try {
        const response = await fetch('/bellringers/api/save', {
            method: 'POST',
            credentials: 'include',
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
        const response = await fetch('/bellringers/api/publish', {
            method: 'POST',
            credentials: 'include',
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
                pre {
                    white-space: pre-wrap;
                    background: #f5f5f5;
                    padding: 1rem;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            ${currentGeneration.content}
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
        const response = await fetch(`/bellringers/api/add-to-binder/${bellRingerId}`, {
            method: 'POST',
            credentials: 'include'
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
        const response = await fetch('/bellringers/admin/login', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.success) {
            window.location.href = '/bellringers/admin/dashboard';
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
        const response = await fetch(`/bellringers/admin/api/approve/${bellRingerId}`, {
            method: 'POST',
            credentials: 'include'
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
        const response = await fetch(`/bellringers/admin/api/delete/${bellRingerId}`, {
            method: 'POST',
            credentials: 'include'
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
document.addEventListener('DOMContentLoaded', async () => {
    // Ensure user is registered BEFORE doing anything else
    await displayUserHandle();

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
