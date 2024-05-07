document.addEventListener('DOMContentLoaded', function() {
    let tg = window.Telegram.WebApp;
    let search = document.getElementById("search");
    tg.expand();
    // Получаем параметры запроса URL
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    // Получаем ссылку на элемент <select> для категорий
    const categorySelect = document.getElementById('category');
    // Получаем ссылку на элемент <select> для сортов
    const sortSelect = document.getElementById('sort');
    const labelSort = document.getElementById('label-sort');

    // Получаем параметры сортов из URL
    const sortParams = urlParams.get('product');
    const decodedSortParams = decodeURIComponent(sortParams);
    const productData = JSON.parse(decodedSortParams);

    // Заполняем список опций для элемента <select> с id="category"
    for (const category in productData) {
        if (productData.hasOwnProperty(category)) {
            const optionElement = document.createElement('option');
            optionElement.value = category;
            optionElement.textContent = category;
            categorySelect.appendChild(optionElement);
        }
    }

    // Скрыть поле выбора сорта при загрузке страницы
    sortSelect.style.display = 'none';
    labelSort.style.display = 'none';
    // Добавить слушатель события изменения значения в поле категории
    categorySelect.addEventListener('change', function() {
        const selectedCategory = this.value;
        const selectedCategorySorts = productData[selectedCategory];

        // Если для выбранной категории есть сорта, то отобразить поле выбора сорта
        // и заполнить его значениями, соответствующими выбранной категории
        if (selectedCategorySorts.length > 0) {
            // Очистить поле выбора сорта
            sortSelect.innerHTML = '<option value="">--Выберите сорт--</option>';
            labelSort.style.display = 'block';
            // Заполнить поле выбора сорта значениями
            selectedCategorySorts.forEach(sort => {
                const optionElement = document.createElement('option');
                optionElement.value = sort;
                optionElement.textContent = sort;
                sortSelect.appendChild(optionElement);
            });
            // Показать поле выбора сорта
            sortSelect.style.display = 'block';
            labelSort.style.display = 'block';

        } else {
            // Если для выбранной категории нет сортов, то скрыть поле выбора сорта
            sortSelect.style.display = 'none';
            labelSort.style.display = 'none';

        }
    });

    search.addEventListener("click", () => {
        var sortValue = document.getElementById("sort").value;
        var categoryValue = document.getElementById("category").value;

        var data = {
            sort: sortValue,
            category: categoryValue,
        };
        //console.log(data);
        //event.preventDefault();


        tg.sendData(JSON.stringify(data));
        tg.close();
    });
});
