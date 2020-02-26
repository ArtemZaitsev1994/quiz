$(document).ready(function(){
    $('.q').on('click', function(){
        var this_id = this.value

        $.ajax({
            dataType: 'json',
            url: '/random_question',
            type: 'GET',
            data: JSON.stringify({'id': this_id}),
            success: function(data) {
                console.log(this_id)
                // $('#q_complexity_' + this_id)[0].innerHTML = `Сложность: ${'🌟'.repeat(data.complexity)}.`
                // $('#q_complexity_' + this_id)[0].attr('id', '#q_complexity_' + data._id)
                // $('#q_category_' + this_id)[0].innerHTML = `Категория: ${data.category}.`
                // $('#q_text_' + this_id)[0].innerHTML = data.text
                // $('#q_text_' + this_id).removeClass('show')
                // $('#q_answer_' + this_id)[0].innerHTML = data.answer
                // $('#q_answer_' + this_id).removeClass('show')
                header_html = `
                      <p>
                        <span>
                            Сложность: ${'🌟'.repeat(data.complexity)}.
                        </span>
                        <span>
                            Категория: ${data.category}.
                        </span>
                      </p>`
                body_html = `
                          <div>
                              <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#q_text_${data._id}">Показать вопрос</button>
                              <div id="q_text_${data._id}_${data._id}" class="collapse">
                                ${data.text}
                              </div>
                          </div>

                          <div class="mt-3">
                              <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#q_answer_${data._id}">Показать ответ</button>
                              <div id="q_answer_${data._id}" class="collapse">
                                ${data.answer}
                              </div>
                          </div >`
                $('#q_header_' + this_id)[0].innerHTML = header_html
                $('#q_header_' + this_id)[0].id = `q_header_${data._id}`
                $('#q_body_' + this_id)[0].innerHTML = body_html
                $('#q_body_' + this_id)[0].id = `q_body_${data._id}`
                
                $('#q_' + this_id).val(data._id)
                $('#q_' + this_id)[0].id = `q_${data._id}`


            }
        });


    })
})