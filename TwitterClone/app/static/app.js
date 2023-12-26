const logIn = document.querySelector("#log-in")
const register = document.querySelector("#register")
const myModal = document.getElementById('myModal')

logIn.addEventListener('click', event => {
    console.log(event.target.id)
})

register.addEventListener('click', event => {
    console.log(event.target.id)
})

myModal.addEventListener('shown.bs.modal',() => {
    myInput.focus()
})