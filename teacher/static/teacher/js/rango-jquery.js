$(document).ready(function () {

    $("#button-room").click(function () {
        let room_name;
        if ($('#room_name').val() == '') {
            room_name = $('#room_name').attr('placeholder');
        } else {
            room_name = $('#room_name').val();
        }
        let lesson = $('#modules').find('button.active').find('#module_name').data('name')
        myRedirect('room/' + room_name, 'lesson', lesson)
    });

    $("button.list-group-item").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    });


});

myRedirect = function (redirectUrl, arg, value) {
    const form = $('<form action="' + redirectUrl + '" method="post">' + CSRF_TOKEN +
        '<input type="hidden" + " name="' + arg + '" value="' + value + '">' + '</form>');
    $('body').append(form);
    console.log(form)
    $(form).submit();
}