function add_carro(){

    container = document.getElementById("form-carro")

    html = "<br><div class='row'>" +
        "<div class='col-md'>" +
        "<input type='text' placeholder='Carro' class='form-control' name='carro'>" +
        "</div>" +
        "<div class='col-md'>" +
        "<input type='text' placeholder='Placa' class='form-control' name='placa'>" +
        "</div>" +
        "<div class='col-md'>" +
        "<input type='number' placeholder='Ano' class='form-control' name='ano'>" +
        "</div>" +
        "</div>"

    container.innerHTML += html
}

function desaparecerElemento(elemento) {
    // Definir um atraso de 6 segundos (6000 milissegundos)
    setTimeout(function() {
        // Remover o elemento definido
        elemento.style.display = 'none';
    }, 6000);
}

var elemento = document.getElementById("erro");
if (elemento) {
    desaparecerElemento(elemento);
}

