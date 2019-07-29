$(document).ready(function () {
    $("#button-play").click(function () {
        controlCommand($(this), cmds.PLAY)
    });
    $("#button-pause").click(function () {
        controlCommand($(this), cmds.PAUSE)
    });
    $("#button-stop").click(function () {
        controlCommand($(this), cmds.STOP)
    });
    $('#createNewRoom').click(function () {
        $('#joinForm').show();
        $('#roomStartText').hide();
    });

    $("#button-room").click(joinRoom);
    // Validate room with 1s delay
    let wto;
    $("#room_name").on('input', function () {
        clearTimeout(wto);
        wto = setTimeout(validateRoomName, 1000);
    });
    $("button.list-group-item").click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    });
    setInterval(updateStudentList, 2000);
    initPopover();
    setStates();
    getRooms();
    setInterval(getRooms, 5000);
});

const cmds = {
    PLAY: 0,
    PAUSE: 1,
    STOP: 2,
};

const states = {
    NOT_STARTED: -1,
    RUNNING: 0,
    PAUSED: 1,
    STOPPED: 2
};

setStates = function () {
    $('#button-play').prop('disabled', state === states.RUNNING)
        .find('path').css({fill: state === states.RUNNING ? "" : "#08e11f"});
    $('#button-pause').prop('disabled', state > states.RUNNING || state === states.NOT_STARTED)
        .find('path').css({fill: state > states.RUNNING || state === states.NOT_STARTED ? "" : "#08e11f"});
    $('#button-stop').prop('disabled', state === states.STOPPED || state === states.NOT_STARTED)
        .find('path').css({fill: state === states.STOPPED || state === states.NOT_STARTED ? "" : "#FF0000"});
};

initPopover = function () {
    $('#control-popover').popover({
        html: true,
        content: function () {
            const template = Handlebars.compile($("#popover-template").html());
            return (template())
        },
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


controlCommand = function (el, cmd) {
    el.blur();
    $.ajax({
        url: "/teacher/control",
        data: {'room_name': roomName, 'cmd': cmd},
        dataType: 'json',
        success: function () {
            state = cmd;
            setStates()
        },
        error: function (jqXHR) {
            // TODO: remove?
            console.log(jqXHR.responseJSON.err)
        }
    })
};

updateStudentList = function update() {
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
        success: function (data) {
            console.log("Test students created")
        },
        error: function (data) {
            // TODO: remove?
            console.log(data.error)
        }
    })
};

joinRoom = function () {
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
    const password = $('#room_password').val();
    if (!password.trim()) {
        $('#password_text').addClass('text-danger').removeClass('text-info');
        warnings.append('<li><h6 class="text-danger">Bitte wähle ein Passwort</h6></li>');
        error = true
    } else {
        $('#password_text').removeClass('text-danger').addClass('text-info');
    }
    if (error) {
        warnings.parent().show();
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
            $(location).attr('href', "/teacher?room_name=" + room_name);
        },
        /** @namespace data.responseJSON.err **/
        error: function (data) {
            console.log(data.responseJSON.err)
        }
    });
};


getRooms = function () {
    $.ajax({
        url: "rooms",
        dataType: 'json',
        success: function (data) {
            const list = $("#dropDownRooms");
            const selected = list.val();
            const l = $('.dropdown-item[data-delete="true"]')
            // Empty dropdown menu except static entries
            $.each(l, function (i, v) {
                v.remove();
            });
            /** @namespace data.rooms **/
            console.log(data.rooms)
            $.each(data.rooms, function (index, value) {
                list.append($('<a class="dropdown-item" data-delete="true" href="#"></a>').text(value));
            })
        }
    })
};