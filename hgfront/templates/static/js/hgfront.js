var hgfront = hgfront || {}

hgfront.options = {
    version : 0.1,
    authors : "Tane Piper &amp; Miran Lipovaca"
}

hgfront.ajaxlink = function(url, target) {
	$(target).html('<div class="loading">Loading...</div>');
	
	$.ajax({
		url: url,
		success: function(html) {
			$(target).html('')
			$(target).append(html);
		}
	});
}

$(document).ready(function(){	
	$('.tabs-navigation').tabs({ fx: { opacity: 'toggle' } });
	
	$('.link-create-issue').click(function(){
		hgfront.ajaxlink($(this).attr('href'), '.issues-content')
		return false;
	});
});
