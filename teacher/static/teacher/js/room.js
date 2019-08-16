$(document).ready(function () {
    $("#button-play").click(function () {
        controlCommand($(this), cmds.PLAY, states.RUNNING)
    });
    $("#button-pause").click(function () {
        controlCommand($(this), cmds.PAUSE, states.PAUSED)
    });
    $("#button-stop").click(function () {
        controlCommand($(this), cmds.STOP, states.CLOSED)
    });
    $('#createNewRoom').click(function () {
        $('#roomStartText').hide();
        $('#controlsRow').hide();
        $('#auswertung').hide();
        $('#joinForm').show();
        clearTimeout(interval);
    });

    $("#button-room").click(createRoom);
    // Validate room with 1s delay
    let wto;
    $("#room_name").on('input', function () {
        clearTimeout(wto);
        wto = setTimeout(validateRoomName, 1000);
    });
    $("button.list-group-item").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    });

    initPopover();
});

var interval;
const cmds = {
    PLAY: 0,
    PAUSE: 1,
    STOP: 2,
};

const states = {
    CLOSED: 0,
    WAITING: 1,
    RUNNING: 2,
    PAUSED: 3,
};

setStates = function () {
    $('#button-play').prop('disabled', state === states.RUNNING);
    $('#button-pause').prop('disabled', state === states.PAUSED);
    $('#button-stop').prop('disabled', state === states.CLOSED);
};

initPopover = function () {
    $('.popover-dismiss').popover({
        trigger: 'focus'
    })

    $('#control-popover').popover({
        html: true,
        content: function () {
            const template = Handlebars.compile($("#popover-template").html());
            return (template())
        },
    });
};

updateResults = function () {
    $.ajax({
        url: "/teacher/results/" + roomName,
        dataType: 'json',
        success: function (data) {
            const results = $("#state_results");
            results.empty(); // remove old options
            const source = document.getElementById("resultItem").innerHTML;
            const template = Handlebars.compile(source);
            /** @namespace data.results **/
            $.each(data.results, function (index, value) {
                value.no_students = data.no_students;
                results.append(template(value));
            },);
        },
        error: function (jqXHR) {
            console.log(jqXHR.responseJSON.err)
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

validateRoomName = function () {
    const room = $('#room_name');
    if (!room) return;
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


controlCommand = function (el, cmd, s) {
    el.blur();
    $.ajax({
        url: "/teacher/control",
        data: {'room_name': roomName, 'cmd': cmd},
        dataType: 'json',
        success: function () {
            state = s;
            setStates()
        },
        error: function (jqXHR) {
            // TODO: remove?
            console.log(jqXHR.responseJSON.err)
        }
    })
};

updateStudentList = function () {
    $.ajax({
        url: "/teacher/students",
        data: {'room_name': roomName},
        dataType: 'json',
        success: function (data) {
            const students = $("#students");
            students.empty(); // remove old options
            const source = document.getElementById("connected-students").innerHTML;
            const template = Handlebars.compile(source);
            /** @namespace data.students **/
            $.each(data.students, function (index, value) {
                students.append(template(value));
            },);
        },
        error: function (data) {
            // TODO: remove?
            console.log(data.error)
        }
    })
};

createTestStudents = function () {
    $.ajax({
        url: "/teacher/test-students",
        data: {'room_name': roomName},
        dataType: 'json',
        success: function () {
            console.log("Test students created")
        },
        error: function (data) {
            // TODO: remove?
            console.log(data.error)
        }
    })
};

createRoom = function () {
    const warnings = $('#warnings');
    warnings.empty();
    const room_name = getRoomName();
    const lesson = $('#lessons').find('button.active').find('#lesson_name').data('name');
    let error = false;
    if (lesson == null) {
        $('#choose_lesson').addClass('text-danger').removeClass('text-info');
        warnings.append('<li><h6 class="text-danger">Kein Modul ausgewählt</h6></li>');
        error = true
    } else {
        $('#choose_lesson').removeClass('text-danger').addClass('text-info');
    }
    if (!room_name.trim()) {
        $('#room_name_text').addClass('text-danger').removeClass('text-info');
        warnings.append('<li><h6 class="text-danger">Bitte wähle einen Raumnamen</h6></li>');
        error = true
    } else {
        $('#room_name_text').removeClass('text-danger').addClass('text-info');
    }
    if (error) {
        warnings.parent().show();
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

updateRoom = function (data) {
    roomName = data.room_name;
    state = data.state;
    $('#roomLesson').text(data.lesson);
    $('#button-auswertung').removeClass('disabled');
    updateView();
};
