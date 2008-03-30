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
		
		$('.tabs-navigation').tabs({ fx: { opacity: 'toggle' } }, function(){
			hgfront.jsactivate();
		});
		
		$('.link-create-repo').click(function(){
			hgfront.ajaxlink($(this).attr('href'), $(this).parent().parent())
			return false;
		});
		
		$('.link-create-issue').click(function(){
			hgfront.ajaxlink($(this).attr('href'), $(this).parent().parent())
			return false;
		});	
		
		$('#id_directory_name').blur(function(){
				$(this).val($(this).val().toLowerCase());
		});
		
		$('#repo-create-form').submit(function(event){
				event.preventDefault();  // stop the form from submitting and refreshing the page
				var form = this;               // in jQuery, this refers to the current element, which is #article_form
			
			    // grab each form value
				var data = {};
				data.directory_name = $(form).find('input[@name=directory_name]').val();
				data.display_name = $(form).find('input[@name=display_name]').val();
				data.description = $(form).find('textarea[@name=description]').val();
				data.creation_method = $(form).find('select[@name=creation_method]').val();
				data.default_path = $(form).find('input[@name=default_path]').val();
				data.allow_anon_pull = $(form).find('input:checkbox[@name=allow_anon_pull]').val();
				data.allow_anon_push = $(form).find('input:checkbox[@name=allow_anon_push]').val();
				data.hgweb_style = $(form).find('select[@name=hgweb_style]').val();
				data.archive_types = $(form).find('input[@name=archive_types]').val();
				data.local_members = $(form).find('select[@name=local_members]').val();
			
			    // now send the data to the server via AJAX
			    $.post($(form).attr('action'), data, function(data){
			        // do a simple alert for now, alert "Article was saved"
			        //alert(responseData.success);
					console.log(data);
					if (data.success == 'true') {
						
						target = $(form).parent().parent();
						
						$(target).load(data.url, function(){
							hgfront.jsactivate();
						});
					}
			    }, "json");
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
