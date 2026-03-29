document.addEventListener('DOMContentLoaded', function () {
    // Localizamos el contenedor del buscador en Jazzmin/DataTables
    const searchContainer = document.querySelector('#result_list_filter');
    
    if (searchContainer) {
        // Creamos el elemento de texto
        const infoText = document.createElement('small');
        infoText.innerText = 'Puedes buscar por: número de documento, nombre completo o correo.';
        
        // Estilo opcional para que se vea como una nota sutil
        infoText.style.display = 'block';
        infoText.style.color = '#666';
        infoText.style.marginTop = '5px';
        infoText.style.fontSize = '0.85rem';

        // Lo insertamos justo debajo del input
        searchContainer.appendChild(infoText);
    }
});