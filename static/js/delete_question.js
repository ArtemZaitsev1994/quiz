// отклонение вопроса присланого юзверем
$(document).ready(function(){
    var this_id = this.value

    $('#delete').click(function(e){

        $.ajax({
            dataType: 'json',
            url: '/admin',
            type: 'DELETE',
            data: JSON.stringify({'id': this.value}),
            success: function(data) {
                console.log(data)
                showSucces()
            }
        });

    })
})