let tg = window.Telegram.WebApp;
tg.expand();

let btn1 = document.getElementById("item-1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5");
let btn6 = document.getElementById("btn6");

btn1.addEventListener("click", function(){
    document.getElementById("inner").style.display = "none";
    document.getElementById("inner-2").style.display = "block";

});


 function fetchData() {
    // Создаем объект XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Настраиваем запрос
    xhr.open('GET', '/api/profile/', true); // Указываем URL эндпоинта API

    // Устанавливаем обработчик события загрузки
    xhr.onload = function () {
        // Проверяем успешность запроса
        if (xhr.status >= 200 && xhr.status < 300) {
            // Парсим JSON-ответ
            var data = JSON.parse(xhr.responseText);
            // Обновляем содержимое элемента с id "result" данными из ответа
            document.getElementById('result').innerHTML = '<p>' + data.phone + '</p>';
        } else {
            // Выводим сообщение об ошибке, если запрос неуспешен
            console.error('Request failed with status:', xhr.status);
        }
    };

    // Устанавливаем обработчик события ошибки
    xhr.onerror = function () {
        console.error('Request failed');
    };

    // Отправляем запрос
    xhr.send();
}

// Вызываем функцию при загрузке страницы
window.onload = fetchData;