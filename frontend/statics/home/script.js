const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

hamburger.addEventListener('click', function() {
    // Toggle active/inactive classes on the navigation links
    if (navLinks.classList.contains('inactive')) {
        navLinks.classList.remove('inactive');
        navLinks.classList.add('active');
    } else {
        navLinks.classList.remove('active');
        navLinks.classList.add('inactive');
    }
});

function navigateToHome() {
    window.location.href = 'home.html'; // Adjust the path to your home page
}

function navigateToPrediction() {
    window.location.href = 'predict.html'; // Adjust the path to your prediction page
}
