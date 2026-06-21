document.addEventListener('DOMContentLoaded', function () {
    const nombre = document.getElementById('id_nombre');
    const numericFields = ['id_cantidad_MD', 'id_stock', 'id_precio_unitario'];

    if (nombre) {
        nombre.addEventListener('input', function () {
            this.value = this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]/g, '');
        });
        nombre.addEventListener('keypress', function (event) {
            if (!/[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]/.test(event.key)) {
                event.preventDefault();
            }
        });
    }

    numericFields.forEach(function (fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.addEventListener('input', function () {
            this.value = this.value.replace(/[^\d]/g, '');
        });

        field.addEventListener('keypress', function (event) {
            if (!/\d/.test(event.key)) {
                event.preventDefault();
            }
        });
    });
});
