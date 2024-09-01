document.addEventListener('DOMContentLoaded', () => { //Permite que todo el archivo se pueda ejecutar despues del archivo base
    const form = document.querySelector('form'); //selecciona el primer elemto del formulario y lo almacena en la variable form
    
    form.addEventListener('submit', (event) => { //si el cliente desea enviar el formulario este se ejecuta con tal y todo este bien diligenciado
        const selects = form.querySelectorAll('select[required]');
        let valid = true; // verifica si todos los campos son validos

        selects.forEach((select) => { //inicializa un bucle
            if (select.value === '') { //verifica las casillas
                valid = false;
                alert(`Por favor, seleccione una respuesta para ${select.previousElementSibling.textContent.trim()}`);
            }
        });

        if (!valid) {
            event.preventDefault(); // Evita el envío del formulario si alguna selección es inválida
        }
    });
});

