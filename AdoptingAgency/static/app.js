$('#go-meet').click(goMeet)

async function goMeet() {
    const id = $(this).data('id')
    await axios.get(`/pets/${id}`)
}
