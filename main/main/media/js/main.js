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
// delete key record
function delkey_home(page, id, search) {
    $.get('/key/del/' + id, function(data) {
            if (search) obj_search(page, 'key');
            else key_update_view(page);
        }).error(function() { 
            error_msg = "Ошибка! Возможно у Вас не хватает прав или нет соединения с сервером.";
            error_msg = '<span class="well span12">' + error_msg + '</span>';
            $('#keycontent').html(error_msg);
        });
}
function key_statistics (prog, divid, onlyfree) {
    $.ajax({
        url: '/key/statistics/' + prog,
        type: 'GET',
        dataType: 'html',
        context: document.body,
        data: {
            free: onlyfree,
        },
        success: function (data) {
            $(divid).html(data);
        },
        error: function () {
            error_msg = "Ошибка получения данных.";
            $(divid).html(error_msg);
        },
    });
}
// search keys by program (keys_home)
function key_update_view(page) {
    divid = '#result';
    program = $('#id_programma').val();
    if ($('#id_onlyfree').is(':checked')) onlyfree = 1;
    else onlyfree = 0;
    // statistics
    key_statistics(program, '#statistics', onlyfree);
    // page
    if (!is_int(page))  page=1;
    // view keys
    $.ajax({
        url: '/key/search/ajax/',
        type: 'GET',
        dataType: 'html',
        context: document.body,
        data: {
            free: onlyfree,
            page: page,
            prog: program,
            revers: 1
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
// search  by condition
function obj_search(page, objname) {
    divid = '#result';
    if (!is_int(page)) page=1;
    template = $('#seachtemplate').val();
    $.ajax({
        url: '/' + objname + '/search/ajax/',
        type: 'GET',
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
// add, edit Client form 
function change_client (id, page, revers) {
    if (!is_int(page)) page=1;
    if (!is_int(id)) id=0;
    varurl = '/client/edit/' + id + '?page=' + page;
    client_edit_add (varurl, revers);
}
function add_client (key, page, revers) {
    if (!is_int(page)) page=1;
    varurl = '/client/add/' + key + '/?page=' + page;
    client_edit_add (varurl, revers);
}
function client_edit_add (varurl, revers) {
    $.ajax({
        url: varurl,
        type: 'GET' ,
        dataType: 'html',
        context: document.body,
        data: { 'revers': revers },
        success: function (data) {
            $('#winmodal').html(data);
            $('#winmodal').modal();
        },
        error: function () {
            error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            alert(error_msg);
        },
    });
}
function save_client (id, page, revers, add) {
    if (!is_int(add)) varurl = '/client/edit/' + id;
    else varurl = '/client/add/' + id + '/?revers=' + revers;
    if ($('#id_student').is(':checked')) student = 1;
    else student = 0;
    $.ajax({
        url: varurl,
        type: 'POST' ,
        dataType: 'html',
        context: document.body,
        data: {
            name: $('#id_name').val(),
            student: student,
            date_start: $('#id_date_start').val(),
            manyuse: $('#id_manyuse').val(),
            comment: $('#id_comment').val(),
        },
        success: function (data) {
            if (data == 'saved') {
                if (revers) key_update_view(page);
                else obj_search(page, 'client') ;
                $('#winmodal').modal('hide');
            }
            else $('#winmodal').html(data);
            // $('#winmodal').modal('hide');
        },
        error: function () {
            $('#winmodal').modal('hide');
            error_msg = "Ошибка получения данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            alert(error_msg);
        },
    });
}
// delete client record
function del_client(page, id) {
    $.get('/client/del/' + id, function(data) {
            if (data == 'OK') obj_search(page, 'client');
            else alert('Ошибка!');
        }).error(function() { 
            error_msg = "Ошибка! Возможно у Вас не хватает прав или нет соединения с сервером.";
            error_msg = '<span class="well span12">' + error_msg + '</span>';
            $('#keycontent').html(error_msg);
        });
}
