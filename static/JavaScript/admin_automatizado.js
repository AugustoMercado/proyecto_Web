/* static/js/admin_stock.js */

document.addEventListener('DOMContentLoaded', function() {
    // Buscamos los elementos
    const checkPeso = document.getElementById('id_is_kilo');
    const inputStock = document.getElementById('id_stock');

    if (checkPeso && inputStock) {
        console.log("✅ Script de Stock: ON");

        // Definimos la función que rellena
        function rellenarSiEsNecesario() {
            if (checkPeso.checked) {
                // Si está marcado y el stock está vacío, poner 9999
                if (inputStock.value === "") {
                    inputStock.value = "9999";
                }
            } else {
                // Si desmarcás y dice 9999, limpiar.
                if (inputStock.value === "9999") {
                    inputStock.value = "";
                }
            }
        }

        // 1. Ejecutar AHORA (Apenas carga la página)
        // Esto arregla tu problema actual: va a ver el tilde y poner 9999 solo.
        rellenarSiEsNecesario();

        // 2. Ejecutar cuando hagas CLICK
        checkPeso.addEventListener('change', rellenarSiEsNecesario);

    } else {
        console.error("❌ ERROR: No encuentro id_is_kilo o id_stock");
    }
});