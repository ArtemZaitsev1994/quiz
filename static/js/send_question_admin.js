// валидация вопроса и отправка на сервер
$(document).ready(function(){

    categories = ['Что', 'Когда', 'Где', 'Почему']
    complexity = ['2', '3', '4']

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }
    function showSucces(){
        $('#error').html('');
        $('#success').html('Вопрос успешно отправлен.');
    }

    $('.submit').click(function(e){
        var this_id = this.getAttribute('q_id')
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

        q_data = {
            'text': $('#question_' + this_id).val(),
            'complexity': $('#complexity_' + this_id).val(),
            'category': $('#category_' + this_id).val(),
            'answer': $('#answer_' + this_id).val(),
            'type': 'questions',
            'not_conf_id': this_id
        }

        $.ajax({
            dataType: 'json',
            url: '/questions',
            type: 'POST',
            data: JSON.stringify(q_data),
            success: function(data) {
                $(`#${this_id}`).css('display', 'none')
            }
        });
    })
})