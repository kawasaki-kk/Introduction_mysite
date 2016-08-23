$(function() {
	$('.del_confirm').on('click', function () {
		$("#del_pk").text($(this).attr("pk"));
		$('#del_url').attr('href', $(this).attr("url"));
	});
});