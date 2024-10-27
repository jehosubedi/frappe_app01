document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    if (result.message) {
        alert(result.message);
        // Redirect to login page after successful registration
        window.location.href = "/";
    } else if (result.error) {
        alert(result.error);
    }
});

