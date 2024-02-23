document.addEventListener("DOMContentLoaded", function () {
    const editableInput = document.getElementById("post-content");
    const counter = document.querySelector(".counter");
    const button = document.querySelector("#post-box-submit button");

    editableInput.addEventListener("input", function () {
        validated(editableInput);
    });

    function validated(element) {
        let text;
        let maxLength = 300;
        let currentLength = element.value.length;

        counter.innerText = maxLength - currentLength;

        if (currentLength > maxLength) {
            let overText = element.value.substr(maxLength); // extracting over texts
            overText = `<span class="highlight">${overText}</span>`; // creating new span and passing over texts
            text = element.value.substr(0, maxLength) + overText; // passing overText value in textTag variable
            counter.style.color = "#e0245e";
            button.classList.remove("active");
        } else {
            counter.style.color = "#333";
            button.classList.add("active");
        }
    }
});
