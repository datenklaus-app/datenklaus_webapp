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
