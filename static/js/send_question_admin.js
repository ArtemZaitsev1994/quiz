// валидация вопроса и отправка на сервер
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

    categories = ['Что', 'Кто', 'Когда', 'Где', 'Почему']
    complexity = ['2', '3', '4']

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showSucces(){
        $('#error').html('');
        $('#success').html('Вопрос успешно отправлен.');
    }

    send_question = (this_id=null) => {
        if (this_id === null) {
            this_id = this.getAttribute('q_id')
        }
        errors = ''

        if ($('#question_' + this_id).val().length < 10) {
            errors += 'Слишком короткий вопрос.<br>'
        }
        if (complexity.indexOf($('#complexity_' + this_id).val()) == -1) {
            errors += 'Не выбрана сложность.<br>'
        }
        if (categories.indexOf($('#category_' + this_id).val()) == -1) {
            errors += 'Не выбрана категория.<br>'
        }
        if ($('#answer_' + this_id).val().length < 1) {
            errors += 'Не указан ответ.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        model = getUrlParameter('model')
        if (model != 'questions'){
            model = 'not_conf_q'
        }


        q_data = {
            'text': $('#question_' + this_id).val(),
            'complexity': $('#complexity_' + this_id).val(),
            'category': $('#category_' + this_id).val(),
            'answer': $('#answer_' + this_id).val(),
            'type': 'questions',
        }
        q_data[model] = this_id

        $.ajax({
            dataType: 'json',
            url: '/questions',
            type: 'POST',
            data: JSON.stringify(q_data),
            success: function(data) {
                $(`#${this_id}`).css('display', 'none')
            }
        });
    }

    $('#submit').click(send_question)
    $('textarea').on('keydown', function(e){
        if (e.keyCode == 13 & !e.shiftKey) {
            e.preventDefault()
            send_question(this.getAttribute('q_id'))
        }
    })

    $('#logout').on('click', function(e){
        $.ajax({
            url: '/login',
            type: 'DELETE',
            success: function(data) {
                window.location = data['location']
            }
        });
    })
});