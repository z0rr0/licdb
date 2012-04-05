/*
 for djago Cross Site Request Forgery protection (CSRF)
*/
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

// update left menu
function get_keys(prog) {
    vurl = "/get_keys/" + prog
    $.ajax({
        url: vurl,
        type: 'GET',
        dataType: 'html',
        context: document.body,
        // data: {
        //     progid: prog
        // }
        success: function (data) {
            $("#keylist").html(data);
        },
        error: function () {
            // alert('sorry, error'); 
            error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            $("#keylist").html('<span class="well span10">' + error_msg + '</span>');
        },
    });
}

function delkey(prog, keydiv, id) {
    if (confirm("Уверены, что хотите удалить данные?")) 
        $.get('/key/delete/' + id, function(data) {
                get_keys(prog)
            }).error(function() { 
                error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
                $("#" + keydiv).html('<span class="well span10">' + error_msg + '</span>');
            });
}