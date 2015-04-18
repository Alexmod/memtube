$(document).ready(function () {
	$(document).on("click", ".viwed", function () {
		var videoid = $(this).data('id');
		$.getJSON('/_viwed', { "videoid": videoid });
		$("#butt_"+videoid).remove();
		$("#viwed_"+videoid).removeClass( )
	});
});
