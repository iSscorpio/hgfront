var hgfront = hgfront || {}

hgfront.options = {
    version : 0.1,
    authors : "Tane Piper &amp; Miran Lipovaca"
}

hgfront.ajaxlink = function(url, target) {
	$(target).html('Loading');
	
	$.ajax({
		url: url,
		success: function(html) {
			$(target).html('')
			$(target).append(html);
		}
	});
}

$(document).ready(function(){
	
//	$.ui.history("enable");
	
	$('#project-details-tabs, #repo-details-tabs, #profile-details-tabs').tabs({ fx: { opacity: 'toggle' } });
/*	
	$('.home').click(function(){
		hgfront.ajaxlink($(this).attr('href'), '#content')
		return false;
	});

	$('.ui-tabs-panel a').click(function(){
		hgfront.ajaxlink($(this).attr('href'), '#content')
		return false;
	});
*/	
	$('.link-create-issue').click(function(){
		hgfront.ajaxlink($(this).attr('href'), '.issues-content')
		return false;
	});
	
	$('.issues-content a').click(function(){
		hgfront.ajaxlink($(this).attr('href'), '.issues-content')
		return false;

	});

});
