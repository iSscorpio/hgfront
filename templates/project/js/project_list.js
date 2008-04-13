$(document).ready(function(){
	$('#project-list-table')
	.tablesorter({widthFixed: true, widgets: ['zebra']})
	.tablesorterPager({container: $("#pager"), positionFixed: false});
});

var view = {% autoescape off %}{{json_output}}{% endautoescape %}