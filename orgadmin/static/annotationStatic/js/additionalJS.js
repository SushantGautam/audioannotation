$(document).ready(function () {
    $('.right-section .result-section').on('click', '.region-edit', () => {
        $('.result .audio-data').addClass('d-none');
        $('.annotation-form-section').removeClass('d-none');
        var id = $('.result-section .region-edit').attr('data-region_id');
        $('.annotation-form .annotation-text').val(wavesurfer.regions.list[id].data.text);
        $('.annotation-form .region-id').val(wavesurfer.regions.list[id].id);
    });

    $('.annotation-form').on('submit', (e) => {
        e.preventDefault();
        var annotated_text = $('.annotation-form .annotation-text').val();
        // Change value in hidden form also
        $('#vals__text').val(annotated_text);
        $('.result .audio-data').removeClass('d-none');
        $('.annotation-form-section').addClass('d-none');
        region = wavesurfer.regions.list[$('.annotation-form .region-id').val()];
        data = region.data;
        data.text = [annotated_text];
        region.update({
            data: data,
        });
        $('.result .text').html(region.data.text);
        changeAnnotationText(region);
    });

    $('.annotation-form button[type=cancel]').on('click', (e) => {
        e.preventDefault();
        $('.result .audio-data').removeClass('d-none');
        $('.annotation-form-section').addClass('d-none');
    });

    $('.result-section').on('click', '.region-delete', () => {
        deleteRegion($('.result-section .region-delete').attr('data-region_id'));
    });

    $('#save-btn').on('click', (e) => {
        localforage.getItem(key_annotation).then(function(value) {
            // This code runs once the value has been loaded
            // from the offline store.
            console.log(value);
            $.ajax({
                url: SAVE_ANNOTATION_URL,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrf_token,
                    'annotated_data': JSON.stringify(value),
                },
                success: function (response) {
                    console.log(response);
                },
                error: function (err) {
                    console.log(err);
                }
            });
        }).catch(function(err) {
            // This code runs if there were any errors
            console.log(err);
        });
    });

    function changeAnnotationText(region) {
        console.log(region)
        $(`.wavesurfer-region[data-id=${region.id}]`).find('.region-text').html(region.data.text);
    }
});