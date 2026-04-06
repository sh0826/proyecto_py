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

    // --- ELIMINAR BOTÓN DE EXPORTAR REBELDE ---
    function removeExportButtons() {
        // Opción 1: Por selectores conocidos
        const selectors = '.export_link, .import_link, [name="_export"], .btn-secondary.export_link';
        document.querySelectorAll(selectors).forEach(el => el.remove());

        // Opción 2: Por contenido de texto (el más infalible para "Exportar")
        document.querySelectorAll('.btn, a, button').forEach(el => {
            const text = el.textContent.trim().toLowerCase();
            if (text === 'exportar' || text === 'export') {
                // Si está dentro de un <li> (herramientas de objeto), eliminamos el <li>
                if (el.parentElement.tagName === 'LI') {
                    el.parentElement.remove();
                } else {
                    el.remove();
                }
            }
        });
    }

    // Ejecutamos inmediatamente y tras un pequeño delay por si Jazzmin lo carga dinámicamente
    removeExportButtons();
    setTimeout(removeExportButtons, 100);
    setTimeout(removeExportButtons, 500);
});
