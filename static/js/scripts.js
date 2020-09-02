$(document).ready(function(){
    $('.delete-position').click(function(){
        var position_id = $(this).data('id')
        fetch('/position_delete', {
            method: 'DELETE',
            body: JSON.stringify({'position_id': position_id}),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            window.location.href = data['url']
        })
    })
})