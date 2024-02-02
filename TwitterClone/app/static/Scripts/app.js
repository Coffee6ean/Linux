const BASE_URL = 'http://127.0.0.1:5000/'

async function getLoggedUserData(username) {
    try {
        let url = BASE_URL + `api/v1/user/${username}`;
        console.log(url);
        const req = await axios.get(url);
        const res = req.data;
        console.log(res);
        return res;
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
}

function main() {
    const headStyle = document.querySelector('head');
    const usernameTag = document.querySelector('#user-profile-details > h2');
    const presentationBtn = document.querySelector("#user-action-presentation");
    const activityBtn = document.querySelector("#user-action-activity");
    const navLinks = document.querySelectorAll('.nav-link');
    const editPictureBtn = document.querySelector('#profile-picture-icon');
    const editBannerBtn = document.querySelector('#profile-banner-icon');
    const editProfileBtn = document.querySelector('#profile-edit-button');

    presentationBtn.addEventListener('click', async () => {
        // Create a new link element
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = '/static/Style/User/user_presentation.css';  // Update this with your actual path
            
        // Append the link element to the head
        document.head.appendChild(link);

        const username = usernameTag.innerText;
        let url = BASE_URL + `v1/user/${username}/presentation`;
        console.log(url);

        // Load content dynamically using jQuery
        $('#user-profile-section').load(url, function(response, status, xhr) {
            if (status == "error") {
                console.error("Error loading content:", xhr.statusText);
            } else {
                // Code to execute after content is loaded
                console.log("Content loaded successfully!");
            }
        });
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

    editPictureBtn.addEventListener('click', () => {
        const popover = document.querySelector('#profile-picture-popover');
        popover.classList.toggle('hideForm');
    });

    editBannerBtn.addEventListener('click', () => {
        const popover = document.querySelector('#banner-picture-popover');
        popover.classList.toggle('hideForm');
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

    // Trigger click on the Presentation button to load its content on page load
    presentationBtn.click();
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
