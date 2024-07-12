
let selectedLayout = 'layout_1.html'; // Default layout

function selectLayout(event) {
    document.querySelectorAll('.layout-icon').forEach(icon => {
        icon.classList.remove('selected');
    });
    event.target.classList.add('selected');
    selectedLayout = event.target.getAttribute('data-layout');
}


function produceRecipe() {
    var ingredients = [];
    for (var i = 1; i <= ingredientCount; i++) {
        var ingredient = document.getElementById('ingredient' + i).value.trim();
        if (ingredient) {
            ingredients.push(ingredient);
        }
    }

    if (ingredients.length === 0) {
        alert('Please fill in at least one ingredient.');
        return;
    }

        // Show loading animation
    toggleLoading(true);


    const payload = {
        ingredients: ingredients,
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


let ingredientCount = 1;

window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('produceRecipe').addEventListener('click', produceRecipe);
    // add layout selection feature later time permitting
    // document.querySelectorAll('.layout-icon').forEach(icon => {
    //     icon.addEventListener('click', selectLayout);
    // });
    addIconToLastingredient();
});

function addIconToLastingredient() {
    // Remove icons from all ingredients
    document.querySelectorAll('.add-ingredient, .remove-ingredient').forEach(icon => {
        icon.remove();
    });

    // Add icons to the last ingredient only
    const lastingredient = document.getElementById('ingredientGroup' + ingredientCount);
    if (lastingredient) {
        const addIcon = document.createElement('span');
        addIcon.className = 'icon add-ingredient';
        addIcon.textContent = '+';
        addIcon.addEventListener('click', addingredientField);
        lastingredient.appendChild(addIcon);

        if (ingredientCount > 1) {
            const removeIcon = document.createElement('span');
            removeIcon.className = 'icon remove-ingredient';
            removeIcon.textContent = '-';
            removeIcon.addEventListener('click', removeingredientField);
            lastingredient.appendChild(removeIcon);
        }
    }
}

function addingredientField() {
    ingredientCount++;
    const formGroup = document.createElement('div');
    formGroup.className = 'form-group';
    formGroup.id = 'ingredientGroup' + ingredientCount;

    const inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.id = 'ingredient' + ingredientCount;
    inputElement.name = 'ingredient' + ingredientCount;
    inputElement.className = 'inputText';
    inputElement.required = true;

    formGroup.appendChild(inputElement);

    document.getElementById('ingredientForm').appendChild(formGroup);

    addIconToLastingredient();
}


function removeingredientField(event) {
    const ingredientGroup = event.target.parentElement;
    if (ingredientGroup && ingredientGroup.id !== 'ingredientGroup1') {
        ingredientGroup.remove();
        ingredientCount--;
        addIconToLastingredient();
    }
}

function displayRecipe(data) {
    if (data.path) {
        window.location.href = data.path;
    } else {
        console.error('Error: Recipe path not found');
    }
}