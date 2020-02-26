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

    $('#submit').click(function(e){
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
        }answer
        
        console.log($('#complexity').val())
        if (errors){
            showError(errors)
            return
        }

        q_data = {
            'text': $('#question').val(),
            'complexity': $('#complexity').val(),
            'category': $('#category').val(),
            'answer': $('#answer').val()
        }
        console.log(q_data)
        $.ajax({
            dataType: 'json',
            url: '/questions',
            type: 'POST',
            data: JSON.stringify(q_data),
            success: function(data) {
                console.log(data)
                showSucces()
            }
        });

    })
})