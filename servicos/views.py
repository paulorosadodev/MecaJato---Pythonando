from django.shortcuts import render
from .forms import FormServico
from django.http import HttpResponse
# Create your views here.
def novo_servico(request):
    if request.method == 'GET':
        form = FormServico()
        ctx = {'form': form}
        return render(request, 'novo_servico.html', ctx)
    elif request.method == 'POST':
        form = FormServico(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('Salvo com sucesso')
        else:
            ctx = {'form': form}
            return render(request, 'novo_servico.html', ctx)
        