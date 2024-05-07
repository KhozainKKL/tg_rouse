let tg = window.Telegram.WebApp;
let search = document.getElementById("search");
tg.expand();
// Получаем параметры запроса URL
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

// Получаем ссылки на элементы <select>
const sortParams = urlParams.get('sort');
const decodedSortParams = decodeURIComponent(sortParams);
const sortOptions = JSON.parse(decodedSortParams);

const categoryParams = urlParams.get('category');
const decodedCategoryParams = decodeURIComponent(categoryParams);
const categoryOptions = JSON.parse(decodedCategoryParams);

// Заполняем список опций для элемента <select> с id="sort"
sortOptions.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option;
    sortSelect.appendChild(optionElement);
});

// Заполняем список опций для элемента <select> с id="category"
categoryOptions.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option;
    categorySelect.appendChild(optionElement);
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
//console.log(data);
//event.preventDefault();


    tg.sendData(JSON.stringify(data));
    tg.close();
 });