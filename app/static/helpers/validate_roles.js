function validate_roles(e) {
    let adminCheckbox = document.getElementById("rol_administrador")
    let operatorCheckbox = document.getElementById("rol_operador")

    if (!adminCheckbox.checked && !operatorCheckbox.checked) { 
        e.preventDefault()
        parragraph = document.createElement("p")
        parragraph.innerHTML = "Seleccione al menos un rol"
        parragraph.className += "text-danger"
        rol_label.replaceWith(parragraph)
    }
}