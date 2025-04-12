from typing import List,Dict,Any,Optional
from manage_error import ManageError
import time

productos_guardados: List[Dict[str, Any]] = []

class ManageError(Exception):
    def __init__(self,message:str)->None:
        self.message=message
        super().__init__(self.message)

    
class Producto:   
    def __init__(self,codigo:str,nombre:str,precio:str,stock:int,categoria:str,tipo:Optional[str]=None,fecha_vencimiento:Optional[str]=None,garantia:Optional[int]=None)->None:
        self.codigo=codigo
        self.nombre=nombre
        self.__precio=precio
        self.__stock=stock
        self.categoria=categoria
        self.tipo=tipo
        self._fecha_vencimiento=fecha_vencimiento
        self._garantia=garantia
    
    def validar_precio(funcion):
        def wrapper(self,precio:float)->None:
            try:
                if not isinstance(precio, float):
                    raise ManageError('Precio no válido')
                if precio<=0:
                    raise ManageError('El precio debe ser mayor a cero')
                
                funcion(self,precio)
            except ManageError as e:
                print(f"Error: {e}")
        return wrapper
    

    @property
    def precio(self)->float:
        return self.__precio
    
    @precio.setter
    @validar_precio
    def precio(self,precio:float)->None:
        self.__precio=precio


    def validar_stock(funcion):
        def wrapper(self,stock:int)->None:
            try:
                if stock<=0:
                    raise ManageError('El stock debe ser mayor a cero')
                funcion(self,stock)
            except ManageError as e:
                print(f"Error: {e}")
        return wrapper


    @property
    def stock(self)->int:
        return self.__stock
    
    @stock.setter
    @validar_stock
    def stock(self,stock:int)->None:
        self.__stock=stock

    def validar_garantia(funcion):
        def wrapper(self,garantia:int)->None:
            try:
                if garantia<0:
                    raise ManageError('La garantia debe ser mayor o igual a cero')
                funcion(self,garantia)
            except ManageError as e:
                print(f"Error: {e}")
        return wrapper
    
    @property
    def garantia(self)->int:
        return self._garantia
    
    @garantia.setter
    @validar_garantia
    def garantia(self,garantia:int)->None:
        self._garantia=garantia
    
    def validar_descuento(funcion)->List[Dict[str,Any]]:
        def wrapper(self,descuento:float)->None:
            try:
                if descuento<=0:
                    raise ManageError('El porcentaje de descuento debe ser mayor a cero')
                resultado=funcion(self,descuento)
                return resultado
            except ManageError as e:
                print(f"Error: {e}")
        return wrapper
    
    def tiempo_ejecucion(funcion):
        def wrapper(*args,**kargs)->Any:
            inicio=time.time()
            resultado=funcion(*args,**kargs)
            fin=time.time()
            print(f"Tiempo de ejecución de la función '{funcion.__name__}': {fin-inicio:.4f} segundos")
            return resultado
        return wrapper
    
    @validar_descuento
    @tiempo_ejecucion
    def aplicar_descuento(self,descuento:float)->List[Dict[str,Any]]:
        global productos_guardados
        productos_descuento=list(map(lambda producto:{**producto,'precio':producto['precio']-(producto['precio']*descuento/100)},productos_guardados))
        productos_guardados=productos_descuento
        return productos_guardados

    @tiempo_ejecucion
    def total_inventario(self)->List[Any]:
        #total_productos=[producto['precio']*producto['stock'] for producto in productos_guardados]
        total_productos=list(map(lambda producto:producto['precio']*producto['stock'],productos_guardados))
        return sum(total_productos)

    def agregar_producto(self,objeto)->None:
        producto={
            'codigo':objeto.codigo,
            'nombre':objeto.nombre,
            'precio':objeto.precio,
            'stock':objeto.stock,
            'categoria':objeto.categoria,
            'tipo':objeto.tipo,
            'garantia':objeto.garantia
        }
        productos_guardados.append(producto)
    
    

productos=[
            ('1231','Producto1',150.50,20,'Categoria1','Tipo1',2),
            ('1232','Producto2',230.32,20,'Categoria2','Tipo2',1),
            ('1233','Producto3',750.23,20,'Categoria3','Tipo3',1),
            ('1234','Producto4',350.43,20,'Categoria4','Tipo4',2),
            ('1235','Producto5',1239.46,20,'Categoria5','Tipo5',2)
          ]

for producto in productos:
     producto=Producto(*producto)
     producto.agregar_producto(producto)


print(producto.aplicar_descuento(50))
print(producto.total_inventario())



