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

let tg = window.Telegram.WebApp;
let register = document.getElementById("register");
tg.expand();

register.addEventListener("click", () => {
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
      telegram_id: 11111,
      phone: 0,
      geo: "string"
    }


    tg.sendData(JSON.stringify(data));

    tg.close();
});
