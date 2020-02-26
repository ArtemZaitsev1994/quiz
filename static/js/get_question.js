$(document).ready(function(){
    $('.q').on('click', function(){
        elem = $('#' + this.value)[0]

        $.ajax({
            dataType: 'json',
            url: '/random_question',
            type: 'GET',
            data: JSON.stringify({'id': this.value}),
            success: function(data) {
                console.log(data)
                html = `<h5 class="card-header">
                      <p>
                        <span>
                            Сложность: ${'🌟'*data.complexity}.
                        </span>
                        <span>
                            Категория: ${data.category}.
                        </span>
                      </p>
                  </h5>
                      <div class="card-body">
                          <div>
                              <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#q_text">Показать вопрос</button>
                              <div id="q_text" class="collapse">
                                ${data.text}
                              </div>
                          </div>

                          <div class="mt-3">
                              <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#q_answer">Показать ответ</button>
                              <div id="q_answer" class="collapse">
                                ${data.answer}
                              </div>
                          </div >

                          <div class="mt-3">
                                <button type="button" class="btn btn-outline-warning q" value="${data._id}">Заменить вопрос</button>
                          </div>

                      </div>`
                elem.innerHTML = html
                elem.id = data._id
            }
        });


    })
})