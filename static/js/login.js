$(document).ready(function(){

    function showError(error){
        $('#error').html(error);
    }

    $('#submit').click(function(e){
        errors = ''

        if ($('#Password').val().length < 1) {
            errors += 'Укажите пароль.<br>'
        }
        if ($('#Login').val().length < 1) {
            errors += 'Укажите логин.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        q_data = {
            'login': $('#Login').val(),
            'password': $('#Password').val(),
        }

        $.ajax({
            dataType: 'json',
            url: '/login',
            type: 'POST',
            data: JSON.stringify(q_data),
            success: function(data){
                console.log(data['location'])
                if (data.error){
                    showError(data.error)
                } else {
                    window.location = data['location']
                }
            }
        });

    })
});
