$(document).ready(function () {

    $("#button-room").click(function () {
        let room_name;
        if ($('#room_name').val() == '') {
            room_name = $('#room_name').attr('placeholder');
        } else {
            room_name = $('#room_name').val();
        }
        let lesson = $('#modules').find('button.active').find('#module_name').data('name')
        let error = false
        if (lesson == null) {
            $('#choose_module').addClass('text-danger').removeClass('text-info')
            $('#warnings').append('<li><h6 class="text-danger">Kein Modul ausgewählt</h6></li>')
            error = true
        }
        let password = $('#room_password').val()
        console.log(password)
        if (!password.trim()) {
            $('#password_text').addClass('text-danger').removeClass('text-info')
            $('#warnings').append('<li><h6 class="text-danger">Bitte wähle ein Passwort</h6></li>')
            error = true
        }
        console.log(error)
        if (error) {
            console.log("showing")
            $('#warnings').parent().show()
            return
        }
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