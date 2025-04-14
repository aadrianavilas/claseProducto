from typing import List,Dict,Optional,Any,Tuple
from datetime import datetime
from tabulate import tabulate
import time

class ManejarError(Exception):
    def __init__(self,mensaje):
        self.mensaje=mensaje
        super().__init__(self.mensaje)
class FechaInvalida(ManejarError):...
class PrecioInvalido(ManejarError):...
class StockInvalido(ManejarError):...
class GarantiaInvalida(ManejarError):...


class Producto:
    def __init__(self,codigo:str,nombre:str,precio:float,stock:int,tipo:Optional[str]=None,fecha_vencimiento:Optional[str]=None,garantia:Optional[int]=None):
        self.codigo=codigo
        self.nombre=nombre
        self.__precio=precio
        self.__stock=stock
        self.tipo=tipo
        self.__fecha_vencimiento=fecha_vencimiento
        self.__garantia=garantia

    def __str__(self)->str:
        return  "\n".join([
                "\nPRODUCTO",
                f"Código: '{self.codigo}'",
                f"Nombre: '{self.nombre}'",
                f"Precio: {self.precio}",
                f"Stock: {self.stock}",
                f"Tipo: '{self.tipo}'",
                f"Fecha de vencimiento: '{self.fecha_vencimiento}'",
                f"Garantia: {self.garantia}",
            ])
    
    @property
    def precio(self)->int:
        return self.__precio
    
    @precio.setter
    def precio(self,precio)->None:
        if not isinstance(precio,float):
            raise PrecioInvalido('Precio no válido')
        if precio<0:
            raise PrecioInvalido('El precio no puede ser negativo')
        self.__precio=precio

    @property
    def stock(self)->int:
        return self.__stock
    
    @stock.setter
    def stock(self,stock)->None:
        if stock<0:
            raise StockInvalido('El stock no puede ser negativo')
        self.__stock=stock

    @property
    def fecha_vencimiento(self)->str:
        return self.__fecha_vencimiento
    
    @fecha_vencimiento.setter
    def fecha_vencimiento(self,fecha_vencimiento)->None:
        if not isinstance(fecha_vencimiento,str):
                raise FechaInvalida('La fecha debe ser texto')
                
        try:          
            if fecha_vencimiento.lower()=="sin fecha vencimiento":
                pass
            else:
                datetime.strptime(fecha_vencimiento,'%d/%m/%Y')
        except ValueError:
            raise ManejarError('Formato de fecha no válido. Usa DD/MM/AAAA.')

        self.__fecha_vencimiento=fecha_vencimiento

    @property
    def garantia(self)->int:
        return self.__garantia
    
    @garantia.setter
    def garantia(self,garantia)->None:
        if garantia<0:
            raise GarantiaInvalida('La garantia no puede ser negativo')
        self.__garantia=garantia
    
if __name__ == "__main__":
    productos_guardados:List[Producto]=[]
    lista:List[Tuple[Any]]=[]
    
    def calcular_tiempo(funcion):
        def wrapper(*args)->Any:
            inicio=time.time()
            result=funcion(*args)
            fin=time.time()
            print(f"El tiempo de ejecución de la funcion '{funcion.__name__}' es de: {fin-inicio:.5f} segundos")
            return result
        return wrapper

    @calcular_tiempo
    def cargar_productos(datos)->None:
        
        for item in datos:
            try:
                codigo,nombre,precio,*resto=item
                producto=Producto(codigo,nombre,precio,*resto)
                productos_guardados.append(producto)
            except ManejarError as e:
                print(f"Error al cargar el producto {nombre}: {e}")
            finally:
                continue


    def validar_descuento(funcion):
        def wrapper(*args):
            if args[0]<=0:
                raise ManejarError('El porcentaje de descuento debe ser mayor a cero')
            funcion(*args)
        return wrapper
    
    @validar_descuento
    @calcular_tiempo
    def aplicar_descuento_masivo(descuento:float)->None:
        global productos_guardados
        def aplicar_descuento(descuento:float,producto:object):
            producto.precio-=producto.precio*descuento/100
            return producto
        productos_guardados=list(map(lambda p:aplicar_descuento(descuento,p),productos_guardados))

    @calcular_tiempo
    def calcular_total_inventario()->int:
        return round(sum(list(map(lambda p: p.precio*p.stock,productos_guardados))),4)
    
    @calcular_tiempo
    def calcular_total_stock()->int:
        return sum(list(map(lambda p: p.stock,productos_guardados)))
    
    def generar_reporte(productos,total)->None:
        lista=[]
        encabezado=['Código','Nombre','Precio','Stock','Tipo','Fecha','Garantia','Total']
        for p in productos:
            *valores,=(p.codigo,p.nombre,p.precio,p.stock,p.tipo,p.fecha_vencimiento,p.garantia)
            lista.append((*valores,round(p.precio*p.stock,4)))
        lista.append(('','','','','','','Total',round(total,4)))
        print(tabulate(lista,headers=encabezado,tablefmt="pretty"))

    @calcular_tiempo
    def reporte_productos()->None:
        total=calcular_total_inventario()
        generar_reporte(productos_guardados,total)

    def productos_con_vencimiento()->None:
        productos=list(filter(lambda p: p.fecha_vencimiento.lower()!="sin fecha vencimiento",productos_guardados))
        if not productos:
            raise ManejarError('No hay productos con ese tipo')
        total=sum(list(map(lambda p: p.precio*p.stock,productos)))
        generar_reporte(productos,total)
        
    def productos_por_tipo(tipo)->None:
        if not isinstance(tipo,str):
            raise ManejarError('El tipo debe ser texto')
        productos=list(filter(lambda p: p.tipo.lower()==tipo.lower(),productos_guardados))
        if not productos:
            raise ManejarError('No hay productos con ese tipo')
        total=sum(list(map(lambda p: p.precio*p.stock,productos)))
        generar_reporte(productos,total)


    try:
        #datos de los productos a instanciar
        datos=[
            ('1','Producto1',15.50,20,'Tipo1',"12/12/2025",1),
            ('2','Producto2',253.34,30,'Tipo2','Sin fecha Vencimiento',1),
            ('3','Producto3',434.67,20,'Tipo1','Sin fecha Vencimiento',1),
            ('4','Producto4',2302.10,15,'Tipo3','Sin fecha Vencimiento',1),
            ('5','Producto5',20.99,20,'Tipo1','13/02/2026',1)
        ]
        
        cargar_productos(datos)

        #print(f"El total de inventario es: {calcular_total_inventario()}")
        #print(f"El total de stock es: {calcular_total_stock()}")
        
        # aplicar_descuento_masivo(50)

        reporte_productos()
        #productos_con_vencimiento()
        #productos_por_tipo("Tipo1")


        

    except ManejarError as e:
        print(f"Error: {e}")
