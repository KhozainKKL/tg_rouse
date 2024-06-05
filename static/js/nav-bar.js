
(function () {
	let a = document.querySelectorAll('.-black');
		for (let i=a.length; i--;) {
			if (a[i].href === window.location.pathname || a[i].href === window.location.href) a[i].className += ' select_href';
			if (a[i].href === window.location.pathname || a[i].href === window.location.href) {
				a[i].closest('.navbar__item').classList.add('select_href_div')
			}
		}
})();



