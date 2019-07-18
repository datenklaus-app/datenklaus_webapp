$(document).ready(function () {
    validateRoomName();
    getRooms();
    setInterval(getRooms, 5000);

    $("#room_name").change(validateRoomName);

    $("#button-room").click(joinRoom);

    $("#button-room-existing").click(function () {
        const room = $('#rooms').val();
        myRedirect('room/' + room);
    });

    $("button.list-group-item").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    })
});

getRooms = function () {
    $.ajax({
        url: "get-rooms",
        dataType: 'json',
        success: function (data) {
            const list = $("#rooms");
            const selected = list.val();
            list.empty(); // remove old options
            $.each(data.rooms, function (index, value) {
                list.append($("<option></option>")
                    .attr("value", value).text(value));
                if (value === selected) {
                    list.val(selected)
                }
            })
        }
    })
};


validateRoomName = function () {
    const room = $('#room_name');
    if (!room) return;
    $.ajax({
        url: room.attr("data-validate-room-name-url"),
        data: room.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.exists) {
                $('#room_name_exists').show();
                $('#button-room').prop('disabled', true);
            } else {
                $('#room_name_exists').hide();
                $('#button-room').prop('disabled', false);
            }

        }
    });
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
    let lesson = $('#lessons').find('button.active').find('#lesson_name').data('name');
    let error = false;
    if (lesson == null) {
        $('#choose_lesson').addClass('text-danger').removeClass('text-info');
        $('#warnings').append('<li><h6 class="text-danger">Kein Modul ausgewählt</h6></li>');
        error = true
    }
    let password = $('#room_password').val();
    if (!password.trim()) {
        $('#password_text').addClass('text-danger').removeClass('text-info');
        $('#warnings').append('<li><h6 class="text-danger">Bitte wähle ein Passwort</h6></li>');
        error = true
    }
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
    $(form).submit();
};
