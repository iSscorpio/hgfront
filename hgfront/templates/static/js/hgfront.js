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
			hgfront.jsactivate();
		}
	});
}

hgfront.jsactivate = function(){
	$(document).ready(function(){
		$('*').unbind();
		
		$('.tabs-navigation').tabs({ fx: { opacity: 'toggle' } });

		$('.link-create-issue').click(function(){
			hgfront.ajaxlink($(this).attr('href'), '.issues-content')
			return false;
		});	
		
		$('#project-list a').click(function(){
			hgfront.ajaxlink($(this).attr('href'), '#main-area')
			return false;
		});	
		
		$('#project-create-form').submit(function(event){
			event.preventDefault();  // stop the form from submitting and refreshing the page
			var form = this;               // in jQuery, this refers to the current element, which is #article_form
		
		    // grab each form value
			var data = {};
			data.name_short = $(form).find('input[@name=name_short]').val();
			data.name_long = $(form).find('input[@name=name_long]').val();
			data.description_short = $(form).find('input[@name=description_short]').val();
			data.description_long = $(form).find('textarea[@name=description_long]').val();
			data.hgweb_style = $(form).find('select[@name=hgweb_style]').val();
		
		    // now send the data to the server via AJAX
		    $.post($(form).attr('action'), data, function(data){
		        // do a simple alert for now, alert "Article was saved"
		        //alert(responseData.success);
				console.log(data);
				if (data.success == 'true') {
					$(form).parent().parent().html('').load(data.url, function(){
						hgfront.jsactivate();
					});
				}
		    }, "json");
		});
	});
}

$(document).ready(function(){	
	hgfront.jsactivate();
});
