from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt

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
    carros = Carro.objects.filter(cliente=cliente)
    carro_list = [{'carro': carro.carro, 'placa': carro.placa, 'ano': carro.ano, 'pk': carro.id} for carro in carros]
    # cliente = Cliente.objects.filter(id=id_cliente)

    # cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    # carros_json = json.loads(serializers.serialize('json', carros))

    ctx = {
        'nome': cliente.nome, 
        'sobrenome': cliente.sobrenome,
        'email': cliente.email,
        'cpf': cliente.cpf,
        'id': cliente.id,
        'carros': carro_list,
    }

    # return JsonResponse(cliente_json)
    return JsonResponse(ctx)

@csrf_exempt
def att_carro(request, id):
    if request.method == 'POST':
        novoNome = request.POST.get('carro')
        novaPlaca = request.POST.get('placa')
        novoAno = request.POST.get('ano')

        carro = Carro.objects.get(id=id)

        carros = Carro.objects.filter(placa=novaPlaca).exclude(id=id)
        if carros.exists():
            return HttpResponse('Placa já existente')

        carro.carro = novoNome
        carro.placa = novaPlaca
        carro.ano = novoAno

        carro.save()

        return HttpResponse('Dados alterados com sucesso')

@csrf_exempt
def dlt_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id}')
    except:
        return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id}')

def update_cliente(request, id):
    if request.method == 'POST':
        body = json.loads(request.body)

        nome = body['nome']
        sobrenome = body['sobrenome']
        email = body['email']
        cpf = body['cpf']

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return JsonResponse({'erro':'Email inválido'})
        
        if Cliente.objects.filter(email=email).exclude(id=id).first():
            return JsonResponse({'erro':'Email já cadastrado'})
        
        if Cliente.objects.filter(nome=nome).exclude(id=id).first():
            return JsonResponse({'erro':'Usuário já cadastrado'})

        cliente = get_object_or_404(Cliente, id=id)

        try:
            cliente.nome = nome
            cliente.sobrenome = sobrenome
            cliente.email = email
            cliente.cpf = cpf

            cliente.save()

            return JsonResponse({'status': '200','nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
        except:
            return JsonResponse({'status': '500'}) 