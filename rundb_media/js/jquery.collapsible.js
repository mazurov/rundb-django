/**
 * CHANGES
 * v.2.1.1 - Forgot to put the new filter from v.2.1 into the if (settings.closed)
 * v.2.1 - Changed $(this).parent().children().filter( ELEMENTS HERE) to $(this).parent().children().not('label').  Prevents you from having to guess what elements will be in the fieldset.
 * v.2.0 - Added settings to allow a fieldset to be initiated as closed.
 *
 * This script may be used by anyone, but please link back to me.
 *
 * Copyright 2009-2010.  Michael Irwin (http://michael.theirwinfamily.net)
 */
       
$.fn.collapse = function(options) {
	var defaults = {
		closed : false
	}
	settings = $.extend({}, defaults, options);

	return this.each(function() {
		var obj = $(this);
		obj.find("legend").addClass('collapsible').click(function() {
			if (obj.hasClass('collapsed'))
				obj.removeClass('collapsed').addClass('collapsible');
	
			$(this).removeClass('collapsed');
	
			obj.children().not('legend').toggle("slow", function() {
			 
				 if ($(this).is(":visible"))
					obj.find("legend").addClass('collapsible');
				 else
					obj.addClass('collapsed').find("legend").addClass('collapsed');
			 });
		});
		if (settings.closed) {
			obj.addClass('collapsed').find("legend").addClass('collapsed');
			obj.children().not("legend").css('display', 'none');
		}
	});
};


