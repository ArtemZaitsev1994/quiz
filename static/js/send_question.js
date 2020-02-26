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
        if (!($('#complexity').val() in complexity)) {
            errors += 'Не выбрана сложность.<br>'
        }
        if (!($('#category').val() in categories)) {
            errors += 'Не выбрана категория.<br>'
        }
        if ($('#answer').val().length < 1) {
            errors += 'Не указан ответ.<br>'
        }answer
        showError(errors)
        if (errors){
            return
        }
        showSucces()

    })
})