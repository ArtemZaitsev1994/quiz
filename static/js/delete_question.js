// отклонение вопроса присланого юзверем
$(document).ready(function(){

    $('.delete').click(function(e){
        var this_id = this.getAttribute('q_id')

        $.ajax({
            dataType: 'json',
            url: '/admin',
            type: 'DELETE',
            data: JSON.stringify({'id': this_id}),
            success: function(data) {
                console.log(data)
                $(`#${this_id}`).css('display', 'none')
            }
        });

    })
})