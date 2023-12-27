function main() {
    const logIn = document.querySelector("#log-in");
    const signUp = document.querySelector("#sign-up");

    logIn.addEventListener('click', () => {
        $('.modal-body').load("{{ url_for('static', filename='Webpage/user_login.html') }}");
    });

    signUp.addEventListener('click', () => {
        $('.modal-body').load("{{ url_for('static', filename='Webpage/user_signup.html') }}");
    });
}

document.addEventListener('DOMContentLoaded', main);
