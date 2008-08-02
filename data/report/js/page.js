
window.onload = function() {
	tabs('#menu');
}

function tabs(id) {
	var objs = $(id).children("ul").children("li");
	objs.each(function(i) {
		var obj = $(this).children("a");
		var attr = obj.attr("href");
		console.log(attr);
		if (i > 0) {
			$(attr).addClass("hide");
		}
		obj[0].onclick = toggle;
	});
}

function toggle() {
	var attr = $(this).attr("href");
	$(this).parent().siblings().each(function(i) {
		var a = $(this).children("a").attr("href")
		if (!$(a).hasClass("hide")) {
			$(a).addClass("hide");
		}
	});
	$(attr).removeClass("hide");
}

