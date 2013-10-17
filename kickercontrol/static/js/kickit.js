$("#player li").draggable({
    containment: $("#player_field"),
    helper: "clone"
});

$("#spielfeld li").droppable({
    activeClass: "ui-state-default",
	hoverClass: "ui-state-hover",
	accept: ":not(.ui-sortable-helper)",
	drop: function(event, ui) {
	  $(this).text(ui.draggable.text());
	  var selector = "#" + $(this).attr("data-team-role");
	  $(selector).val(ui.draggable.attr("data-player-id"));
	  ui.draggable.remove();
	}
});

$('.slider-code').tinycarousel({
    duration: 200,
	callback: function(element, index){
    	var li = $(element);
    	var selector = '#' + li.attr("data-team-role");
    	$(selector).val(li.text());
	}
});