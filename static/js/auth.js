$('.form').find('input, textarea').on('keyup blur focus', function (e) {

    var $this = $(this),
    label = $this.prev('label');

    if (e.type === 'keyup') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
        if( $this.val() === '' ) {
            label.removeClass('active highlight');
        } else {
            label.removeClass('highlight');
        }
    } else if (e.type === 'focus') {

        if( $this.val() === '' ) {
            label.removeClass('highlight');
        }
        else if( $this.val() !== '' ) {
            label.addClass('highlight');
        }
    }

});

$('.tab a').on('click', function (e) {

    e.preventDefault();

    $(this).parent().addClass('active');
    $(this).parent().siblings().removeClass('active');

    target = $(this).attr('href');

    $('.tab-content > div').not(target).hide();

    $(target).fadeIn(600);

});
document.addEventListener("DOMContentLoaded", function() {

    let tg = window.Telegram.WebApp;
    document.getElementById("demo").innerHTML = tg.initDataUnsafe.user.id;
    let register = document.getElementById("register");
    tg.expand();

    register.addEventListener("click", async (event) => {
        event.preventDefault();

        let fisrt_name = document.getElementById("first_name").value;
        let last_name = document.getElementById("last_name").value;
        let email = document.getElementById("email-register").value;
        let password = document.getElementById("password-register").value;

        let data = {
            email: email,
            password: password,
            is_active: true,
            is_superuser: false,
            is_verified: false,
            first_name: fisrt_name,
            last_name: last_name,
            telegram_id: tg.initDataUnsafe.user.id,
            phone: 0,
            geo: ""
        }
        console.log(data);
        event.preventDefault();

        try {
            let response = await fetch('http://127.0.0.1:8080/api/v1/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                let result = await response.json();
                tg.sendData(JSON.stringify(result));
                console.log(result);
                tg.close();
            } else {
                console.error('Ошибка регистрации:', response.statusText);
            }
        } catch (error) {
            console.error('Ошибка регистрации:', error);
        }
    });
});

