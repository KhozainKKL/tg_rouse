

(function () {
	var a = document.querySelectorAll('.-black');
    var icon = document.querySelectorAll('.icon');
		for (var i=a.length; i--;) {
			if (a[i].href === window.location.pathname || a[i].href === window.location.href) a[i].className += ' select_href';
		}
})();