// отклонение вопроса присланого юзверем
$(document).ready(function(){

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
            }
        }
    };

    $('.delete').click(function(e){
        var this_id = this.getAttribute('q_id')

        model = getUrlParameter('model')
        if (model != 'questions'){
            model = 'not_conf_q'
        }

        $.ajax({
            dataType: 'json',
            url: '/admin',
            type: 'DELETE',
            data: JSON.stringify({'id': this_id, 'model': model}),
            success: function(data) {
                console.log(data)
                $(`#${this_id}`).css('display', 'none')
            }
        });

    })
});
