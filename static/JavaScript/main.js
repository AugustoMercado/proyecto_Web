
function showToast(mensaje) {
    const toast = document.getElementById('toast-box');
    const texto = document.getElementById('toast-message');
    if (texto) texto.innerText = mensaje;
    
    if (toast) {
        toast.classList.remove('toast-hidden');
        toast.classList.add('toast-visible');
        setTimeout(() => {
            toast.classList.remove('toast-visible');
            toast.classList.add('toast-hidden');
        }, 3000);
    }
}


function changeValue(productId, change) {
    const input = document.getElementById(`quantity-${productId}`);
    if (input) {
        let currentValue = parseInt(input.value) || 0;
        let max = parseInt(input.getAttribute('max'));
        let newValue = currentValue + change;
        
        if (newValue >= 1 && newValue <= max) {
            input.value = newValue;
        }
    }
}

function processAddToCart(productId, isKiloStr) {
    const input = document.getElementById(`quantity-${productId}`);
    const quantity = input ? parseInt(input.value) : 1;
    
    const isKilo = (isKiloStr === 'True' || isKiloStr === 'true');
    if (isKilo && quantity < 50) {
        // Usamos el Toast también para validaciones locales
        showToast("⚠️ El mínimo son 50 gramos."); 
        return;
    }
    
    const url = `/cart/add/${productId}/?cantidad=${quantity}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                // CASO 1: ÉXITO (Verde)
                // Cambiamos el fondo a verde (si tenés una clase para eso) o usamos el default
                const toast = document.getElementById('toast-box');
                toast.style.backgroundColor = "var(--color-success)"; // Verde
                showToast("✅ " + data.message);
                
            } else if (data.status === 'login_required') {
                // CASO 2: FALTA LOGIN (Naranja/Rojo)
                const toast = document.getElementById('toast-box');
                toast.style.backgroundColor = "var(--color-danger)"; // Rojo/Naranja para alerta
                showToast("🔒 " + data.message);
                
                // Esperamos 2 segundos para que lea el cartel y luego redirigimos
                setTimeout(() => {
                    window.location.href = "/login/"; 
                }, 2000);

            } else {
                // CASO 3: ERROR GENERICO (Rojo)
                const toast = document.getElementById('toast-box');
                toast.style.backgroundColor = "var(--color-danger)";
                showToast("❌ " + (data.message || "Ocurrió un error"));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast("❌ Error de conexión");
        });
}


function updateQty(productId, action, urlBorrado) {
    var url = '/cart/update_item/' + productId + '/' + action + '/';
    
    // VALIDACIÓN EN INGLÉS ('subtract')
    if (action === 'subtract') { 
        var qtySpan = document.getElementById('qty-' + productId);
        // Si es 1 y tocan subtract, preguntamos si quiere borrar
        if (qtySpan && parseInt(qtySpan.innerText) <= 1) {
            ask_delete(urlBorrado); 
            return; 
        }
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {
        var totalSpan = document.getElementById('total-carrito');
        if (totalSpan) totalSpan.innerText = data.total;
        
        // RESPUESTA EN INGLÉS (.quantity)
        if (data.quantity === 0) {
            var tarjeta = document.getElementById('producto-' + productId);
            if (tarjeta) tarjeta.remove();
        } else {
            var qtySpan = document.getElementById('qty-' + productId);
            if (qtySpan) qtySpan.innerText = data.quantity; // <--- data.quantity
        }
    })
    .catch(error => console.error('Error:', error));
}


function ask_delete(url) {
    const modal = document.getElementById('modalBorrar');
    if(modal) {
        modal.querySelector('h3').innerText = "¿Estás seguro?";
        modal.querySelector('p').innerText = "Vas a eliminar este producto.";
        
        const btn = document.getElementById('btnConfirmar');
        btn.innerText = "Sí, eliminar";       // TEXTO DE BORRADO
        btn.style.backgroundColor = "#e74c3c"; // ROJO (Peligro)
        
        // Comportamiento normal de link
        btn.onclick = null; 
        btn.href = url;
        
        modal.style.display = 'flex';
    }
}

function ask_cancel_cart(url) {
    const modal = document.getElementById('modalBorrar');
    if(modal) {
        modal.querySelector('h3').innerText = "¿Vaciar Carrito?";
        modal.querySelector('p').innerText = "Se perderán todos los productos seleccionados.";
        document.getElementById('btnConfirmar').href = url;
        modal.style.display = 'flex';
    }
}

function Closemodal() {
    const modal = document.getElementById('modalBorrar');
    if(modal) modal.style.display = 'none';
}

function pagarTotal(urlDestino) {
    const modal = document.getElementById('modalExito');
    if(modal) {
        modal.style.display = 'flex';
        setTimeout(function() {
            window.location.href = urlDestino;
        }, 2000);
    }
}

function ask_confirm_order(url) {
    const modal = document.getElementById('modalBorrar');
    if(modal) {
        modal.querySelector('h3').innerText = "¿Confirmar Pedido?";
        modal.querySelector('p').innerText = "Estás a un paso de finalizar tu compra.";
        
        const btn = document.getElementById('btnConfirmar');
        btn.innerText = "Sí, Comprar";
        
        // --- CAMBIO DE COLOR AQUÍ ---
        btn.style.backgroundColor = "#E67E22"; // TU NARANJA DE MARCA (Mucho mejor)
        // Si preferís el Azul de la marca usa: "#4C64B9"
        
        btn.removeAttribute('href'); 
        
        btn.onclick = function() { 
            Closemodal();     
            pagarTotal(url);  
        };
        
        modal.style.display = 'flex';
    }
}