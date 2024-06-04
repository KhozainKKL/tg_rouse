

document.addEventListener("DOMContentLoaded", async function(event) {
    event.preventDefault();
    var tg = window.Telegram.WebApp;
    tg.expand();
    var post_in_html_telegram_id = tg.initDataUnsafe.user.id;
    function func_one() {
        try {
            let telegram_id = tg.initDataUnsafe.user.id;
            let response = await fetch('http://127.0.0.1:8080/api/v1/users/' + telegram_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (response.ok) {
                let result = await response.json();
                tg.sendData(JSON.stringify(result));
                event.preventDefault();
                window.location.href = 'https://khozainkkl.github.io/tg_rouse.github.io/static/templates/index.html';
            } else {
                window.location.href = 'https://khozainkkl.github.io/tg_rouse.github.io/static/templates/auth.html';
            }
        } catch (error) {
            window.location.href = 'https://khozainkkl.github.io/tg_rouse.github.io/static/templates/auth.html';
        }
        func_one = () => {};
    }

    func_one();

    function get_cart() {
        let telegram_id = tg.initDataUnsafe.user.id;
            let response = await fetch('http://127.0.0.1:8080/api/v1/cart/' + telegram_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (response.ok) {
                let result = await response.json();
                tg.sendData(JSON.stringify(result));
                event.preventDefault();
                window.location.href = 'https://khozainkkl.github.io/tg_rouse.github.io/static/templates/index.html';
            }
    }
});