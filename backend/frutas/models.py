from string import octdigits
from django.db import models
  
class Usuario(models.Model):
    usu_id  = models.BigAutoField(primary_key=True)
    usu_rut=models.CharField(max_length=100)
    usu_password=models.CharField(max_length=100)
    usu_telefono=models.CharField(max_length=100,default="None",null=True)
    usu_email=models.CharField(max_length=100,default="None",null=True)
    usu_nombre=models.CharField(max_length=100,default="None",null=True)
    usu_apellidop=models.CharField(max_length=100,default="None",null=True)
    usu_apellidom=models.CharField(max_length=100,default="None",null=True)
    usu_rol=models.IntegerField(default=False)
    
  
    # string representation of the class
    def __str__(self):

        return self.usu_rut 
class Pedido(models.Model):
    pedido_id = models.BigAutoField(primary_key=True)
    pedido_estado =models.CharField(max_length=100,default="None",null=True)
    pedido_fecha=models.DateField(null=True)
    pedido_direccion=models.CharField(max_length=100,null=True)
    pedido_usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
  
    # string representation of the class
    def __str__(self):
        return self.pedido_id      
class Carro(models.Model):
    carro_id = models.BigAutoField(primary_key=True)
    carro_usuario =models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
    carro_estado =models.CharField(max_length=100,default="None",null=True)
    # string representation of the class
    def __str__(self):
        return self.carro_id          





           
class Fruta(models.Model):
    fruta_id = models.BigAutoField(primary_key=True)
    fruta_nombre=models.CharField(max_length=100)
    fruta_cantidad=models.IntegerField(default=False)
    fruta_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE,null=True)
    fruta_carro = models.ForeignKey(Carro, on_delete=models.CASCADE,null=True)
    fruta_precio =models.IntegerField(default=False,null=True)
    # reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    # string representation of the class
    def __str__(self):
  
        #it will return the title
        return self.fruta_id 

class Ofertaproductor(models.Model):
    oferta_id = models.BigAutoField(primary_key=True)
    oferta_estado =models.CharField(max_length=100,default="None",null=True)
    oferta_fecha=models.DateTimeField(null=True)
    oferta_monto=models.IntegerField(default=False,null=True)
    oferta_cantidad=models.IntegerField(default=False,null=True)
    oferta_usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
    oferta_fruta = models.ForeignKey(Fruta, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.oferta_id            

class Stocktienda(models.Model):
    stock_id = models.BigAutoField(primary_key=True)
    stock_nombre_fruta=models.CharField(max_length=100)
    stock_cantidad=models.IntegerField(default=False,null=True)
    stock_precio =models.IntegerField(default=False,null=True)
   
    # reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    # string representation of the class
    def __str__(self):
  
        #it will return the title
        return self.stock_id         

class Contrato(models.Model):
    contrato_id = models.BigAutoField(primary_key=True)
    contrato_usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
    contrato_sueldo = models.IntegerField(default=False)
    contrato_estado = models.CharField(default=False,max_length=100)
    contrato_fecha_i = models.DateField()
    contrato_fecha_t = models.DateField()
  
    # string representation of the class
    def __str__(self):
  
        #it will return the title
        return self.id    

class Venta(models.Model):
    venta_id = models.BigAutoField(primary_key=True)
    venta_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE,null=True)
    venta_tamano =models.IntegerField(default=False,null=True)
    venta_capacidad_carga = models.IntegerField(default=False,null=True)
    venta_refrigeracion = models.CharField(default=False,max_length=100,null=True)

    def __str__(self):

        return str(self.venta_id)
class Subastatransportista(models.Model):
    subasta_id = models.BigAutoField(primary_key=True)
    subasta_venta = models.ForeignKey(Venta, on_delete=models.CASCADE,null=True)
    subasta_valor = models.IntegerField(default=False,null=True)
    subasta_transportista = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
    subasta_estado = models.CharField(default=False,max_length=100,null=True)
   

    def __str__(self):

        return str(self.subasta_id)
 
class Venta_interna(models.Model):
    venta_id = models.BigAutoField(primary_key=True)
    venta_carro = models.ForeignKey(Carro, on_delete=models.CASCADE,null=True)
    venta_estado =models.IntegerField(default=False,null=True)
    venta_monto =models.IntegerField(default=False,null=True)
    venta_fecha =models.DateTimeField(null=True)

    def __str__(self):

        return str(self.venta_id)

class Peticion(models.Model):
    peticion_id = models.BigAutoField(primary_key=True)
    peticion_nombre = models.CharField(default=False,max_length=100,null=True)
    peticion_telefono = models.CharField(default=False,max_length=100,null=True)
    peticion_descripcion = models.CharField(default=False,max_length=600,null=True)
    

    def __str__(self):
        return str(self.peticion_id)        