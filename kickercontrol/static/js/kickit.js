$("#player li").draggable({
    containment: $("#player_field"),
    cursor: "crosshair",
    helper: "clone"
});

$("#spielfeld li").droppable({
    activeClass: "ui-state-default",
	hoverClass: "ui-state-hover",
	accept: ":not(.ui-sortable-helper)",
	drop: function( event, ui ) {
	  $(this).text(ui.draggable.text());
	  var selector = "#" + $(this).attr("data-team-role");
	  $(selector).val(ui.draggable.attr("data-player-id"))
	  ui.draggable.remove();
	}
});
