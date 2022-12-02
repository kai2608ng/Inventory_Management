const MaterialCategory = document.getElementsByClassName("form-sub-container")[0].cloneNode(true)

function addMaterial(){
    const materialMainCategory = document.getElementsByClassName("form-material-main-container")[0]
    const newMaterialCategory = MaterialCategory.cloneNode(true)
    materialMainCategory.appendChild(newMaterialCategory)
    
    const deleteMaterialButtons = document.getElementsByClassName("close")
    for(let i = 0; i < deleteMaterialButtons.length; i++)
        deleteMaterialButtons[i].addEventListener("click", deleteMaterial)
}

function deleteMaterial(){
    this.parentNode.parentNode.remove()
    console.log("click")
}

// Initialization
const addMaterialButton = document.getElementById("add-material")
const deleteMaterialButtons = document.getElementsByClassName("close")

addMaterialButton.addEventListener("click", addMaterial)
for(let i = 0; i < deleteMaterialButtons.length; i++)
    deleteMaterialButtons[i].addEventListener("click", deleteMaterial)



