function check_for_active_lesson() {
    $.ajax({
        method: "POST",
        url: '/lesson/status',
        dataType: 'json',
        contentType: 'json',
        headers: {
            "X-CSRFToken": "{{ csrf_token }}"
        },
        success: function (data) {
            if (data.redirect)
                window.location.replace(data.redirect);

            if (data.running && data.is_sync)
                window.location.replace('/lesson/');
        }
    })
}

setInterval(check_for_active_lesson, 1000);