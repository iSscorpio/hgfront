var hgfront = hgfront || {}

hgfront.options = {
    version : 0.1,
    authors : "Tane Piper, Miran Lipovaca &amp; Matt Marshall"
}

hgfront.ajaxlink = function(url, target) {
	$(target).html('<div class="loading">Loading...</div>');
	
	$.ajax({
		url: url,
		success: function(html) {
			$(target).html('')
			$(target).append(html);
			hgfront.jsactivate();
		}
	});
}

hgfront.jsactivate = function(){
	$(document).ready(function(){
		$('*').unbind();
		
		$('.tabs-navigation').tabs({ fx: { opacity: 'toggle' } });
		
		$('.link-create-repo').click(function(){
			hgfront.ajaxlink($(this).attr('href'), $(this).parent().parent())
			return false;
		});
		
		$('.link-create-issue').click(function(){
			hgfront.ajaxlink($(this).attr('href'), $(this).parent().parent())
			return false;
		});	
		
		
/*
		
		$('#project-list a').click(function(){
			hgfront.ajaxlink($(this).attr('href'), '#main-area')
			return false;
		});	
		*/
	});
};

$(document).ready(function(){	
	hgfront.jsactivate();
});
