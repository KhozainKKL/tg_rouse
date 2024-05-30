document.getElementById("error").innerText = "";
let tg = window.Telegram.WebApp;
let order = document.getElementById("order");
let phoneInput = document.getElementById("user_phone");
tg.expand();

phoneInput.addEventListener("input", function() {
    let phoneNumber = phoneInput.value.replace(/\D/g, '');
    phoneNumber = phoneNumber.slice(0, 11);
    if (!phoneNumber.startsWith('8') && phoneNumber.length > 0) {
        phoneNumber = '8' + phoneNumber;
    }
    phoneNumber = phoneNumber.replace(/(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/, '$1$2$3$4$5');
    phoneInput.value = phoneNumber;
});

order.addEventListener("click", () => {
    let name = document.getElementById("user_name").value;
    let family = document.getElementById("user_family").value;
    let email = document.getElementById("user_email").value;
    let phone = phoneInput.value;
    let errorField = document.getElementById("error");

    if (name.length < 1) {
        errorField.innerText = 'Введите свое Имя';
        errorField.style.display = 'block'; // Показываем поле с ошибкой
        event.preventDefault(); // Предотвращаем отправку формы
        return;
    }
    if (family.length < 1) {
        errorField.innerText = 'Введите свою Фамилию';
        errorField.style.display = 'block'; // Показываем поле с ошибкой
        event.preventDefault(); // Предотвращаем отправку формы
        return;
    }
    if (phone.length < 11) {
        errorField.innerText = 'Ошибка в номере телефона';
        errorField.style.display = 'block'; // Показываем поле с ошибкой
        event.preventDefault(); // Предотвращаем отправку формы
        return;
    }

    let data = {
        name: name,
        family: family,
        email: email,
        phone: phone,
    }
    tg.sendData(JSON.stringify(data));

    tg.close();
});
