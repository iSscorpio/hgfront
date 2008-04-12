$(document).ready(function(){
	
	$('#id_project_id').blur(function(){
		$(this).val($(this).val().toLowerCase().replace(/\s+/,'_'));
	});

	$('#project-create-form').validate({
		rules : {
			project_id : {
				required: true,
				minlength: 4,
				maxlength: 50,
				remote: '{% url project-verifyprojectshortname %}'
			},
			t_and_c : {
				required: true
			}
		},
		messages : {
			project_id : {
				required: 'A short name for project is required.',
				minlength: jQuery.format("Enter at least {0} characters"),
				remote: jQuery.format("{0} is already in use")
			},
			t_and_c : {
				required: "You must confirm this site's T&C's to continue"
			}
		}
	});
	
	$('#project-create-form').submit(function(event){
		event.preventDefault();  // stop the form from submitting and refreshing the page
		var form = this;               // in jQuery, this refers to the current element, which is #article_form
	
	    // grab each form value
		var data = {};
		data.project_id = $(form).find('input[@name=project_id]').val();
		data.project_name = $(form).find('input[@name=project_name]').val();
		data.short_description = $(form).find('input[@name=short_description]').val();
		data.full_description = $(form).find('textarea[@name=full_description]').val();
		data.project_icon = $(form).find('input[@name=project_icon]').val();
		data.hgweb_style = $(form).find('select[@name=hgweb_style]').val();
		data.t_and_c = $(form).find('input[@name=t_and_c]').val();
	
	    // now send the data to the server via AJAX
	    $.post($(form).attr('action'), data, function(data){
	        // do a simple alert for now, alert "Article was saved"
	        //alert(responseData.success);
			console.log(data);
			if (data.success == 'true') {
				$('#content').load(data.url, function(){
					hgfront.jsactivate();
				});
			} else {
				$('#content').load(data.url);
			}
	    }, "json");
	});
});