/* Stock management automation for product admin form. */

document.addEventListener('DOMContentLoaded', function () {
    const isKiloCheckbox = document.getElementById('id_is_kilo');
    const stockInput = document.getElementById('id_stock');

    if (!isKiloCheckbox || !stockInput) {
        console.error('❌ ERROR: Missing required form elements (id_is_kilo or id_stock)');
        return;
    }

    console.log('✅ Stock automation script loaded');

    /**
     * Manages stock value based on product type.
     * Sets stock to 9999 for kilo-based products, clears for regular products.
     */
    function updateStockValue() {
        const defaultKiloStock = '9999';
        
        if (isKiloCheckbox.checked) {
            if (stockInput.value === '') {
                stockInput.value = defaultKiloStock;
            }
        } else {
            if (stockInput.value === defaultKiloStock) {
                stockInput.value = '';
            }
        }
    }

    updateStockValue();
    isKiloCheckbox.addEventListener('change', updateStockValue);
});