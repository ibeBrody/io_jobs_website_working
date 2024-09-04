document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;

    // Check for saved theme preference in localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        if (savedTheme === 'dark-mode' && themeIcon) {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
    }

    // Theme toggle logic
    if (themeToggle && themeIcon) {
        themeToggle.addEventListener('click', function() {
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
                localStorage.setItem('theme', 'dark-mode');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
                localStorage.setItem('theme', 'light-mode');
            }
        });
    }

    // Debug Toggle Logic
    const debugToggle = document.getElementById('debug-toggle');
    const debugInfo = document.getElementById('debug-info');

    if (debugToggle && debugInfo) {
        debugToggle.addEventListener('click', function() {
            debugInfo.style.display = (debugInfo.style.display === 'none' || debugInfo.style.display === '') ? 'block' : 'none';
        });
    }

    // Check All Checkboxes in Debug Mode
    const checkAllButton = document.getElementById('check-all-button');
    if (checkAllButton) {
        checkAllButton.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = true;
            });
        });
    }
});

function toggleSuggestions() {
    var suggestionsList = document.getElementById('suggestions-list');
    var button = document.getElementById('toggle-suggestions');

    // Check the current display style and toggle accordingly
    if (suggestionsList.style.display === 'none' || suggestionsList.style.display === '') {
        suggestionsList.style.display = 'block';
        button.textContent = 'Hide Suggestions';
    } else {
        suggestionsList.style.display = 'none';
        button.textContent = 'Show Suggestions';
    }
}