$(document).ready(function () {
    $("#button-pause").click(function () {
        controlCommand($(this), cmds.PAUSE)
    });
    $("#button-stop").click(function () {
        controlCommand($(this), cmds.STOP)
    });
    setInterval(updateStudentList, 2000);
    initPopover();
});

const cmds = {
    PAUSE: 0,
    STOP: 1,
    EVAL: 2
}

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
            console.log("Command success");
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

