$(function() {
  $('.progress-bar').each(function() {
    var bar_value = $(this).attr('aria-valuenow') + '%';
     $(this).css('width', bar_value);
  });
});

function catchPokemon(element, pokemon){
    $.get('/pokemon/catch/' + pokemon + '/')
        .done(function () {
            $.notify(pokemon + " added");
            $(element).addClass('btn-warning').removeClass('btn-success').text('Oops!').attr("onclick","deletePokemon(this, '" + pokemon + "')");
            $(element).parent().parent().addClass('panel-success').removeClass('panel-danger');
        })
        .fail(function () {
            alert("Error")
        })
}

function deletePokemon(element, pokemon){
    $.get('/pokemon/delete/' + pokemon + '/')
        .done(function () {
            $.notify(pokemon + " deleted");
            $(element).addClass('btn-success').removeClass('btn-warning').text('Caught!').attr("onclick","catchPokemon(this, '" + pokemon + "')");
            $(element).parent().parent().addClass('panel-danger').removeClass('panel-success');
        })
        .fail(function () {
            alert("Error")
        })
}

