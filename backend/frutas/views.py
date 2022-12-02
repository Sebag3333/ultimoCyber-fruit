import datetime
from django.shortcuts import render

# import view sets from the REST framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# import the TodoSerializer from the serializer file
from .serializers import CarroSerializer, ContratoSerializer, OfertaSerializer, PedidoSerializer, PeticionSerializer, SubastaSerializer, UsuarioSerializer,FrutaSerializer, VentaSerializer
from django.db.models import Q, F,Count  
# import the Todo model from the models file
from .models import Carro, Contrato, Fruta, Ofertaproductor, Pedido, Peticion, Stocktienda, Subastatransportista, Usuario, Venta, Venta_interna
  
# create a class for the Todo model viewsets
class UsuarioView(viewsets.ModelViewSet):
  
    # create a sereializer class and 
    # assign it to the TodoSerializer class
    serializer_class = UsuarioSerializer
  
    # define a variable and populate it 
    # with the Todo list objects
    queryset = Usuario.objects.all()

@ api_view(['POST'])
def login(request):
    if request.method == 'POST':
        rut= request.data.get('usu_rut')
        rut = request.data["usu_rut"]
        rut = rut.replace("-","")
        rut = rut.replace(".","")
        rut = rut.lower()
        
        contraseña= request.data.get('usu_contraseña')
        usu = Usuario.objects.filter(usu_rut= rut).first()
        if usu!= None:
            if usu.usu_password ==contraseña:
                return Response({'cargo' :usu.usu_rol,'estado':1,'rut':usu.usu_rut,"nombre":usu.usu_nombre,"usu_id":usu.usu_id})
            else:
                return Response({'cargo' :usu.usu_rol,'estado':2})
        else:
            return Response({'estado':3}) 


@ api_view(['POST'])
def crear_producto(request):
    if request.method == 'POST':
        nombre =request.data["fruta_nombre"]
        cantidad =request.data["fruta_cantidad"]
        fruit = Fruta.objects.filter(fruta_nombre= nombre,fruta_pedido=None,fruta_carro=None,fruta_ofertaproductor=None).first()
        if fruit is None:
            serializer = FrutaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
            else:   
                print(serializer.errors)
                return Response(status=400)     
        else:   
            fruit.fruta_cantidad= fruit.fruta_cantidad+ int(cantidad)
            fruit.save() 
            return Response(status=200)    

@ api_view(['POST'])
def crear_fruta(request):
    if request.method == 'POST':
        elid=request.data["fruta_pedido"]
        nombre=request.data["fruta_nombre"]
        cantidad=request.data["fruta_cantidad"]
        yaexiste=0
        fruta =Fruta.objects.filter(fruta_pedido=elid,fruta_nombre=nombre).first()
        if fruta is not None:
            fruta.fruta_cantidad= fruta.fruta_cantidad+   int(cantidad) 
            fruta.save()
            return Response(status=200)
        else:          
            serializer = FrutaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
       

@ api_view(['POST'])
def Crear_oferta(request):
    if request.method == 'POST':
        request.data["oferta_fecha"]=datetime.datetime.now()
        serializer = OfertaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:   
            print(serializer.errors)
            return Response(status=400)

@ api_view(['POST'])
def crear_subasta(request):
    if request.method == 'POST':
        serializer = SubastaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:   
            print(serializer.errors)
            return Response(status=400)                  
       
@ api_view(['POST'])
def crear_venta(request):
    if request.method == 'POST':
        
        id_pedido =request.data["venta_pedido"]
        pedido= Pedido.objects.filter(pedido_id=id_pedido).first()
        frutitas = Fruta.objects.all().filter(fruta_pedido=pedido.pedido_id)
        cantidad= 0
        for s in frutitas:  
            cantidad= cantidad + s.fruta_cantidad
        request.data["venta_capacidad_carga"]= cantidad
        if cantidad >0:
            request.data["venta_tamano"]= 1
        if cantidad >4000:
            request.data["venta_tamano"]= 2 
        if cantidad >10000:
            request.data["venta_tamano"]= 3      
        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:   
            print(serializer.errors)
            return Response(status=400)    

