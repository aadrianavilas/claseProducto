from abc import ABC, abstractmethod
from typing import Dict,Any

class InterfaceFile(ABC):
    def __init__(self,file_path)->None:
        self.file_path=file_path

    @abstractmethod
    def save_json(self, data:Dict[str,Any])->bool:
         """
        Método abstracto para guardar datos en formato JSON
        Args:
            datos: Diccionario con los datos a guardar
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
         pass 

    @abstractmethod
    def read_data(self)->Dict[str,Any]:
         """
        Método abstracto para leer datos desde un archivo JSON
        Returns:
            Dict: Diccionario con los datos leídos del archivo
        """
         pass
    
    @abstractmethod
    def exists_file(self)->bool:
        """
        Método abstracto para validar si el archivo existe y es válido
        Returns:
            bool: True si el archivo es válido, False en caso contrario
        """
        pass
