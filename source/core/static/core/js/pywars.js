pywars = window.pywars || {};

$.noty.defaults.layout = 'bottomCenter';
$.noty.defaults.animation.speed = 200;
$.noty.defaults.timeout = 2000;

pywars.messages = {
    error: function(message) {
        noty({text: message, type: 'error'})
    }
};

$(document).ajaxComplete(function(event, xhr, settings) {
    if (xhr.responseJSON && xhr.responseJSON.status == 'error') {
        pywars.messages.error(xhr.responseJSON.message);
    }
});