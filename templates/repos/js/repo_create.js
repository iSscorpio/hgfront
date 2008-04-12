$(document).ready(function(){
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
			if (data[0].success == 'true') {
				target = $(form).parent().parent().parent();
				$(target).load(data[0].url, function(){
					hgfront.jsactivate();
				});
			}
	    }, "json");
	});	
});
