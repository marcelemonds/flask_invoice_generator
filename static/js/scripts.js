$(document).ready(function(){
    $('#positions-submit').click(function(e){
        e.preventDefault()
        // show positions table
        $('#positions-table-container').removeClass('hidden-content')
        // get form data
        var unit = $('#unit').val()
        var amount = $('#amount').val()
        var price = $('#price').val()
        var description = $('#description').val()
        var total = amount * price
        // append table row
        $('#positions-table-body').append('<tr class="position"><td>'+unit+'</td><td>'+amount+'</td><td>'+price+'</td><td>'+description+'</td><td>'+total+'</td></tr>')
        // clear input fields
        $('#unit').val('')
        $('#amount').val('')
        $('#price').val('')
        $('#description').val('')
    })
})