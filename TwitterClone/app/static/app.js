function main() {
    const logIn = document.querySelector("#log-in");
    const signUp = document.querySelector("#sign-up");

    logIn.addEventListener('click', function() {
        $('#modal-title').text('Log In');
        $('.modal-body').html('<h1 class="display-3">Welcome Back! \
        <i class="fa-brands fa-twitter fa-sm" id="twitter-sm-logo"></i></h1> \
        <div class="container-fluid"> \
            <div class="row m-1" id="email_register"> \
                <div class="col"> \
                    <label for="email_input">Email</label> \
                    <input type="text" class="form-control" id="email_input" placeholder="Email"> \
                </div> \
            </div> \
            <div class="row m-1" id="password_register"> \
                <div class="col"> \
                    <label for="password_input">Password</label> \
                    <input type="text" class="form-control" id="password_input" placeholder="Create a password"> \
                </div> \
            </div> \
        </div>');
    })
    
    signUp.addEventListener('click', () => {
        $('#modal-title').text('Sign Up');
        $('.modal-body').html('<h1 class="display-1">Welcome to Twitter Clone</h1> \
        <div class="container-fluid"> \
            <i class="fa-brands fa-twitter fa-2xl" id="twitter-2xl-logo"></i> \
            <p class="sign-up-slogan">Post. Discuss. Connect</p> \
            <div class="row m-1" id="email_signup"> \
                <div class="col"> \
                    <label for="email_input">Email</label> \
                    <input type="text" class="form-control" id="email_input" placeholder="Email"> \
                </div> \
            </div> \
            <div class="row m-1" id="username_signup"> \
                <div class="col"> \
                    <label for="username_input">User Name</label> \
                    <input type="text" class="form-control" id="username_input" placeholder="Email"> \
                </div> \
            </div> \
            <div class="row m-1" id="password_signup"> \
                <div class="col"> \
                    <label for="password_input">Password</label> \
                    <input type="text" class="form-control" id="password_input" placeholder="Create a password"> \
                </div> \
            </div> \
            <div class="row m-1" id="birthdate_signup"> \
                <div class="col"> \
                    <label for="birthdate_input">Birthdate</label> \
                    <input type="date" class="form-control" id="birthdate_input" placeholder="mm/dd/yyyy"> \
                </div> \
            </div> \
        </div>');
    })
}

document.addEventListener('DOMContentLoaded', main);
