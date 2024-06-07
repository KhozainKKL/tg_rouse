document.addEventListener('DOMContentLoaded', async function() {
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

    // Измененная часть: функция для получения данных корзины пользователя
    async function getUserCart(telegramId) {
        let response = await fetch('http://127.0.0.1:8080/api/v1/cart/' + tg.initDataUnsafe.user.id, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (response.ok) {
            let cartData = await response.json();
            return cartData;
        } else {
            console.error('Error fetching cart data');
            return [];
        }
    }

    // Измененная часть: функция для заполнения корзины на основе данных API
    async function populateCart() {
        let telegramId = tg.initDataUnsafe.user.id;
        let cartData = await getUserCart(telegramId);

        if (cartData.length > 0) {
            const orderList = document.querySelector('.order-list');
            let totalPrice = 0;

            for (let item of cartData) {
                // Fetch product details (assuming you have an endpoint for product details)
                let productResponse = await fetch('http://127.0.0.1:8080/api/v1/products/' + item.product, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                });

                if (productResponse.ok) {
                    let product = await productResponse.json();
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
                    productImage.src = "https://khozainkkl.github.io/tg_rouse.github.io/config/media/" + product.image;
                    productImage.alt = product.name;

                    const quantityInput = document.createElement('div');
                    quantityInput.classList.add('quantity-input-container');

                    const minusButton = document.createElement('button');
                    minusButton.classList.add('quantity-btn');
                    minusButton.textContent = '-';
                    minusButton.addEventListener('click', function(event) {
                        event.preventDefault();
                        const input = quantityInput.querySelector('input');
                        input.value = Math.max(parseInt(input.value) - 1, 1);
                        calculateTotalPrice();
                    });

                    const quantityInputField = document.createElement('input');
                    quantityInputField.setAttribute('type', 'number');
                    quantityInputField.classList.add('quantity-input');
                    quantityInputField.setAttribute('value', item.quantity);
                    quantityInputField.setAttribute('min', '1');

                    const plusButton = document.createElement('button');
                    plusButton.classList.add('quantity-btn');
                    plusButton.textContent = '+';
                    plusButton.addEventListener('click', function(event) {
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

                    itemDetails.appendChild(productImage);
                    itemDetails.appendChild(productName);
                    itemDetails.appendChild(productDescription);
                    itemDetails.appendChild(productPrice);
                    itemDetails.appendChild(quantityInput);
                    listItem.appendChild(itemDetails);
                    itemActions.appendChild(removeButton);
                    listItem.appendChild(itemActions);
                    orderList.appendChild(listItem);

                    totalPrice += product.price * item.quantity;
                }
            }

            const totalPriceElement = document.getElementById('total-price');
            totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
            checkCartIsEmpty();

            // Добавляем обработчики событий после добавления элементов корзины
            addRemoveButtonEventListeners();
            addQuantityInputEventListeners();
        } else {
            checkCartIsEmpty();
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
        let data = {};

        if (deletedProducts.length > 0) {
            data.deletedProducts = deletedProducts;
        }

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

        const totalPriceElement = document.getElementById('total-price');
        const totalPrice = parseFloat(totalPriceElement.textContent.split('$')[1]);
        data.total_price = totalPrice;

        tg.sendData(JSON.stringify(data));
        tg.close();
    }

    checkCartIsEmpty();
    await populateCart();  // Измененная часть: вызов функции populateCart
    orderButton.addEventListener('click', sendOrderData);
});
