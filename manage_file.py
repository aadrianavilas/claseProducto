from interface_file import InterfaceFile
import json,os
from typing import Any, Dict

class ManageFile(InterfaceFile):
    def __init__(self,file_path):
        super().__init__(file_path)

    def save_json(self, data)->bool:
        try:
            with open(self.file_path,mode='w',encoding='utf-8') as file:
                json.dump(data,file,indent=4,ensure_ascii=False)
            return True
        except Exception as e:
            print(f'Error al cargar archivo: {e}')
            return False
        
    def read_data(self)->Dict[str,Any]:
        try:
            if self.exists_file():
                with open(self.file_path,mode='r',encoding='utf-8') as file:
                    data=json.load(file)
            return data
        except Exception as e:
            print(f'Error al leer el archivo: {e}')
            return {}
        
    def exists_file(self):
        return os.path.exists(self.file_path)
    

s=ManageFile('productos.json')
    


