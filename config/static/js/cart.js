document.addEventListener('DOMContentLoaded', function() {
    let tg = window.Telegram.WebApp;
    const orderButton = document.getElementById('checkout-btn');
    let deletedProducts = [];
    tg.expand();

    const emptyCartMessage = document.getElementById('empty-cart-message');
    const emptyCartTotal = document.getElementById('total');
    const emptyCartCheckoutBtn = document.getElementById('checkout-btn');

    function checkCartIsEmpty() {
        const orderItems = document.querySelectorAll('.order-item');
        if (orderItems.length === 0) {
            emptyCartMessage.style.display = 'block';
            emptyCartTotal.style.display = 'none';
            emptyCartCheckoutBtn.style.display = 'none';
        } else {
            emptyCartMessage.style.display = 'none';
            emptyCartTotal.style.display = 'block';
            emptyCartCheckoutBtn.style.display = 'block';
        }
    }

    function populateCartFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        const productsParam = urlParams.get('product');

        if (productsParam) {
            const decodedProductsParam = decodeURIComponent(productsParam);
            const products = JSON.parse(decodedProductsParam);

            const orderList = document.querySelector('.order-list');
            let totalPrice = 0;

            products.forEach(function(product, index) {
                const listItem = document.createElement('li');
                listItem.classList.add('order-item');

                const itemDetails = document.createElement('div');
                itemDetails.classList.add('item-details');

                const productName = document.createElement('h2');
                productName.textContent = product.name;

                const productDescription = document.createElement('p');
                productDescription.textContent = product.description;

                const productPrice = document.createElement('p');
                productPrice.textContent = `Цена: $${product.price}`;

                const productImage = document.createElement('img');
                productImage.src = product.image; // Путь к изображению товара
                productImage.alt = product.name; // Альтернативный текст для изображения

                const quantityInput = document.createElement('div');
                quantityInput.classList.add('quantity-input-container');

                const minusButton = document.createElement('button');
                minusButton.classList.add('quantity-btn');
                minusButton.textContent = '-';
                minusButton.addEventListener('click', function() {
                    event.preventDefault();
                    const input = quantityInput.querySelector('input');
                    input.value = Math.max(parseInt(input.value) - 1, 1);
                    calculateTotalPrice();
                });

                const quantityInputField = document.createElement('input');
                quantityInputField.setAttribute('type', 'number');
                quantityInputField.classList.add('quantity-input');
                quantityInputField.setAttribute('value', '1');
                quantityInputField.setAttribute('min', '1');

                const plusButton = document.createElement('button');
                plusButton.classList.add('quantity-btn');
                plusButton.textContent = '+';
                plusButton.addEventListener('click', function() {
                    event.preventDefault();
                    const input = quantityInput.querySelector('input');
                    input.value = parseInt(input.value) + 1;
                    calculateTotalPrice();
                });

                quantityInput.appendChild(minusButton);
                quantityInput.appendChild(quantityInputField);
                quantityInput.appendChild(plusButton);

                const itemActions = document.createElement('div');
                itemActions.classList.add('item-actions');

                const removeButton = document.createElement('button');
                removeButton.classList.add('remove-btn');
                removeButton.textContent = 'Удалить';

                itemDetails.appendChild(productImage); // Добавляем изображение в элемент товара
                itemDetails.appendChild(productName);
                itemDetails.appendChild(productDescription);
                itemDetails.appendChild(productPrice);
                itemDetails.appendChild(quantityInput);
                listItem.appendChild(itemDetails);
                itemActions.appendChild(removeButton);
                listItem.appendChild(itemActions);
                orderList.appendChild(listItem);

                totalPrice += product.price;
            });

            const totalPriceElement = document.getElementById('total-price');
            totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
            checkCartIsEmpty();

            // Добавляем обработчики событий после добавления элементов корзины
            addRemoveButtonEventListeners();
            addQuantityInputEventListeners();
        }
    }


    function addRemoveButtonEventListeners() {
        const removeButtons = document.querySelectorAll('.remove-btn');
        removeButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const listItem = this.closest('.order-item');
                const productName = listItem.querySelector('h2').textContent;
                deletedProducts.push(productName);
                listItem.remove();
                calculateTotalPrice();
                checkCartIsEmpty();
            });
        });
    }

    function addQuantityInputEventListeners() {
        const quantityInputs = document.querySelectorAll('.quantity-input');
        quantityInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                calculateTotalPrice();
            });
        });
    }

    function calculateTotalPrice() {
        let totalPrice = 0;
        const orderItems = document.querySelectorAll('.order-item');

        orderItems.forEach(function(item) {
            const priceElement = item.querySelector('p:nth-of-type(2)');
            const price = parseFloat(priceElement.textContent.split('$')[1]);

            const quantityInput = item.querySelector('.quantity-input');
            const quantity = parseInt(quantityInput.value);

            totalPrice += price * quantity;
        });

        const totalPriceElement = document.getElementById('total-price');
        totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
    }




    function sendOrderData() {
        let data = {}; // Объект для хранения данных о заказе

        // Добавляем информацию о удаленных товарах, если она есть
        if (deletedProducts.length > 0) {
            data.deletedProducts = deletedProducts;
        }

        // Добавляем информацию о товарах в корзине и общей стоимости заказа
        const orderItems = document.querySelectorAll('.order-item');
        orderItems.forEach(function(item, index) {
            const productName = item.querySelector('h2').textContent;
            const priceElement = item.querySelector('p:nth-of-type(2)').textContent;
            const price = parseFloat(priceElement.split('$')[1]);
            const quantityInput = item.querySelector('.quantity-input');
            const quantity = parseInt(quantityInput.value);

            data[`product${index + 1}`] = {
                name: productName,
                price: price,
                quantity: quantity
            };
        });

        // Добавляем информацию об общей стоимости заказа
        const totalPriceElement = document.getElementById('total-price');
        const totalPrice = parseFloat(totalPriceElement.textContent.split('$')[1]);
        data.total_price = totalPrice;

        // Отправляем данные на сервер
//        console.log(data);
//        event.preventDefault();
    tg.sendData(JSON.stringify(data));
    tg.close();
}

checkCartIsEmpty();
populateCartFromUrl();
orderButton.addEventListener('click', sendOrderData);
});