$(document).ready(function(){

    q_ids = $('#my-data').data().q_ids.split('.')

    $('.q').on('click', function(){
        var this_id = this.value
        send_data = {'ids': q_ids}
        console.log(JSON.stringify(send_data))

        $.ajax({
            dataType: 'json',
            url: '/random_question',
            type: 'PUT',
            data: JSON.stringify(send_data),
            success: function(data) {
                // $('#q_complexity_' + this_id)[0].innerHTML = `Сложность: ${'🌟'.repeat(data.complexity)}.`
                // $('#q_complexity_' + this_id)[0].attr('id', '#q_complexity_' + data._id)
                // $('#q_category_' + this_id)[0].innerHTML = `Категория: ${data.category}.`
                // $('#q_text_' + this_id)[0].innerHTML = data.text
                // $('#q_text_' + this_id).removeClass('show')
                // $('#q_answer_' + this_id)[0].innerHTML = data.answer
                // $('#q_answer_' + this_id).removeClass('show')
                if (data.warning){
                    header_html = `<p>Упс...</p>`
                    body_html = `<p>У нас закончились вопросы, но вы можете прислать свои, для других пользователей!</p>`
                    $('#q_header_' + this_id)[0].innerHTML = header_html
                    $('#q_body_' + this_id)[0].innerHTML = body_html
                } else {
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
                                  <div id="q_text_${data._id}" class="collapse">
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

                    q_ids.push(data._id)
                }
                

            }
        });


    })
})