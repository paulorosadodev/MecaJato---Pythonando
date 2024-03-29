function desaparecerElemento(elemento) {
    // Definir um atraso de 6 segundos (6000 milissegundos)
    setTimeout(function() {
        // Remover o elemento definido
        elemento.style.display = 'none';
    }, 3000);
}

var elemento = document.getElementById("erro");
if (elemento) {
    desaparecerElemento(elemento);
}

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

function exibir_form(tipo) {
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att-cliente')

    if (tipo == 1) {
        att_cliente.style.display = 'none'
        add_cliente.style.display = 'block'
    } else if (tipo == 2){
        att_cliente.style.display = 'block'
        add_cliente.style.display = 'none'
    }
}

function dados_clientes() {
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value

    data = new FormData()
    data.append("id_cliente", id_cliente)
    
    fetch("/clientes/atualiza_cliente/", {
        method:"POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data,
    }).then (function(result){
        return result.json()
    }).then (function(data){
        document.getElementById('form-att-cliente').style.display = 'block'
        
        id = document.getElementById('id')
        id.value = data['id']
        
        nome = document.getElementById('nome')
        nome.value = data['nome']
        
        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['sobrenome']
        
        cpf = document.getElementById('cpf')
        cpf.value = data['cpf']
        
        email = document.getElementById('email')
        email.value = data['email']
        
        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ''
        
        if (data['carros'].length == 0) {
            div_carros.innerHTML = '<p>O cliente não possui carros cadastrados</p>'
        }
        
        for (i = 0; i < data['carros'].length; i++) {
            car = data['carros'][i]
            div_carros.innerHTML += "<form action='/clientes/update_carro/" + car.pk + "' method='POST'>\
                                    <div class='row'>\
                                    <div class='col-md'>\
                                    <input class='form-control' type='text' name='carro' value='" + car.carro + "'>\
                                    </div>\
                                    <div class='col-md'>\
                                    <input class='form-control' type='text' name='placa' value='" + car.placa + "'>\
                                    </div>\
                                    <div class='col-md'>\
                                    <input class='form-control' type='number' name='ano' value='" + car.ano + "'>\
                                    </div>\
                                    <div class='col-md'>\
                                    <input class='btn btn-success' type='submit' value='Salvar'>\
                                    </div>\
                                    </form>\
                                    <div class='col-md'>\
                                            <a class='btn btn-danger' href='/clientes/excluir_carro/" + car.pk + "'>Excluir</a>\
                                            </div>\
                                            </div><br>"
                                        }
                                    })
}

function update_cliente(){
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    id = document.getElementById('id').value

    fetch('/clientes/update_cliente/' + id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf,
        })

    }).then(function(result){
        return result.json()
    }).then(function(data){

        if(data['status'] == '200'){
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']

            div_success = document.getElementById('message_update')
            div_success.innerHTML = ''
            div_success.innerHTML += '<div class="alert alert-success" role="alert">\
                                    Dados alterados com sucesso\
                                    </div>'
            desaparecerElemento(div_success);
        }else{
            div_erro = document.getElementById('message_update')
            div_erro.innerHTML = ''
            erro = data['erro']
            div_erro.innerHTML += '<div class="alert alert-danger" role="alert">' + erro + '</div>'
            desaparecerElemento(div_erro);
        }
    })
}
