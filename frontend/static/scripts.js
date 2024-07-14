
let selectedLayout = 'layout_1.html'; // Default layout

// function selectLayout(event) {
//     document.querySelectorAll('.layout-icon').forEach(icon => {
//         icon.classList.remove('selected');
//     });
//     event.target.classList.add('selected');
//     selectedLayout = event.target.getAttribute('data-layout');
// }


function produceRecipe() {
    var keywords = [];
    for (var i = 1; i <= keywordCount; i++) {
        var keyword = document.getElementById('keyword' + i).value.trim();
        if (keyword) {
            keywords.push(keyword);
        }
    }

    if (keywords.length === 0) {
        alert('Please fill in at least one keyword.');
        return;
    }

        // Show loading animation
    toggleLoading(true);


    const payload = {
        keywords: keywords,
        layout: selectedLayout
    };

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
        toggleLoading(false);
        displayRecipe(data);
    })
    .catch((error) => {
        toggleLoading(false);
        console.error('Error:', error);
    });
}

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


let keywordCount = 1;

window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('produceRecipe').addEventListener('click', produceRecipe);
    // add layout selection feature later time permitting
    // document.querySelectorAll('.layout-icon').forEach(icon => {
    //     icon.addEventListener('click', selectLayout);
    // });
    addIconToLastkeyword();
});

function addIconToLastkeyword() {
    // Remove icons from all keywords
    document.querySelectorAll('.add-keyword, .remove-keyword').forEach(icon => {
        icon.remove();
    });

    // Add icons to the last keyword only
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


function removekeywordField(event) {
    const keywordGroup = event.target.parentElement;
    if (keywordGroup && keywordGroup.id !== 'keywordGroup1') {
        keywordGroup.remove();
        keywordCount--;
        addIconToLastkeyword();
    }
}

function displayRecipe(data) {
    if (data.path) {
        window.location.href = data.path;
    } else {
        console.error('Error: Recipe path not found');
    }
}