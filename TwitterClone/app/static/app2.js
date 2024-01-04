function main() {
    const logIn = document.querySelector("#log-in");
    const signUp = document.querySelector("#sign-up");
    const presentationBtn = document.querySelector("#user-action-presentation");
    const activityBtn = document.querySelector("#user-action-activity");
    const workBtn = document.querySelector("#user-action-work");
    const otherBtn = document.querySelector("#user-action-other");
    const navLinks = document.querySelectorAll('.nav-link');

    /*
    logIn.addEventListener('click', () => {
        $('.modal-body').load("{{ url_for('static', filename='Webpage/user_login.html') }}");
    });

    signUp.addEventListener('click', () => {
        $('.modal-body').load("{{ url_for('static', filename='Webpage/user_signup.html') }}");
    });
    */

    presentationBtn.addEventListener('click', () => {
        $('#user-profile-section').html(
            '<span> \
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ex, quam nihil. Corrupti, cupiditate sequi exercitationem distinctio nulla animi odio accusantium magnam, quam quae aliquam, nam hic unde illum repellat quisquam! \
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus aspernatur dolore minima, commodi cumque doloribus. Eligendi repellendus laboriosam at neque, voluptatum minima dolorem. Similique, fugiat! Architecto expedita doloribus nostrum dolorum. \
                Lorem ipsum, dolor sit amet consectetur adipisicing elit. Exercitationem nulla optio excepturi amet quo temporibus, ea quas asperiores voluptatem sint eligendi quae, beatae adipisci sit veritatis deserunt perspiciatis nostrum velit. \
            </span>'
        );
    });

    activityBtn.addEventListener('click', () => {
        $('#user-profile-section').html(
            'Lorem ipsum dolor sit amet consectetur adipisicing elit. Maiores eos doloremque labore dignissimos necessitatibus architecto omnis eaque nesciunt, ipsum deserunt veritatis alias dolorem itaque, eveniet debitis voluptate dolor velit accusantium! \
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique, dignissimos laborum! Sequi libero officia eum deleniti ipsum impedit nobis commodi, autem labore quisquam voluptatibus alias itaque vitae culpa cum aspernatur. \
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Nulla velit, enim repellat repudiandae nemo soluta quos sit ipsa magni sed minima omnis aperiam animi sequi! Velit temporibus minima maxime veritatis. \
            \
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat corrupti tenetur iusto assumenda error rerum, quis ullam quos aliquid fugiat eos adipisci voluptas dolore deserunt et sapiente obcaecati quod explicabo. \
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatum exercitationem rem perspiciatis fugit minima voluptatibus amet ipsum labore, excepturi magnam? Quo a odit, possimus illo voluptas assumenda modi facere quasi.'
        );
    });

    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            // Remove the 'active' class from all links
            navLinks.forEach(function (navLink) {
                navLink.classList.remove('active');
            });

            // Add the 'active' class to the clicked link
            link.classList.add('active');
        });
    });
}

document.addEventListener('DOMContentLoaded', main);
document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.flash');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.display = 'none'; // Hide flash messages after 5 seconds
        }, 5000);
    });
});
