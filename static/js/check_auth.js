document.addEventListener("DOMContentLoaded", async function(event) {
    event.preventDefault();
    let tg = window.Telegram.WebApp;
    tg.expand();


    try {
            let telegram_id= tg.initDataUnsafe.user.id;
            let response = await fetch('http://127.0.0.1:8080/api/v1/users/' + telegram_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (response.ok) {
                let result = await response.json();
                tg.sendData(JSON.stringify(result));
                console.log(result);

            } else {
                window.location.href = 'http://localhost:63342/tg_rouse/static/templates/auth.html';
            }
        } catch (error) {
            window.location.href = 'http://localhost:63342/tg_rouse/static/templates/auth.html';
        }
});