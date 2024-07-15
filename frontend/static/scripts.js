// Default layout for the recipe book
let selectedLayout = 'layout_1.html';

function produceRecipe() {
    // Gather keywords from input fields
    var keywords = [];
    for (var i = 1; i <= keywordCount; i++) {
        var keyword = document.getElementById('keyword' + i).value.trim();
        if (keyword) {
            keywords.push(keyword);
        }
    }

    // Ensure at least one keyword is provided
    if (keywords.length === 0) {
        alert('Please fill in at least one keyword.');
        return;
    }

    // Show loading message
    toggleLoading(true);

    // Create payload for the POST request
    const payload = {
        keywords: keywords,
        layout: selectedLayout
    };

    // Send POST request to the server
    fetch('http://localhost:8000/generate_recipebook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Hide loading message
        toggleLoading(false);
        // Display the generated recipe book
        displayRecipe(data);
    })
    .catch((error) => {
        // Hide loading message on error
        toggleLoading(false);
        console.error('Error:', error);
    });
}

// Function to toggle loading messages
function toggleLoading(isLoading) {
    const loadingSection = document.getElementById('loading');
    const loadingMessages = document.getElementById('loadingMessages');
    const messages = ["Looking for recipes...", "Curating sources...", "Writing recipes...", "Editing final recipe..."];
    loadingMessages.style.fontFamily = "papyrus";

    if (isLoading) {
        loadingSection.classList.remove('hidden');
        let messageIndex = 0;
        loadingMessages.textContent = messages[messageIndex];
        const interval = setInterval(() => {
            if (messageIndex < messages.length - 1) {
                messageIndex++;
                loadingMessages.textContent = messages[messageIndex];
            } else {
                clearInterval(interval);
            }
        }, 12000);
        loadingSection.dataset.intervalId = interval;
    } else {
        loadingSection.classList.add('hidden');
        clearInterval(loadingSection.dataset.intervalId);
    }
}

// Initialize keyword count
let keywordCount = 1;

// Add event listener for DOMContentLoaded to initialize the form
window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('produceRecipe').addEventListener('click', produceRecipe);
    addIconToLastkeyword();
});

// Function to add icons for adding/removing keyword fields
function addIconToLastkeyword() {
    // Remove icons from all keyword fields
    document.querySelectorAll('.add-keyword, .remove-keyword').forEach(icon => {
        icon.remove();
    });

    // Add icons to the last keyword field only
    const lastkeyword = document.getElementById('keywordGroup' + keywordCount);
    if (lastkeyword) {
        const addIcon = document.createElement('span');
        addIcon.className = 'icon add-keyword';
        addIcon.textContent = '+';
        addIcon.addEventListener('click', addkeywordField);
        lastkeyword.appendChild(addIcon);

        if (keywordCount > 1) {
            const removeIcon = document.createElement('span');
            removeIcon.className = 'icon remove-keyword';
            removeIcon.textContent = '-';
            removeIcon.addEventListener('click', removekeywordField);
            lastkeyword.appendChild(removeIcon);
        }
    }
}

// Function to add a new keyword input field
function addkeywordField() {
    keywordCount++;
    const formGroup = document.createElement('div');
    formGroup.className = 'form-group';
    formGroup.id = 'keywordGroup' + keywordCount;

    const inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.id = 'keyword' + keywordCount;
    inputElement.name = 'keyword' + keywordCount;
    inputElement.className = 'inputText';
    inputElement.required = true;

    formGroup.appendChild(inputElement);
    document.getElementById('keywordForm').appendChild(formGroup);

    addIconToLastkeyword();
}

// Function to remove a keyword input field
function removekeywordField(event) {
    const keywordGroup = event.target.parentElement;
    if (keywordGroup && keywordGroup.id !== 'keywordGroup1') {
        keywordGroup.remove();
        keywordCount--;
        addIconToLastkeyword();
    }
}

// Function to display the generated recipe
function displayRecipe(data) {
    if (data.path) {
        window.location.href = data.path;
    } else {
        console.error('Error: Recipe path not found');
    }
}
