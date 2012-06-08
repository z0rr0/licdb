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
function is_int(input) {
    return typeof(input)=='number' && parseInt(input)==input;
  }
// get list and statistics key's data
function get_keys(prog, page, divid) {
    vurl = "/get_keys/" + prog
    $.ajax({
        url: vurl,
        type: 'GET',
        dataType: 'html',
        context: document.body,
        data: {
            page: page
        },
        success: function (data) {
            $(divid).html(data);
        },
        error: function () {
            error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            $(divid).html('<span class="well span10">' + error_msg + '</span>');
        },
    });
}
// delete key record
function delkey(prog, keydiv, id, page) {
    if (confirm("Уверены, что хотите удалить данные?")) 
        $.get('/key/delete/' + id, function(data) {
                get_keys(prog, page, keydiv)
            }).error(function() { 
                error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
                $(keydiv).html('<span class="well span10">' + error_msg + '</span>');
            });
}
// delete key record
function delkey_home(page, id) {
    $.get('/key/delete/' + id, function(data) {
            key_update_view(page);
        }).error(function() { 
            error_msg = "Ошибка! Возможно у Вас не хватает прав или нет соединения с сервером.";
            error_msg = '<span class="well span12">' + error_msg + '</span>';
            $('#keycontent').html(error_msg);
        });
}

// search keys by program
function key_update_view(page) {
    divid = '#keycontent';
    program = $('#id_programma').val();
    if ($('#id_onlyfree').is(':checked')) onlyfree = 1;
    else onlyfree = 0;
    if (!is_int(page))  page=1;
    $.ajax({
        url: '/keys/program/' + program,
        type: 'GET',
        dataType: 'html',
        context: document.body,
        data: {
            free: onlyfree,
            page: page
        },
        success: function (data) {
            $(divid).html(data);
        },
        error: function () {
            error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            error_msg = '<span class="well span12">' + error_msg + '</span>';
            $(divid).html(error_msg);
        },
    });
}
// search keys by condition
function keys_search(page) {
    divid = '#searchkeys';
    type_req = 'POST';
    if (!is_int(page))  page=1;
    template = $('#seachtemplate').val();
    if (type_req=='GET') template = encodeURIComponent(template);
    $.ajax({
        url: '/key/search/ajax/',
        type: type_req ,
        dataType: 'html',
        context: document.body,
        data: {
            page: page,
            search: template
        },
        success: function (data) {
            $(divid).html(data);
        },
        error: function () {
            error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            error_msg = '<span class="well span12">' + error_msg + '</span>';
            $(divid).html(error_msg);
        },
    });
}