@ api_view(['POST'])
def crear_Usuario(request):
    if request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:   
            print(serializer.errors)
 
            return Response(status=400) 


@ api_view(['POST'])
def crear_peticion(request):
    if request.method == 'POST':
        serializer = PeticionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:   
            print(serializer.errors)
 
            return Response(status=400) 



@ api_view(['POST'])
def crear_carro_por_usuario(request):
    if request.method == 'POST':
        usu =request.data["carro_usuario"]
        carrito = Carro.objects.filter(carro_usuario= usu,carro_estado="En creacion").first()
        if carrito is None:
            serializer = CarroSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'id' :serializer.data["carro_id"]})
            else:   
                print(serializer.errors)
 
                return Response(status=400) 

        else:
            return Response({'id' :carrito.carro_id}) 


@ api_view(['POST'])
def Pasar_carro_a_venta(request):
    if request.method == 'POST':
        usu =request.data["carro_usuario"]
        carrito = Carro.objects.filter(carro_usuario= usu,carro_estado="En creacion").first()
        carrito.carro_estado="Pagado"
        carrito.save()
        monto=0
        queryset = Fruta.objects.all().filter(fruta_carro=carrito.carro_id)
        for x in queryset:
            monto= monto +(x.fruta_precio * x.fruta_cantidad)
        f = Venta_interna(venta_carro=carrito,venta_monto=monto,venta_estado=0,venta_fecha=datetime.datetime.now())
        f.save()
 
        return Response(status=200) 

       




@ api_view(['POST'])
def crear_productovacio_por_usuario(request):
    if request.method == 'POST':
        usu =request.data["pedido_usuario"]
        pedido = Pedido.objects.filter(pedido_usuario= usu,pedido_estado="En creacion").first()
        if pedido is None:
            serializer = PedidoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'id' :serializer.data["pedido_id"]})
            else:   
                print(serializer.errors)
 
                return Response(status=400) 

        else:
            return Response({'id' :pedido.pedido_id}) 

@ api_view(['PATCH'])
def crear_pedido(request):
    if request.method == 'PATCH':
        id= request.data.get('pedido_id')
        
        pedido= Pedido.objects.all().filter(pedido_id= id).first()
          
        serializer = PedidoSerializer(pedido, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200) 

        else:
             return Response(status=400)           

