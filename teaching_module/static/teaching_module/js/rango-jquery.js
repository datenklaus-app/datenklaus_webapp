$(document).ready(function () {

    $("#button-room").click(function () {
        let room_name;
        if ($('#room_name').val() == '') {
            room_name = $('#room_name').attr('placeholder');
        } else {
            room_name = $('#room_name').val();
        }
        window.location.href = 'room/' + room_name;
    });
});