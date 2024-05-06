let tg = window.Telegram.WebApp;
let search = document.getElementById("search");
tg.expand();
// Получаем параметры запроса URL
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

// Получаем ссылки на элементы <select>
const sortSelect = document.getElementById('sort');
const categorySelect = document.getElementById('category');
const colorSelect = document.getElementById('color');

// Заполняем список опций для элемента <select> с id="sort"
const sortOptions = urlParams.getAll('sort');
sortOptions.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option;
    sortSelect.appendChild(optionElement);
});

// Заполняем список опций для элемента <select> с id="category"
const categoryOptions = urlParams.getAll('category');
categoryOptions.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option;
    categorySelect.appendChild(optionElement);
});
const colorOptions = urlParams.getAll('color');
colorOptions.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option;
    colorSelect.appendChild(optionElement);
});


 search.addEventListener("click", () => {
    var sortValue = document.getElementById("sort").value;
    var categoryValue = document.getElementById("category").value;
    var colorValue = document.getElementById("color").value;

    var data = {
        sort: sortValue,
        category: categoryValue,
        color: colorValue
    };
<!--            console.log(data);-->
<!--            event.preventDefault();-->


    tg.sendData(JSON.stringify(data));
    tg.close();
 });