/* --- main.js COMPLETO --- */

/* ==============================================
   1. UTILIDADES Y TOASTS
   ============================================== */
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

/* ==============================================
   2. LÓGICA DE PRODUCTO (VISTA DE DETALLES)
   ============================================== */

// Botones +/- en la ficha del producto (antes de agregar)
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

// Función principal para AGREGAR al carrito
function processAddToCart(productId, isKiloStr) {
    const input = document.getElementById(`quantity-${productId}`);
    const quantity = input ? parseInt(input.value) : 1;
    
    // Validar Fiambre (mínimo 50g)
    const isKilo = (isKiloStr === 'True' || isKiloStr === 'true');
    if (isKilo && quantity < 50) {
        alert("El mínimo para pesar son 50 gramos.");
        return;
    }
    
    // URL correcta
    const url = `/cart/add/${productId}/?cantidad=${quantity}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                showToast("✅ " + (data.message || "Agregado"));
            } else if (data.status === 'login_required') {
                window.location.href = "/LoginAccount/"; 
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}

/* ==============================================
   3. LÓGICA DEL CARRITO (LO QUE FALTABA) 🛒
   ============================================== */

// Actualizar cantidad desde el Carrito (+ / -)
function updateQty(productId, action, urlBorrado) {
    var url = '/cart/update_item/' + productId + '/' + action + '/';
    
    // Si la acción es restar y queda 1, preguntamos si quiere borrar
    if (action === 'restar') {
        var qtySpan = document.getElementById('qty-' + productId);
        // Nota: Si usas span, asegurate de leer innerText. Si es input, value.
        // Asumiendo que usas span según tu HTML anterior:
        if (qtySpan && parseInt(qtySpan.innerText) <= 1) {
            ask_delete(urlBorrado); 
            return; 
        }
    }

    fetch(url)
    .then(response => response.json())
    .then(data => {
        // Actualizamos el total general
        var totalSpan = document.getElementById('total-carrito');
        if (totalSpan) totalSpan.innerText = data.total;
        
        if (data.cantidad === 0) {
            // Si llega a 0, quitamos la tarjeta
            var tarjeta = document.getElementById('producto-' + productId);
            if (tarjeta) tarjeta.remove();
        } else {
            // Si no, actualizamos el numerito
            var qtySpan = document.getElementById('qty-' + productId);
            if (qtySpan) qtySpan.innerText = data.cantidad;
        }
    })
    .catch(error => console.error('Error:', error));
}

// Modales de Confirmación
function ask_delete(url) {
    const modal = document.getElementById('modalBorrar');
    if(modal) {
        modal.querySelector('h3').innerText = "¿Estás seguro?";
        modal.querySelector('p').innerText = "Vas a eliminar este producto.";
        document.getElementById('btnConfirmar').href = url;
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