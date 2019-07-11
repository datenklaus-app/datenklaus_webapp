$(document).ready(function () {

    $("#room_name").change(validateRoomName);

    $("#button-room").click(joinRoom);

    $("button.list-group-item").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    })
});

validateRoomName = function () {
    const room = $('#room_name');
    console.log("change");
    $.ajax({
        url: room.attr("data-validate-room-name-url"),
        data: room.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.exists) {
                $('#room_name_exists').show();
            } else {
                $('#room_name_existing').hide();
            }

        }
    })
};

getRoomName = function () {
    let roomName;
    const roomElem = $('#room_name');
    if (!roomElem.val()) {
        roomName = roomElem.attr('placeholder');
    } else {
        roomName = roomElem.val();
    }
    return roomName;
};

joinRoom = function () {
    let room_name = getRoomName();
    let lesson = $('#modules').find('button.active').find('#module_name').data('name');
    let error = false;
    if (lesson == null) {
        $('#choose_module').addClass('text-danger').removeClass('text-info');
        $('#warnings').append('<li><h6 class="text-danger">Kein Modul ausgewählt</h6></li>');
        error = true
    }
    let password = $('#room_password').val();
    if (!password.trim()) {
        $('#password_text').addClass('text-danger').removeClass('text-info');
        $('#warnings').append('<li><h6 class="text-danger">Bitte wähle ein Passwort</h6></li>');
        error = true
    }
    // TODO Show error if room already exists
    if (error) {
        $('#warnings').parent().show();
        return
    }
    myRedirect('room/' + room_name, 'lesson', lesson)
};

myRedirect = function (redirectUrl, arg, value) {
    const form = $('<form action="' + redirectUrl + '" method="post">' + CSRF_TOKEN +
        '<input type="hidden" + " name="' + arg + '" value="' + value + '">' + '</form>');
    $('body').append(form);
    console.log(form);
    $(form).submit();
};
