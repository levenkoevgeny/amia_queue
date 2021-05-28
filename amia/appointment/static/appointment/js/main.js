$(document).ready(function () {

    'use strict';

    $(".date_picker_enabled").on("click", function () {

        $('#div_for_intervals').html('<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>');

        $('.can_be_disabled').each(function (){
            $(this).prop('disabled', true);
        });

        let picker_date = this.getAttribute("value");

        // $('#id_date_appointment').attr('value', picker_date_id);
        setTimeout(()=> get_free_intervals(picker_date), 500);
        // get_free_intervals(picker_date);

        $(".date_picker_enabled").each(function () {
            $(this).removeClass("btn-info");
            $(this).addClass("btn-light");
        });

        $(this).removeClass("btn-light");
        $(this).addClass("btn-info");


        // $(".date_picker_enabled").each(function() {
        //     $(this).removeClass("btn-success");
        //     $(this).addClass("btn-secondary");
        // });

    });


    function get_free_intervals(picker_date) {

        let search = {};
        let today = new Date();
        let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

        $.ajax({
            url: `/rest/appointments/?date_appointment=${picker_date}&is_booked=False&time_appointment=${time}`,
            type: "GET",
            dataType: 'json',
            data: search,
            timeout: 100000,
            success: function (data) {
                display_intervals(data);
                make_enabled();
            },
            error: function (e) {
                console.log("ERROR: ", e);
            },
            done: function (e) {
                console.log("DONE");
            }
        });
    }


    function display_intervals(dataJSON) {
        let elem = $('#div_for_intervals');
        elem.html('');
        $('#id_time_interval').attr('value', '');

        if (dataJSON.length) {
            elem.append("<b>Свободное время для записи:</b><br>");
            for (var i = 0; i < dataJSON.length; i++) {
                var new_button = $('<button type="button" class="btn btn-secondary m-2 interval_button" value="' + dataJSON[i].id + '">' + dataJSON[i].time_appointment + '</button>');
                elem.append(new_button);
            }
        } else {
            elem.append("<b>Записей нет</b><br>");
        }
    }

    function make_enabled(){
        $('.can_be_disabled').each(function (){
            $(this).prop('disabled', false);
        });
    }

    $("body").on("click", ".interval_button", function (e) {
        let elem = $(this);
        $(".interval_button").each(function () {
            $(this).removeClass("btn-success");
            $(this).addClass("btn-secondary");
        });
        elem.removeClass("btn-secondary");
        elem.addClass("btn-success");

        $('#id_time_interval').attr('value', this.getAttribute("value"));
    });


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

    $("#id_month_select").on("change", function () {
        window.location.href = `/?month=${$(this).val()}`
    });

});