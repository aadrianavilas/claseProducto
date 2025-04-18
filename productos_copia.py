from typing import List,Dict,Any,Tuple
from datetime import datetime
from inventario import ManageInventory
from manage_error import ManageError,InvalidDate,InvalidPrice,InvalidStock,InvalidWarranty
from manage_file import ManageFile
import json


class Product:
    def __init__(self,code:str,name:str,price:float,stock:int,product_type:str | None=None,expiration_date:str|None=None,warranty:int|None=None):
        self.__code=code
        self._name=name
        self.__price=price
        self.__stock=stock
        self._product_type=product_type
        self.__expiration_date=expiration_date
        self.__warranty=warranty

    
    @property
    def code(self)->str:
        return self.__code
    @property
    def name(self)->str:
        return self._name
    
    @name.setter
    def name(self,name)->None:
        if name.strip()=="":
            raise ManageError('El nombre no puede estar vacio')
        self._name=name

    @property
    def price(self)->int:
        return self.__price
    
    @price.setter
    def price(self,price)->None:
        if not isinstance(price,float):
            raise InvalidPrice('Precio no válido')
        if price<0:
            raise InvalidPrice('El precio no puede ser negativo')
        self.__price=price

    @property
    def stock(self)->int:
        return self.__stock
    
    @stock.setter
    def stock(self,stock)->None:
        if stock<0:
            raise InvalidStock('El stock no puede ser negativo')
        self.__stock=stock

    @property
    def product_type(self)->str:
        return self._product_type
    
    @product_type.setter
    def product_type(self,product_type)->None:
        if product_type.strip()=="":
            raise ManageError('El tipo del producto no puede estar vacio')
        self._product_type=product_type

    @property
    def expiration_date(self)->str:
        return self.__expiration_date
    
    @expiration_date.setter
    def expiration_date(self,expiration_date)->None:
        if not isinstance(expiration_date,str):
                raise InvalidDate('La fecha debe ser texto')
                
        try:          
            if expiration_date.lower()=="sin fecha vencimiento":
                pass
            else:
                datetime.strptime(expiration_date,'%d/%m/%Y')
        except ValueError:
            raise ManageError('Formato de fecha no válido. Usa DD/MM/AAAA.')

        self.__expiration_date=expiration_date

    @property
    def warranty(self)->int:
        return self.__warranty
    
    @warranty.setter
    def warranty(self,warranty)->None:
        if warranty<0:
            raise InvalidWarranty('La garantia no puede ser negativo')
        self.__warranty=warranty

 

    
if __name__ == "__main__":
    list_dict={'products':[]}    
    def create_dict(item)->Dict[str,Any]:
        code,name,price,stock,product_type,expiration_date,warranty=item
        list_dict['products'].append({       
                'code':code,
                'name':name,
                'price':price,
                'stock':stock,
                'product_type':product_type,
                'expiration_date':expiration_date,
                'warranty':warranty
                    })
        
    def read_data_json()->str:
        data_json=manage_file.read_data()
        return json.dumps(data_json,indent=2,ensure_ascii=False)
    
    def write_data_json():
        if manage_file.save_json(list_dict): 
            print('Archivo creado exitosamente')

    def cargar_productos(data)->None: 
        for item in data:
            try:
                code,name,price,*rest=item
                product=Product(code,name,price,*rest)
                ManageInventory.save_product(product)
                create_dict(item)
            except ManageError as e:
                print(f"Error al cargar el producto {name}: {e}")


    try:
        #datos de los productos a instanciar
        data=[
            ('1','Producto1',15.50,20,'Tipo1',"12/12/2025",1),
            ('2','Producto2',253.34,30,'Tipo2','Sin fecha Vencimiento',1),
            ('3','Producto3',434.67,20,'Tipo1','Sin fecha Vencimiento',1),
            ('4','Producto4',2302.10,15,'Tipo3','Sin fecha Vencimiento',1),
            ('5','Producto5',20.99,20,'Tipo1','13/02/2026',1)
        ]
        
        cargar_productos(data)
        # manage_file=ManageFile('products.json')
        # write_data_json()
        # print(read_data_json())
        print(f"El total de inventario es: {ManageInventory.calculate_total_inventory()}")
        print(f"El total de stock es: {ManageInventory.calculate_total_stock()}")
        
        ManageInventory.aplicate_massive_discount(50)
        

        ManageInventory.reporte_productos()
        ManageInventory.products_with_expiration()
        ManageInventory.products_to_type("Tipo1")


        

    except ManageError as e:
        print(f"Error: {e}")
