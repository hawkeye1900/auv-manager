const deleteForm = document.querySelector(".deleteForm")

function openModal(id){
    document.getElementById(`modal-${id}`).style.display = "block"
    console.log("Opening modal")
}

function closeModal(id){
    document.getElementById(`modal-${id}`).style.display = "None"
}

function confirmDelete(id) {
    if (id !== null) {
        const deleteForm = document.getElementById(`modal-${id}`)
        deleteForm.action = `/auvs/delete/${id}`
        deleteForm.method = "POST"
        closeModal(id)
    }
}