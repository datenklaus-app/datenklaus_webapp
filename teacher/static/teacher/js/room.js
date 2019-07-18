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
    setInterval(updateStudentList, 2000);
    initPopover();
    setStates();
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
    $('#button-play').find('path').css({fill: state === states.RUNNING ? "" : "#08e11f"})
        .prop('disabled', state === states.RUNNING);
    $('#button-pause').find('path').css({fill: state > states.RUNNING || state === states.NOT_STARTED ? "" : "#08e11f"})
        .prop('disabled', state > states.RUNNING || state === states.NOT_STARTED);
    $('#button-stop').find('path').css({fill: state === states.STOPPED || state === states.NOT_STARTED ? "" : "#FF0000"})
        .prop('disabled', state === states.STOPPED || state === states.NOT_STARTED)
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
        error: function (data) {
            console.log(data.error);
        }
    })
};

updateStudentList = function update() {
    $.ajax({
        url: "/teacher/get-students",
        data: {'room_name': roomName},
        dataType: 'json',
        success: function (data) {
            const students = $("#students");
            students.empty(); // remove old options
            const source = document.getElementById("connected-students").innerHTML;
            const template = Handlebars.compile(source);
            $.each(data.students, function (index, value) {
                students.append(template(value));
            },);
        },
        error: function (data) {
            console.log(data.error)
        }
    })
};

