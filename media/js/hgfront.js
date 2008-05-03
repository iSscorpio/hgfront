EnableTabs = $.klass({
	initialize : function(options) {
		this.element.tabs(options);
	}
});

LoadInParentTab = $.klass({
	onclick : function() {
		this.element.parents('.panel').load(this.element.attr('href'));
	}
});

$(document).ready(function(){
	$('.tabs-navigation').attach(EnableTabs, { fx: { opacity: 'toggle' } });
	$('.link-create-repo').attach(LoadInParentTab)
});