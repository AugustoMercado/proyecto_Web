
/**
 * Displays a toast notification with the given message.
 */
function showToast(message) {
    const toastBox = document.getElementById('toast-box');
    const toastMessage = document.getElementById('toast-message');
    
    if (toastMessage) toastMessage.innerText = message;
    
    if (toastBox) {
        toastBox.classList.remove('toast-hidden');
        toastBox.classList.add('toast-visible');
        setTimeout(() => {
            toastBox.classList.remove('toast-visible');
            toastBox.classList.add('toast-hidden');
        }, 3000);
    }
}


/**
 * Updates quantity input for a product.
 */
function changeValue(productId, change) {
    const input = document.getElementById(`quantity-${productId}`);
    if (!input) return;
    
    let currentValue = parseInt(input.value) || 0;
    const maxValue = parseInt(input.getAttribute('max'));
    const newValue = currentValue + change;
    
    if (newValue >= 1 && newValue <= maxValue) {
        input.value = newValue;
    }
}

/**
 * Handles add to cart request with validation.
 */
function processAddToCart(productId, isKiloStr) {
    const input = document.getElementById(`quantity-${productId}`);
    const quantity = input ? parseInt(input.value) : 1;
    
    const isKilo = (isKiloStr === 'True' || isKiloStr === 'true');
    if (isKilo && quantity < 50) {
        showToast("⚠️ El mínimo son 50 gramos.");
        return;
    }
    
    const url = `/cart/add/${productId}/?cantidad=${quantity}`;

    fetch(url)
        .then(response => response.json())
        .then(data => handleAddToCartResponse(data))
        .catch(error => {
            console.error('Error:', error);
            showToast("❌ Error de conexión");
        });
}

/**
 * Processes add to cart response and shows appropriate toast.
 */
function handleAddToCartResponse(data) {
    const toastBox = document.getElementById('toast-box');
    
    if (data.status === 'ok') {
        toastBox.style.backgroundColor = "var(--color-success)";
        showToast("✅ " + data.message);
    } else if (data.status === 'login_required') {
        toastBox.style.backgroundColor = "var(--color-danger)";
        showToast("🔒 " + data.message);
        setTimeout(() => {
            window.location.href = "/login/";
        }, 2000);
    } else {
        toastBox.style.backgroundColor = "var(--color-danger)";
        showToast("❌ " + (data.message || "Ocurrió un error"));
    }
}


/**
 * Updates cart item quantity or removes it.
 */
function updateQty(productId, action, deleteUrl) {
    const url = `/cart/update_item/${productId}/${action}/`;
    
    if (action === 'subtract') {
        const qtySpan = document.getElementById(`qty-${productId}`);
        if (qtySpan && parseInt(qtySpan.innerText) <= 1) {
            askDelete(deleteUrl);
            return;
        }
    }

    fetch(url)
        .then(response => response.json())
        .then(data => updateCartDisplay(data, productId))
        .catch(error => console.error('Error:', error));
}

/**
 * Updates cart display after quantity change.
 */
function updateCartDisplay(data, productId) {
    const totalSpan = document.getElementById('total-carrito');
    if (totalSpan) totalSpan.innerText = data.total;
    
    if (data.quantity === 0) {
        const card = document.getElementById(`producto-${productId}`);
        if (card) card.remove();
    } else {
        const qtySpan = document.getElementById(`qty-${productId}`);
        if (qtySpan) qtySpan.innerText = data.quantity;
    }
}


/**
 * Shows confirmation modal for item deletion.
 */
function askDelete(url) {
    const modal = document.getElementById('modalBorrar');
    if (!modal) return;
    
    modal.querySelector('h3').innerText = "¿Estás seguro?";
    modal.querySelector('p').innerText = "Vas a eliminar este producto.";
    
    const btn = document.getElementById('btnConfirmar');
    btn.innerText = "Sí, eliminar";
    btn.style.backgroundColor = "#e74c3c";
    btn.onclick = null;
    btn.href = url;
    
    modal.style.display = 'flex';
}

/**
 * Shows confirmation modal for clearing entire cart.
 */
function askCancelCart(url) {
    const modal = document.getElementById('modalBorrar');
    if (!modal) return;
    
    modal.querySelector('h3').innerText = "¿Vaciar Carrito?";
    modal.querySelector('p').innerText = "Se perderán todos los productos seleccionados.";
    document.getElementById('btnConfirmar').href = url;
    
    modal.style.display = 'flex';
}

/**
 * Closes the modal dialog.
 */
function closeModal() {
    const modal = document.getElementById('modalBorrar');
    if (modal) modal.style.display = 'none';
}

/**
 * Shows success modal and redirects to destination.
 */
function payTotal(destinationUrl) {
    const modal = document.getElementById('modalExito');
    if (!modal) return;
    
    modal.style.display = 'flex';
    setTimeout(() => {
        window.location.href = destinationUrl;
    }, 2000);
}

/**
 * Shows confirmation modal for order completion.
 */
function askConfirmOrder(url) {
    const modal = document.getElementById('modalBorrar');
    if (!modal) return;
    
    modal.querySelector('h3').innerText = "¿Confirmar Pedido?";
    modal.querySelector('p').innerText = "Estás a un paso de finalizar tu compra.";
    
    const btn = document.getElementById('btnConfirmar');
    btn.innerText = "Sí, Comprar";
    btn.style.backgroundColor = "#E67E22";
    btn.removeAttribute('href');
    btn.onclick = () => {
        closeModal();
        payTotal(url);
    };
    
    modal.style.display = 'flex';
}