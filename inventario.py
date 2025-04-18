from typing import List,Any
from tabulate import tabulate
from manage_error import ManageError
import time

class ManageInventory:
    saved_products:List[object]=[]

    @classmethod
    def save_product(cls,product:object)->None:
        cls.saved_products.append(product)
    
    @staticmethod
    def __aplicate_discount(discount:float,product:object)->object:
        product.price-=product.price*discount/100
        return product
    
    @staticmethod
    def validate_discount(funcion):
        def wrapper(*args):
            if args[1]<=0:
                raise ManageError('El porcentaje de descuento debe ser mayor a cero')
            funcion(*args)
        return wrapper
    
    @staticmethod
    def calculate_time(function):
        def wrapper(*args)->Any:
            inicio=time.time()
            result=function(*args)
            fin=time.time()
            print(f"El tiempo de ejecución de la funcion '{function.__name__}' es de: {fin-inicio:.5f} segundos")
            return result
        return wrapper
    
    @classmethod
    @validate_discount
    @calculate_time
    def aplicate_massive_discount(cls,discount:float)->None:
        cls.saved_products=list(map(lambda p:ManageInventory.__aplicate_discount(discount,p),cls.saved_products))

    @classmethod
    @calculate_time
    def calculate_total_inventory(cls)->int:
        return round(sum(list(map(lambda p: p.price*p.stock,cls.saved_products))),4)
    
    @classmethod
    @calculate_time
    def calculate_total_stock(cls)->int:
        return sum(list(map(lambda p: p.stock,cls.saved_products)))
    
    @staticmethod
    def generate_report(products:List[object],total:float)->None:
        lista=[]
        headers=['Código','Nombre','Precio','Stock','Tipo','Fecha','Garantia','Total']
        for p in products:
            *values,=(p.code,p.name,p.price,p.stock,p.product_type,p.expiration_date,p.warranty)
            lista.append((*values,round(p.price*p.stock,4)))
        lista.append(('','','','','','','Total',round(total,4)))
        print(tabulate(lista,headers=headers,tablefmt="pretty"))

    @classmethod
    @calculate_time
    def reporte_productos(cls)->None:
        total=cls.calculate_total_inventory()
        ManageInventory.generate_report(cls.saved_products,total)

    @classmethod
    @calculate_time
    def products_with_expiration(cls)->None:
        products=list(filter(lambda p: p.expiration_date.lower()!="sin fecha vencimiento",cls.saved_products))
        if not products:
            raise ManageError('No hay productos con ese tipo')
        total=sum(list(map(lambda p: p.price*p.stock,products)))
        ManageInventory.generate_report(products,total)

    @classmethod
    @calculate_time
    def products_to_type(cls,product_type:str)->None:
        if not isinstance(product_type,str):
            raise ManageError('El tipo debe ser texto')
        products=list(filter(lambda p: p.product_type.lower()==product_type.lower(),cls.saved_products))
        if not products:
            raise ManageError('No hay productos con ese tipo')
        total=sum(list(map(lambda p: p.price*p.stock,products)))
        ManageInventory.generate_report(products,total)

    
