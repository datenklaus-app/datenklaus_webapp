$(document).ready(function () {
    $("#joinForm")[0].reset();
    // Validate room with 1s delay
    let wto;
    $("#room_name").on('input', function () {
        clearTimeout(wto);
        wto = setTimeout(validateRoomName, 1000);
    });
    $("button.list-group-item").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    });
});

function getRoomName() {
    let roomName;
    const roomElem = $('#room_name');
    roomName = roomElem.val();
//   if (!roomElem.val()) {
//       roomName = roomElem.attr('placeholder');
//   } else {
//   }
    return roomName;
}

validateRoomName = function () {
    const room = $('#room_name');
    if (!room) {
        setRoomWarning();
        return;
    }
    removeRoomWarning();
    $.ajax({
        url: "validate-room",
        data: room.serialize(),
        dataType: 'json',
        /** @namespace data.exists **/
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

function setRoomWarning() {
    const warnings = $('#warnings');
    $('#room_name_text').addClass('text-danger').removeClass('text-dark');
    warnings.append('<li><h6 class="text-danger" id="room-warning">Bitte wähle einen Raumnamen</h6></li>');
}

function removeRoomWarning() {
    const warnings = $('#warnings');
    warnings.find('#room-warning').remove();
    $('#room_name_text').removeClass('text-danger').addClass('text-dark');
}

function removeLessonWarning() {
    const warnings = $('#warnings');
    warnings.find("#lesson-warning").remove();
    $('#choose_lesson').removeClass('text-danger').addClass('text-dark');
}

createRoom = function () {
    const warnings = $('#warnings');
    warnings.empty();
    const room_name = getRoomName();
    const lesson = $('#lessons').find('button.active').find('#lesson_name').data('name');
    let error = false;
    if (lesson == null) {
        $('#choose_lesson').addClass('text-danger').removeClass('text-dark');
        warnings.append('<li><h6 class="text-danger" id="lesson-warning">Kein Modul ausgewählt</h6></li>');
        error = true
    } else {
        $('#choose_lesson').removeClass('text-danger').addClass('text-dark');
    }
    if (!room_name.trim()) {
        setRoomWarning();
        error = true
    }
    if (error) {
        return
    }
    $('#module_choice').val(lesson);
    $('#room_name').val(room_name);
    $.ajax({
        url: 'create-room',
        type: 'post',
        headers: {
            "X-CSRFToken": CSRF_TOKEN
        },
        dataType: 'json',
        data: $("#joinForm").serialize(),
        success: function (data) {
            updateRoom(data);
        },
        /** @namespace data.responseJSON.err **/
        error: function (data) {
            console.log(data.responseJSON.err)
        }
    });
};
