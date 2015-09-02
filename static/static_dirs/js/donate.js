'use strict';

$(document).ready(function() {
    // Toggle form submit content when clicked
    var submitButton = $('#submitButton');

    submitButton.on('click', function() {
        submitButton.find('span').toggle();
        submitButton.attr('disabled', 'disabled').addClass('btn-disabled');
    });
});