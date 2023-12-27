function main() {
    const logIn = document.querySelector("#log-in");
    const signUp = document.querySelector("#sign-up");

    logIn.addEventListener('click', function() {
        $('.modal-body').html();
    })
    
    signUp.addEventListener('click', () => {
        $('.modal-body').html();
    })

    $(document).ready(function () {
        
    })
}

document.addEventListener('DOMContentLoaded', main);
