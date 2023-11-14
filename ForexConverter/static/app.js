// Constants for API endpoints
const ENDPOINTS = {
    LIVE_RATES: 'live',
    CURR_LIST: 'list'
};

// Global variables for currency data and quotes
let CURRENCY_LIST = [];
let QUOTES = {};
let SOURCE;

// Access key for API requests
const ACCESS_KEY = '62009edbc15ca236e2585d316889871b';

// DOM elements for user input and interaction
const convertFrom = document.querySelector('#convert-from');
const convertTo = document.querySelector('#convert-to');
const firstDropdown = document.querySelector('#first-dropdown-list');
const secondDropdown = document.querySelector('#second-dropdown-list');
const submit = document.querySelector('#submit');

// Asynchronous function to fetch live currency rates and source
async function fetchCurrencyData(endpoint = ENDPOINTS.LIVE_RATES, 
                                 accessKey = ACCESS_KEY) {
    try {
        // Make API request to get live rates
        const response = await axios.get(
            `http://api.exchangerate.host/${endpoint}?access_key=${accessKey}`);
        const { quotes, source } = response.data;

        // Update global variables with API response data
        QUOTES = quotes;
        SOURCE = source;
    } catch (error) {
        // Log any errors that occur during the API request
        console.error(error);
    }
}

// Asynchronous function to fetch the list of supported currencies
async function fetchCurrencyList(endpoint = ENDPOINTS.CURR_LIST, 
                                 accessKey = ACCESS_KEY) {
    try {
        // Make API request to get the list of currencies
        const response = await axios.get(
            `http://api.exchangerate.host/${endpoint}?access_key=${accessKey}`);
        const { currencies } = response.data;

        // Update the global currency list based on user preferences
        CURRENCY_LIST = $("convert-from").hasClass('abbreviate') ? Object.keys(currencies) : Object.values(currencies);
    } catch (error) {
        // Log any errors that occur during the API request
        console.error(error);
    }
}

// Function to filter the currency list based on user input
function filterList(str) {
    return CURRENCY_LIST.filter(
        element => element.toLowerCase().includes(str.toLowerCase())
    );
}

// Function to render a list in a dropdown element
function renderListInDropdown(listJSON, ulElement) {
    ulElement.innerHTML = listJSON.map(
        item => `<li>${item}</li>`
    ).join('');
}

// Function to handle selecting an option from the dropdown
function useRenderedOption(event) {
    const ul = event.target.parentElement;
    
    // Update the selected input field with the chosen currency
    if (ul.id.includes('first')) {
        convertFrom.value = event.target.innerText;
    } else {
        convertTo.value = event.target.innerText;
    }

    // Clear the dropdown list
    ul.innerHTML = '';
}

// Function to prevent Enter key from triggering form submission
function noEnter() {
    return !(window.event && window.event.keyCode === 13);
}

// Function to handle user input for searching currencies
function searchHandler(event) {
    const input = event.target.value;
    const $ul = event.target.id.includes('from') ? $('ul').eq(0) : $('ul').eq(1);
    $ul.html('');

    // Display filtered list in the dropdown based on user input
    if (input !== '') {
        $ul.addClass('active');
        const filteredSearch = filterList(input);
        renderListInDropdown(filteredSearch, $ul[0]);
    } else {
        $ul.removeClass('active');
    }
}

// Function to check if a string contains uppercase letters
function containsUppercase(str) {
    return /^[A-Z]+$/.test(str);
}

// Function to get the currency conversion rate for a given currency
function getQuoteForCurrency(currency) {
    let currencyKey;

    // Handle special case for USD (United States Dollar)
    if (currency === 'United States Dollar' || currency === 'USD') {
        return 1;
    } else {
        // Determine the currency key for the given input
        if (containsUppercase(currency)) {
            currencyKey = Object.keys(QUOTES).find(key => key.includes(currency));
        } else {
            let currencyIdx = CURRENCY_LIST.indexOf(currency);
            currencyKey = Object.keys(QUOTES)[currencyIdx];
        }
    }

    // Return the conversion rate for the given currency
    return QUOTES[currencyKey];
}

// Function to send user input to the server for rate calculation
async function sendDataToServer() {
    const firstInput = getQuoteForCurrency(convertFrom.value);
    const secondInput = getQuoteForCurrency(convertTo.value);
    const amountInput = document.getElementById('input-amount').value;

    // Make a POST request to the server with user input
    fetch('/calculate_rate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            firstInput: firstInput,
            secondInput: secondInput,
            amountInput: amountInput
        })
    })
    .then(response => {
        // Check if the server response is OK
        if (response.ok) {
            return response.json();
        } else {
            // Throw an error for non-OK responses
            throw new Error('Server response was not OK.');
        }
    })
    .then(data => {
        // Log the server response data
        console.log(data);
    })
    .catch(error => {
        // Log any errors that occur during the process
        console.error('Error:', error);
    });
}

// Initialization function to set up event listeners and fetch initial data
function init() {
    fetchCurrencyData();
    fetchCurrencyList();

    // Add event listeners to handle user interactions
    convertFrom.addEventListener('keyup', searchHandler);
    convertTo.addEventListener('keyup', searchHandler);
    firstDropdown.addEventListener('click', useRenderedOption);
    secondDropdown.addEventListener('click', useRenderedOption);
    submit.addEventListener('click', sendDataToServer);
}

// Event listener for when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', init);
document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.display = 'none'; // Hide flash messages after 5 seconds
        }, 5000);
    });
});
