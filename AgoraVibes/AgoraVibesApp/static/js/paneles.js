/**
 * paneles.js
 * Reordena el DOM del admin para colocar el buscador
 * debajo del panel de filtros en la vista de lista.
 */
document.addEventListener('DOMContentLoaded', function () {
    const search = document.getElementById('changelist-search');
    const filter = document.getElementById('changelist-filter');

    if (!search || !filter) return;

    // Mueve el buscador justo después del panel de filtros
    filter.parentNode.insertBefore(search, filter.nextSibling);

    // Pequeño estilo adicional para que el search quede integrado
    search.style.marginTop = '12px';

    // Agregamos botón de "Limpiar filtros" si hay filtros activos
    if (window.location.search && window.location.search.length > 1) {
        const h2 = filter.querySelector('h2');
        if (h2) {
            h2.style.display = 'flex';
            h2.style.justifyContent = 'space-between';
            h2.style.alignItems = 'center';

            const clearBtn = document.createElement('a');
            clearBtn.href = window.location.pathname; // URL limpia sin parámetros
            clearBtn.innerHTML = '<i class="fas fa-times-circle"></i>';
            clearBtn.title = 'Limpiar todos los filtros y búsqueda';
            clearBtn.className = 'clear-filters-btn';
            h2.appendChild(clearBtn);
        }
    }
});
