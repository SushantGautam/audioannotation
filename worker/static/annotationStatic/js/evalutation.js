$(document).ready(function () {
    $('#submit-task').on('click', (e) => {
        var ids = [];
        var form = $('form[name=evaluation_form]');
        if (!$(form)[0].checkValidity()) {
            alert('Please select all data in every column.');
            return false;
        }
        $(form).find('input[type=radio]:checked').each(function () {
                ids.push($(this).val());
            }
        );
        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrf_token,
                'ids': JSON.stringify(ids),
            },
            success: function (response) {
                // console.log(response)
                location.reload();
            },
            error: function (err) {
                console.log(err);
            }
        });
    });
});