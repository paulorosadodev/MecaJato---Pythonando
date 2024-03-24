from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json

# Create your views here.
def clientes(request):
    if request.method == 'GET':
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        #Verificação se o CPF já existe
        cliente = Cliente.objects.filter(cpf=cpf)
        if cliente.exists():
            ctx = {
                'nome': nome, 
                'sobrenome': sobrenome, 
                'email':email,
                'erro': 'CPF JÁ EXISTE',
                'carros': zip(carros, placas, anos),
            }

            return render(request, 'clientes.html', ctx)
        
        #Verifica se email é valido
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            ctx = {
                'nome': nome, 
                'sobrenome': sobrenome, 
                'cpf':cpf,
                'erro': 'EMAIL INVALIDO',
                'carros': zip(carros, placas, anos),
            }
            
            return render(request, 'clientes.html', ctx)
        
        cliente = Cliente(nome=nome, sobrenome=sobrenome, email=email, cpf=cpf)

        cliente.save()

        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()

        return redirect('clientes')

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')

    cliente = Cliente.objects.get(id=id_cliente)
    
    # cliente = Cliente.objects.filter(id=id_cliente)

    # cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']

    ctx = {
        'nome': cliente.nome, 
        'sobrenome': cliente.sobrenome,
        'email': cliente.email,
        'cpf': cliente.cpf,
    }

    # return JsonResponse(cliente_json)
    return JsonResponse(ctx)