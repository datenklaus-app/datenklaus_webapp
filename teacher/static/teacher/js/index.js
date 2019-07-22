$(document).ready(function () {
    // Clear form on reload
    $(window).on('beforeunload', clearForm);
    // Get list of existing rooms
    getRooms();
    setInterval(getRooms, 5000);
    // Validate room with 1s delay
    let wto;
    $("#room_name").on('input', function () {
        clearTimeout(wto);
        wto = setTimeout(validateRoomName, 1000);
    });
    // Set click handler
    $("#button-room").click(joinRoom);
    $("#button-room-existing").click(function () {
        const room = $('#rooms').val();
        $(location).attr('href', 'room/' + room);
    });
    $("button.list-group-item").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    })
});

clearForm = function () {
    $(':input', '#joinForm')
        .not(':button, :submit, :reset, :hidden')
        .val('')
    $('#lessons').scrollTop(0);
};

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
    const room_name = getRoomName();
    const lesson = $('#lessons').find('button.active').find('#lesson_name').data('name');
    let error = false;
    if (lesson == null) {
        $('#choose_lesson').addClass('text-danger').removeClass('text-info');
        $('#warnings').append('<li><h6 class="text-danger">Kein Modul ausgewählt</h6></li>');
        error = true
    }
    const password = $('#room_password').val();
    if (!password.trim()) {
        $('#password_text').addClass('text-danger').removeClass('text-info');
        $('#warnings').append('<li><h6 class="text-danger">Bitte wähle ein Passwort</h6></li>');
        error = true
    }
    if (error) {
        $('#warnings').parent().show();
        return
    }
    $('#module_choice').val(lesson);
    $('#room_name').val(room_name);
    $.ajax({
        url: 'join-room',
        type: 'post',
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        dataType: 'json',
        data: $("#joinForm").serialize(),
        success: function () {
            $(location).attr('href', "room/" + room_name);
        },
        error: function (data) {
            console.log(data.responseJSON.err)
        }
    });
};
