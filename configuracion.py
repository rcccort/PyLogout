#!/bin/python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import toml

class Configuracion:
    
    def __init__(self, app: str, config: str, base: dict) -> None:
        '''Crea si no existen el directorio y el archivo o archivos
        de configuración para la aplicación dada...
        
        :app: Nombre de la aplicación
        :config: Nombre del archivo de configuración
        :base: configuración base
        '''
        # busca el directorio de configuración del usuario Ej. /home/usuario/.config
        self.directorio_configuracion = self.getconfigdir() 
        self.app = app
        self.config = config
        self.base = base
        # comprueba si existen el directorio y el archivo
        self.comprobar(self.app, self.config)
        
    def comprobar(self, directorio: str, archivo: str) -> None:
        config_dir = Path(self.directorio_configuracion) / directorio # ruta directorio configuración
        if not config_dir.exists(): # si no existe lo crea
            os.makedirs(config_dir) 
        config_file = config_dir / archivo #ruta archivo de configuración
        if not config_file.exists(): # si no existe lo crea con los datos dados
            self.escribir_datos(self.base)
    
    def read_conf(self) -> dict:
        ''' devuelve un diccionario con la configuración del archivo'''
        config_dir = Path(self.directorio_configuracion) / self.app
        config_file = config_dir / self.config
        idata = toml.load(config_file)
        return idata
    
    def escribir_datos(self, idato: dict) -> None:
        ''' escribe la configuración dada en idato en el archivo de configuración'''
        config_file = Path(self.directorio_configuracion) / self.app / self.config
        with open(config_file, 'w') as fw:
            toml.dump(idato, fw)
    
    def getconfigdir(self):
        ''' busca el directorio de configuración del usuario Ej. /home/usuario/.config'''
        if 'XDG_CONFIG_HOME' in os.environ:
            return os.environ['XDG_CONFIG_HOME']
        else:
            return Path.home() / '.config'
        
    def get_dir(self) -> Path:
        ''' devuelve la ruta del directorio de configuración'''
        return Path(self.directorio_configuracion) / self.app

## Ejemplo de modo de uso ##

#if __name__ == '__main__':
#    
#    APP = "pelisdb"
#    config = f"{APP}.conf"
#    
#    conf = Configuracion(APP, config)  
#    
#    #datos2 = conf.read_conf()
#    #datos2["ultimo_lugar"] = "Carpeta 1"
#    #
#    #conf.escribir_datos(datos2)
#    #
#    datos=conf.read_conf()
#    #print(datos)
#    
#    print(conf.get_dir() / datos['dir_caratulas'])
