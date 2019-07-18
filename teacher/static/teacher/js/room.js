$(document).ready(function () {
    $("#button-pause").click(pauseModule);
    setInterval(updateStudentList, 2000)
});

pauseModule = function () {
    $.ajax({
        url: "/teacher/pause-module",
        data: {'room_name': roomName},
        dataType: 'json',
        success: function () {
            console.log("Module paused");
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

