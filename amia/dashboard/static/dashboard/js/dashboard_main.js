$(document).ready(function () {
    'use strict';

    $("#is_booked_all_checkbox_id").on("click", function () {
        let is_booked_list = $('.is_booked_checkbox');

        if ($(this).is(':checked')) {
            is_booked_list.each(function () {
                $(this).prop('checked', true);
            })
        } else {
            is_booked_list.each(function () {
                $(this).prop('checked', false);
            })
        }
    });

    $("#save_button").on("click", function () {
        make_elements_disabled();
        let is_booked_list = $('.is_booked_checkbox');

        let requests = []
        is_booked_list.each(function () {
            let is_booked = !!($(this).is(':checked'));
            let last_name = $(`#id_last_name_${$(this).val()}`).val();
            let date_of_birth = $(`#id_date_of_birth_${$(this).val()}`).val();
            let comment = $(`#id_comment_${$(this).val()}`).val();
            const request = fetch(`/rest/appointments/${$(this).val()}/`, {
                method: 'PATCH',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({"is_booked": is_booked, "last_name": last_name, "date_of_birth": date_of_birth, "comment": comment})
            });
            requests.push(request);
        });

        (async () => {
            Promise.all(requests)
                .then(() => document.location.reload())
                .catch((e) => console.log('Ошибка сохранения!!!', e))
                .finally(() => document.location.reload());
        })();
    });

    function make_elements_disabled() {
        $('.may_be_disabled').each(function () {
            $(this).prop('disabled', true);
            $('#save_button').html('<div className="spinner-border" role="status"><span className="visually-hidden">Сохранение...</span></div>');
        });

    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});