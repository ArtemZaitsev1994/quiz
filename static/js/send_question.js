// валидация вопроса и отправка на сервер
$(document).ready(function(){

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

    send_question = function(){
        errors = ''

        if ($('#question').val().length < 10) {
            errors += 'Слишком короткий вопрос.<br>'
        }
        if (complexity.indexOf($('#complexity').val()) == -1) {
            errors += 'Не выбрана сложность.<br>'
        }
        if (categories.indexOf($('#category').val()) == -1) {
            errors += 'Не выбрана категория.<br>'
        }
        if ($('#answer').val().length < 1) {
            errors += 'Не указан ответ.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        q_data = {
            'text': $('#question').val(),
            'complexity': $('#complexity').val(),
            'category': $('#category').val(),
            'answer': $('#answer').val(),
            'type': 'not_conf_q'
        }

        $.ajax({
            dataType: 'json',
            url: '/questions',
            type: 'POST',
            data: JSON.stringify(q_data),
            success: function(data) {
                showSucces()
            }
        });

    }

    $('#submit').click(send_question)
    $('textarea').on('keydown', function(e){
        if (e.keyCode == 13 & !e.shiftKey) {
            e.preventDefault()
            send_question()
        }
    })
});
