# import sereliazers from the REST framework
from rest_framework import serializers
  
# import the todo data model
from .models import Carro, Contrato, Ofertaproductor, Pedido, Peticion, Subastatransportista, Usuario,Fruta, Venta
  
# create a sereliazer class

class UsuarioSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Usuario
        fields = ('usu_id','usu_email',"usu_telefono",'usu_rut','usu_password','usu_rol','usu_nombre','usu_apellidop','usu_apellidom')    

class FrutaSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Fruta
        fields = ('fruta_id','fruta_nombre','fruta_cantidad','fruta_pedido','fruta_carro','fruta_precio')   
class PedidoSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Pedido
        fields = ('pedido_id','pedido_fecha','pedido_direccion','pedido_usuario','pedido_estado')          
class CarroSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Carro
        fields = ('carro_id','carro_usuario','carro_estado')                   

class ContratoSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Contrato
        fields = ('contrato_id', 'contrato_usuario', 'contrato_sueldo', 'contrato_estado', 'contrato_fecha_i', 'contrato_fecha_t')           


class VentaSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Venta
        fields = ('venta_id','venta_pedido','venta_tamano', 'venta_capacidad_carga', 'venta_refrigeracion')                   

class SubastaSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Subastatransportista
        fields = ('subasta_id','subasta_venta','subasta_valor', 'subasta_transportista', 'subasta_estado')   

class OfertaSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Ofertaproductor
        fields = ('oferta_id','oferta_estado','oferta_fecha', 'oferta_usuario', 'oferta_fruta','oferta_monto','oferta_cantidad')  

class PeticionSerializer(serializers.ModelSerializer):
  
    # create a meta class
    class Meta:
        model = Peticion
        fields = ('peticion_id','peticion_nombre','peticion_telefono', 'peticion_descripcion')  

            

