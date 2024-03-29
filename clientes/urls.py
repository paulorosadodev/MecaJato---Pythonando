from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('atualiza_cliente/', views.att_cliente, name="atualiza_cliente"),
    path('update_carro/<int:id>', views.att_carro, name="atualiza_carro"),
    path('excluir_carro/<int:id>', views.dlt_carro, name="deleta_carro"),
    path('update_cliente/<int:id>', views.update_cliente, name="atualiza_cliente"),
]