@ api_view(['GET'])
def pedidos(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Pedido.objects.all().values("pedido_id","pedido_direccion","pedido_fecha","pedido_estado",usuario_rut=F("pedido_usuario__usu_rut")).filter(~Q(pedido_estado="En creacion")).order_by('pedido_id')
        respuesta["datos"]=queryset
        return Response(respuesta)

@ api_view(['GET'])
def ventas(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Venta.objects.all().values('venta_id','venta_pedido','venta_tamano', 'venta_capacidad_carga', 'venta_refrigeracion').order_by('venta_id')
        respuesta["datos"]=queryset
        return Response(respuesta)        

@ api_view(['GET'])
def peticiones(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Peticion.objects.all().values('peticion_id','peticion_nombre','peticion_telefono', 'peticion_descripcion').order_by('peticion_id')
        respuesta["datos"]=queryset
        return Response(respuesta)  

@ api_view(['GET'])
def miscompras(request):
    if request.method == 'GET':
        respuesta = {}
        usu = request.GET.get('usu_rut')
        queryset = Venta_interna.objects.all().values('venta_id','venta_carro','venta_estado','venta_monto','venta_fecha').filter(venta_carro__carro_usuario__usu_id=usu).order_by('venta_id')
        respuesta["datos"]=queryset
        return Response(respuesta)   


@ api_view(['GET'])
def compras(request):
    if request.method == 'GET':
        respuesta = {}
        queryset = Venta_interna.objects.all().values('venta_id','venta_carro','venta_estado','venta_monto','venta_fecha',usuario_rut=F("venta_carro__carro_usuario__usu_rut"),usuario_nombre=F("venta_carro__carro_usuario__usu_nombre")).order_by('venta_id')
        respuesta["datos"]=queryset
        return Response(respuesta)   




@ api_view(['GET'])
def subastas_segun_transportista(request):
    if request.method == 'GET':
        respuesta = {}
        usu = request.GET.get('usu_rut')
        queryset = Subastatransportista.objects.all().filter(subasta_transportista=usu).values('subasta_id','subasta_venta','subasta_valor', 'subasta_transportista', 'subasta_estado').order_by('subasta_id')
        respuesta["datos"]=queryset
        return Response(respuesta)        

@ api_view(['GET'])
def ventas_con_sus_respectivas_subastas(request):
    if request.method == 'GET':
        respuesta = {}
        queryset = Venta.objects.all().values('venta_id','venta_pedido','venta_tamano', 'venta_capacidad_carga', 'venta_refrigeracion').order_by('venta_id')
        respuesta["datos"]=queryset
        return Response(respuesta)        

@ api_view(['GET'])
def stocktienda(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Stocktienda.objects.all().values("stock_id","stock_nombre_fruta","stock_cantidad","stock_precio").order_by('stock_id')
        respuesta["datos"]=queryset
        return Response(respuesta)

@ api_view(['GET'])
def stocktienda_por_nombre(request):
    if request.method == 'GET':
        respuesta = {}
        nombre = request.GET.get('nombre')
        queryset = Stocktienda.objects.all().values("stock_id","stock_nombre_fruta","stock_cantidad","stock_precio").order_by('stock_id').filter(stock_nombre_fruta__icontains=nombre)
        respuesta["datos"]=queryset
        return Response(respuesta)

@ api_view(['GET'])
def pedidos_por_usuario(request):
    if request.method == 'GET':
        respuesta = {}
        usu = request.GET.get('usu_rut')
        queryset = Pedido.objects.all().values("pedido_id","pedido_direccion","pedido_fecha","pedido_estado").filter(~Q(pedido_estado="En creacion"),pedido_usuario=usu).order_by('pedido_id')
        respuesta["datos"]=queryset
        return Response(respuesta)




@ api_view(['GET'])
def pedidos_publicados(request):
    if request.method == 'GET':
        respuesta = {}
        queryset = Pedido.objects.all().values("pedido_id","pedido_direccion","pedido_fecha","pedido_estado",usuario_rut=F("pedido_usuario__usu_rut"),usuario_nombre=F("pedido_usuario__usu_nombre")).filter(pedido_estado="Publicado").order_by('pedido_id')
        respuesta["datos"]=queryset
        return Response(respuesta)


@ api_view(['GET'])
def frutas(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Fruta.objects.all().values("fruta_id","fruta_nombre","fruta_cantidad").order_by('fruta_id').filter(fruta_pedido=None,fruta_carro=None,fruta_ofertaproductor=None)
        respuesta["datos"]=queryset
        return Response(respuesta)

@ api_view(['GET'])
def usuarios(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Usuario.objects.all().values('usu_id','usu_email',"usu_telefono",'usu_rut','usu_password','usu_rol','usu_nombre','usu_apellidop','usu_apellidom').order_by('usu_id')
        respuesta["datos"]=queryset
        return Response(respuesta)

@ api_view(['GET'])
def contratos(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Contrato.objects.all().values('contrato_id', 'contrato_usuario', 'contrato_sueldo', 'contrato_estado', 'contrato_fecha_i', 'contrato_fecha_t',usuario_rut=F("contrato_usuario__usu_rut")).order_by('contrato_id')
        respuesta["datos"]=queryset
        return Response(respuesta)



@ api_view(['PATCH'])
def frutas_por_id_pedido(request):
    if request.method == 'PATCH':
        respuesta = {}
        elid= request.data.get('id')
        queryset = Fruta.objects.all().values("fruta_id","fruta_nombre","fruta_cantidad","fruta_precio").order_by('fruta_id').filter(fruta_pedido=elid)
        respuesta["datos"]=queryset
        return Response(respuesta)

@ api_view(['GET'])
def frutas_por_id_carro(request):
    if request.method == 'GET':
        respuesta = {}
        elid= request.GET.get('id')
        queryset = Fruta.objects.all().values("fruta_id","fruta_nombre","fruta_cantidad","fruta_precio").order_by('fruta_id').filter(fruta_carro=elid)
        respuesta["datos"]=queryset
        return Response(respuesta)        


@ api_view(['GET'])
def subastasdelaventa(request):
    if request.method == 'GET':
        respuesta = {}
        elid= request.GET.get('id')
        queryset = Subastatransportista.objects.all().values("subasta_id","subasta_venta","subasta_valor","subasta_transportista","subasta_estado",nombretransportista=F("subasta_transportista__usu_nombre"),ruttransportista=F("subasta_transportista__usu_rut")).order_by('subasta_id').filter(subasta_venta=elid)
        respuesta["datos"]=queryset
        return Response(respuesta)  

@ api_view(['GET'])
def fruta_por_id_fruta(request):
    if request.method == 'GET':
        respuesta = {}
        elid= request.GET.get('fruta_id')
        queryset = Fruta.objects.values('fruta_id','fruta_nombre','fruta_cantidad','fruta_pedido','fruta_carro','fruta_precio').filter(fruta_id=elid).first()
        respuesta["datos"]=queryset
        return Response(respuesta)   


@ api_view(['GET'])
def verificar_esta_lista_la_oferta(request):
    if request.method == 'GET':
        respuesta = {}
        elid= request.GET.get('fruta_id')
        totalcantidad=0
        totalprecio=0
        totalfinal=0
        listo=0
        queryset = Ofertaproductor.objects.filter(oferta_fruta__fruta_id=elid,oferta_estado="Seleccionado").all()
        for x in queryset:
            totalcantidad=totalcantidad+x.oferta_cantidad
            totalprecio=totalprecio+x.oferta_monto
        queryset2 = Fruta.objects.filter(fruta_id=elid).first()
        if queryset.count()>0:
            totalfinal=(totalprecio/totalcantidad)*queryset2.fruta_cantidad
        if totalcantidad>= queryset2.fruta_cantidad:
            listo=1
            queryset2.fruta_precio=totalfinal
            queryset2.save()
        else:
            queryset2.fruta_precio=None
            queryset2.save()      
        respuesta["listo"]=listo
        return Response(respuesta)   

@ api_view(['GET'])
def ofertas_por_fruta(request):
    if request.method == 'GET':
        respuesta = {}
        elid= request.GET.get('fruta_id')
        queryset = Ofertaproductor.objects.all().values('oferta_id','oferta_estado','oferta_fecha', 'oferta_usuario', 'oferta_fruta','oferta_monto','oferta_cantidad',fruta_nombre=F("oferta_fruta__fruta_nombre"),nombre_usuario=F("oferta_usuario__usu_nombre"),rut_usuario=F("oferta_usuario__usu_rut")).order_by('oferta_id').filter(oferta_fruta=elid)
        respuesta["datos"]=queryset
        return Response(respuesta)   

@ api_view(['GET'])
def Ofertas_por_productor(request):
    if request.method == 'GET':
        respuesta = {}
        usu = request.GET.get('usu_rut')
        queryset = Ofertaproductor.objects.all().values(pedido_id=F("oferta_fruta__fruta_pedido"),pedido_direccion=F("oferta_fruta__fruta_pedido__pedido_direccion"),pedido_estado=F("oferta_fruta__fruta_pedido__pedido_estado"),pedido_usuario_rut=F("oferta_fruta__fruta_pedido__pedido_usuario__usu_rut")).annotate(dcount=Count('oferta_fruta__fruta_pedido')).order_by().filter(oferta_usuario=usu)
        respuesta["datos"]=queryset
        return Response(respuesta)   

@ api_view(['GET'])
def detalle_Ofertas_por_productor(request):
    if request.method == 'GET':
        respuesta = {}
        usu = request.GET.get('usu_rut')
        pedi_id = request.GET.get('pedido_id')
        queryset = Ofertaproductor.objects.all().values('oferta_id','oferta_estado','oferta_fecha', 'oferta_usuario','oferta_cantidad', 'oferta_fruta','oferta_monto',fruta_nombre=F("oferta_fruta__fruta_nombre"),fruta_cantidad=F("oferta_fruta__fruta_cantidad")).order_by('oferta_id').filter(oferta_usuario=usu,oferta_fruta__fruta_pedido=pedi_id)
        respuesta["datos"]=queryset
        return Response(respuesta)   

@ api_view(['GET'])
def verificar_pedido_tiene_transportes(request):
    if request.method == 'GET':
        respuesta = {}
        pedi_id = request.GET.get('pedido_id')
        queryset = ""
        total = 0
        venta = Venta.objects.filter(venta_pedido= pedi_id).first()
        if venta is not None:
            queryset = Subastatransportista.objects.all().values('subasta_id','subasta_venta','subasta_valor',nombre_transportista=F('subasta_transportista__usu_nombre')).order_by('subasta_id').filter(subasta_venta=venta.venta_id,subasta_estado='Seleccionado').first()
            total = Subastatransportista.objects.all().order_by('subasta_id').filter(subasta_venta=venta.venta_id,subasta_estado='Seleccionado').count()
           
        respuesta["datos"]=queryset
        respuesta["cantidad"]=total
        return Response(respuesta)  


@ api_view(['GET'])
def verificar_venta_ya_tiene_transportista(request):
    if request.method == 'GET':
        respuesta = {}
        pedi_id = request.GET.get('id_venta')
        total = 0
        subs = Subastatransportista.objects.filter(subasta_venta= pedi_id,subasta_estado='Seleccionado').first()
        if subs is not None:
            total=1
        respuesta["existe"]=total
        return Response(respuesta)  



@ api_view(['PATCH'])
def actualizar_nombre_fruta(request):
    if request.method == 'PATCH':
        elid= request.data.get('id')
        nombre= request.data.get('nombre')
        fruit= Fruta.objects.all().filter(fruta_id= elid).first()
        serializer = FrutaSerializer(fruit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200) 

        else:
             return Response(status=400) 


@ api_view(['PATCH'])
def actualizar_subasta(request):
    if request.method == 'PATCH':
        elid= request.data.get('id')
        fruit= Subastatransportista.objects.filter(subasta_id= elid).first()
        serializer = SubastaSerializer(fruit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200) 

        else:
             return Response(status=400) 

@ api_view(['PATCH'])
def publcar_pedido(request):
    if request.method == 'PATCH':
        elid= request.data.get('id')
        ped= Pedido.objects.all().filter(pedido_id= elid).first()
        serializer = PedidoSerializer(ped, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200) 

        else:
             return Response(status=400) 


@ api_view(['POST'])
def crear_fruta_Carro(request):
    if request.method == 'POST':
        nombre =request.data["fruta_nombre"]
        carro =request.data["fruta_carro"]
        fruit= Fruta.objects.all().filter(fruta_nombre= nombre,fruta_carro=carro).first()
        if fruit is None:
            serializer = FrutaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=200)
        else:
            fruit.fruta_cantidad=fruit.fruta_cantidad+1
            fruit.save()
            return Response(status=200) 

@ api_view(['GET'])
def pedidos_todos(request):
    if request.method == 'GET':
        respuesta = {}
        
        queryset = Fruta.objects.all().values("fruta_id","fruta_nombre","fruta_cantidad").order_by('fruta_id')
        respuesta["datos"]=queryset
        return Response(respuesta)           


@ api_view(['DELETE'])
def borrar_producto(request):
    if request.method == 'DELETE':
        elid= request.data.get('id_producto')
       
        ped= Fruta.objects.filter(fruta_id = elid).first()
        if ped is not None:
            ped.delete()
            return Response(status=200)
        else:
            return Response(status=400)  


@ api_view(['DELETE'])
def borrar_pedidos(request):
    if request.method == 'DELETE':
        elid= request.data.get('pedido_id')
       
        ped= Pedido.objects.filter(pedido_id = elid).first()
        if ped is not None:
            ped.delete()
            return Response(status=200)
        else:
            return Response(status=400)  


def borrar_pedido(request):
    
        ped= Venta.objects.filter(venta_id = 2).first()
        ped.delete()
        return Response(status=200)

def ingresar_stock(request):
    
        ped= Stocktienda(stock_nombre_fruta='Melon C.',stock_cantidad=8000,stock_precio=2850)
    
       
        ped.save()
        return Response(status=200)        
    
def ingresar_subasta(request):
        pventa= Venta.objects.filter(venta_id = 1).first()
        puser= Usuario.objects.filter(usu_id = 7).first()
        ped= Subastatransportista(subasta_venta=pventa,subasta_valor=74500,subasta_transportista=puser,subasta_estado="Postulado")
    
       
        ped.save()
        return Response(status=200)


def vaciar_base_de_datos(request):
       ped= Subastatransportista.objects.all()
       ped.delete()
       ped= Venta.objects.all()
       ped.delete()
       ped= Ofertaproductor.objects.all()
       ped.delete()
       ped= Fruta.objects.all()
       ped.delete()
       ped= Carro.objects.all()
       ped.delete()
       ped= Pedido.objects.all()
       ped.delete()
       return Response(status=200)                

@ api_view(['DELETE'])
def disminuir_producto(request):
    if request.method == 'DELETE':
        elid= request.data.get('id_producto')
        ped= Fruta.objects.filter(fruta_id = elid).first()
        if ped.fruta_cantidad==1:
            ped.delete()
            return Response(status=200)
        else :
            ped.fruta_cantidad= ped.fruta_cantidad-1  
            ped.save()  
            return Response(status=200)                                              
# cosas del edgar -------------------------------------------------------


@ api_view(['GET'])
def verificarcontrato(request):
    if request.method == 'GET':
        respuesta = {}
        rut = request.GET.get('contrato_rut')
        contrato1 = Contrato.objects.filter(contrato_rut=rut).first()
        existe=0
        if contrato1 is not None:
            existe=1
    
        return Response({'existe' :existe})










@ api_view(['GET'])
def pedido_por_id_pedido(request):
    if request.method == 'GET':
        respuesta = {}
        elid = request.GET.get('id_pedido')
        queryset = Pedido.objects.values('pedido_id','pedido_fecha','pedido_direccion','pedido_usuario','pedido_estado').filter(pedido_id=elid).first()

        respuesta["datos"]=queryset
        return Response(respuesta)  


@ api_view(['GET'])
def verificarusuario(request):
    if request.method == 'GET':
        respuesta = {}
        rut = request.GET.get('usu_rut')
        usuario1 = Usuario.objects.filter(usu_rut=rut).first()
        existe=0
        if usuario1 is not None:
            existe=1
    
        return Response({'existe' :existe})



@ api_view(['GET'])
def verificaryasubastaste(request):
    if request.method == 'GET':
        respuesta = {}
        rut = request.GET.get('usu_rut')
        idventa = request.GET.get('id_venta')
        usuario1 = Subastatransportista.objects.filter(subasta_transportista=rut,subasta_venta=idventa).first()
        existe=0
        if usuario1 is not None:
            existe=1
    
        return Response({'existe' :existe})  

@ api_view(['GET'])
def verificaryaofertaste(request):
    if request.method == 'GET':
        respuesta = {}
        rut = request.GET.get('usu_rut')
        usuario1 = Ofertaproductor.objects.all().filter(oferta_usuario=rut).values('oferta_id','oferta_estado','oferta_fecha', 'oferta_usuario', 'oferta_fruta','oferta_monto')
        existe=0
        if usuario1 is not None:
            respuesta["datos"]=usuario1
            return Response(respuesta)
    
        else:
            return Response(status=400)            

@ api_view(['PATCH'])
def actualizar_usuario(request):
    if request.method == 'PATCH':
        elid= request.data.get('usu_rut')
        Usu= Usuario.objects.all().filter(usu_rut= elid).first()
        serializer = UsuarioSerializer(Usu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200) 

        else:
             return Response(status=400) 


@ api_view(['GET'])
def buscar_usuario(request):
    if request.method == 'GET':
        respuesta = {}
        rut = request.GET.get('usu_rut')
        usuario1 = Usuario.objects.filter(usu_rut=rut).values('usu_id','usu_email',"usu_telefono",'usu_rut','usu_password','usu_rol','usu_nombre','usu_apellidop','usu_apellidom').first()
        existe=0
        if usuario1 is not None:
            respuesta["datos"]=usuario1
            return Response(respuesta)
        else:
            return Response(status=400) 
        
       

@ api_view(['DELETE'])
def borrar_usuario(request):
    if request.method == 'DELETE':
        elid= request.data.get('rut')
       
        ped= Usuario.objects.filter(usu_rut = elid).first()
        if ped is not None:
            ped.delete()
            return Response(status=200)
        else:
            return Response(status=400)              

@ api_view(['GET'])
def verificar_contrato(request):
    if request.method == 'GET':
        respuesta = {}
        rut = request.GET.get('contrato_rut')
        contrato1 = Contrato.objects.filter(contrato_rut=rut).first()
        existe=0
        if contrato1 is not None:
            existe=1
    
        return Response({'existe' :existe})

         




@ api_view(['GET'])
def pedido_segun_venta(request):
    if request.method == 'GET':
        respuesta = {}
        elid = request.GET.get('id_venta')
        vent = Venta.objects.filter(venta_id=elid).first()
        Ped = Pedido.objects.filter(pedido_id=vent.venta_pedido.pedido_id).values('pedido_id','pedido_fecha','pedido_direccion','pedido_usuario','pedido_estado').first()
        existe=0
        if Ped is not None:
            respuesta["datos"]=Ped
            return Response(respuesta)
        else:
            return Response(status=400) 


@ api_view(['POST'])
def crear_contrato(request):
    if request.method == 'POST':
        serializer = ContratoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:   
            print(serializer.errors)
 
            return Response(status=400)             

@ api_view(['PATCH'])
def actualizar_contrato(request):
    if request.method == 'PATCH':
        elid= request.data.get('contrato_id')
        cont= Contrato.objects.all().filter(contrato_id= elid).first()
        serializer = ContratoSerializer(cont, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200) 

        else:
             return Response(status=400) 


@ api_view(['PATCH'])
def actualizar_oferta(request):
    if request.method == 'PATCH':
        elid= request.data.get('ofert_id')
        cont= Ofertaproductor.objects.filter(oferta_id= elid).first()
        serializer = OfertaSerializer(cont, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200) 

        else:
             return Response(status=400) 



@ api_view(['GET'])
def buscar_contrato(request):
    if request.method == 'GET':
        respuesta = {}
        rut = request.GET.get('contrato_rut')
        contrato1 = Contrato.objects.filter(contrato_rut=rut).values().first()
        existe=0
        if contrato1 is not None:
            respuesta["datos"]=contrato1
            return Response(respuesta)
        else:
            return Response(status=400) 

@ api_view(['DELETE'])
def borrar_contrato(request):
    if request.method == 'DELETE':
        elid= request.data.get('contrato_rut')
       
        ped= Contrato.objects.filter(contrato_rut = elid).first()
        if ped is not None:
            ped.delete()
            return Response(status=200)
        else:
            return Response(status=400)      

@ api_view(['DELETE'])
def borrar_contrato2(request):
    if request.method == 'DELETE':
        elid= request.data.get('contrato_id')
       
        ped= Contrato.objects.filter(contrato_id = elid).first()
        if ped is not None:
            ped.delete()
            return Response(status=200)
        else:
            return Response(status=400)      

@ api_view(['DELETE'])
def borrar_oferta(request):
    if request.method == 'DELETE':
        elid= request.data.get('id')
       
        ped= Ofertaproductor.objects.filter(oferta_fruta__fruta_id = elid).first()
        if ped is not None:
            ped.delete()
            return Response(status=200)
        else:
            return Response(status=400)               

       