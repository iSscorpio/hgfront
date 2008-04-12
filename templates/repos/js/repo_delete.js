$(document).ready(function(){
	
	$('.delete').click(function(){
		var url = $(this).attr('href');
		$.ajax({
			type: "GET",
			url: url,
			dataType: "json",
			success: function(data){
				console.log(data);
				if (data[0].success == 'true') {
					$('#content').load(data[0].url, function(){
						hgfront.jsactivate();
					});
				} else {
					$('#content').load(data[0].url);
				}	
			}
		});
	});
	
	$('.delete').confirm(
		{
  			timeout:3000,
  			dialogShow:'fadeIn',
  			dialogSpeed:'slow',
  			buttons: {
    		wrapper:'<button></button>',
    		separator:'  '
  		}  
	});
});
