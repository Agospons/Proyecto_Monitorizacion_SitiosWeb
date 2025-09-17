from sqlalchemy.orm import Session
from models.sitios import Sitios as SitiosModel
from schemas.sitios import Sitios
from schemas.sitios import EstadoO_O
from models.log_chequeo import Log_chequeo as LogoModels
from schemas.log_chequeo import Log_chequeo, logOut
import requests
import time
from models.usuarios import Usuarios as UsuariosModel
from fastapi import HTTPException
from datetime import date, datetime
import sqlite3
from http.client import HTTPConnection
from urllib.request import urlopen
import urllib.request

from urllib.error import URLError, HTTPError




class SitiosService():
    def __init__(self, db) -> None:
       self.db = db
    
    def create_Sitios(self, sitios: Sitios):
        hoy = date.today()
        fecha_alta = sitios.fecha_alta

        if fecha_alta is None:
            raise ValueError("fecha_alta no puede ser nula")

        if fecha_alta > hoy:
            raise HTTPException(status_code=404, detail="La fecha de alta no puede ser posterior a hoy")
        
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == sitios.id_cliente).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        ip = self.db.query(SitiosModel).filter(SitiosModel.ip == sitios.ip).first()
        if ip:
            raise HTTPException(status_code=404, detail="La direccion IP ya esta registrada")
        
        nuevo_sitio = SitiosModel(**sitios.dict())
        self.db.add(nuevo_sitio)
        self.db.commit()

        url = nuevo_sitio.dominio.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        try:
            start_time = time.time()  
            response = requests.get(
                url, 
                timeout=10,
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Website Monitoring Bot)',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                },
                verify=False
            )
            end_time = time.time()
            
            tiempo_respuesta = int((end_time - start_time) * 1000)
        except requests.exceptions.Timeout:
            estado = EstadoO_O.offline
            error_message = "Timeout: El sitio no respondió a tiempo (10s)"
        

        log = LogoModels (
            id_sitio = nuevo_sitio.id,
            estado = sitios.estado,
            tiempo_respuesta = tiempo_respuesta,
            timestamp = datetime.now()
        )
        self.db.add(log)
        self.db.commit()
        return nuevo_sitio

    def get_sitios(self):
        resultado = self.db.query(SitiosModel).all()
        return resultado
    
    def get_sitios_id(self, id:int):
        resultado = self.db.query(SitiosModel).filter(SitiosModel.id == id).first()
        return resultado
    
    def update_Sitios(self, idd: int, data: Sitios):
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == data.id_cliente).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == idd).first()
        sitio.dominio = data.dominio
        sitio.ip = data.ip
        sitio.servidor = data.servidor
        sitio.id_cliente = data.id_cliente
        sitio.notas = data.notas
        sitio.estado = data.estado
        sitio.ultima_revision = data.ultima_revision
        sitio.vencimiento_dominio = data.vencimiento_dominio
        sitio.estado_dominio = data.estado_dominio
        sitio.fecha_alta = data.fecha_alta
        
        
        url = sitio.dominio.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        try:
            start_time = time.time()  
            response = requests.get(
                url, 
                timeout=10,
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Website Monitoring Bot)',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                },
                verify=False
            )
            end_time = time.time()
            
            tiempo_respuesta = int((end_time - start_time) * 1000)
        except requests.exceptions.Timeout:
            estado = EstadoO_O.offline
            error_message = "Timeout: El sitio no respondió a tiempo (10s)"
        

        log = LogoModels (
            id_sitio = sitio.id,
            estado = data.estado,
            tiempo_respuesta = tiempo_respuesta,
            timestamp = datetime.now()
        )
        self.db.add(log)
        
        self.db.commit()
        return 
    
    def delete_sitios(self, id: int):
        sitios = self.db.query(SitiosModel).filter(SitiosModel.id == id).first()
        if sitios:
            self.db.delete(sitios)
            self.db.commit()
            return 





########################################################################################################################################################################################################################################################
    
    
    
    def chequear_sitio(self, id: int):
        ### verificar si el id del sitio a chequear es valido
        sitio = self.db.query(SitiosModel).filter(SitiosModel.id == id).first()
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio Web no encontrado")

        ### controla la url
        url = sitio.dominio.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        tiempo_respuesta = None
        estado = EstadoO_O.offline
        status_code = 0
        error_message = None


        try:
            start_time = time.time()  
            response = requests.get(
                url, 
                timeout=10,
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Website Monitoring Bot)',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                },
                verify=False
            )
            end_time = time.time()
            
            tiempo_respuesta = int((end_time - start_time) * 1000) ### crear el tiempo de respuesta segun el momento en el que empieza y cuadno decuelve el resultafo
            status_code = response.status_code ### codigo de respuesta
            
            
            if 200 <= response.status_code < 400:
                estado = EstadoO_O.online
            else:
                estado = EstadoO_O.offline
                error_message = f"Código HTTP: {status_code}" ### en caso de que el sitio lance un error 
                
        except requests.exceptions.Timeout:
            estado = EstadoO_O.offline
            error_message = "Timeout: El sitio no respondió a tiempo (10s)" ## lanza error en caso de que demore demaciado en verificar el sitio
            
        except requests.exceptions.SSLError:
            
            try: ### en caso de que el link ingresado falle en https
                if url.startswith('https://'):
                    http_url = url.replace('https://', 'http://')
                    start_time = time.time()
                    response = requests.get(http_url, timeout=8, verify=False)
                    end_time = time.time()
                    tiempo_respuesta = int((end_time - start_time) * 1000)
                    status_code = response.status_code
                    
                    if 200 <= response.status_code < 400:
                        estado = EstadoO_O.online
                        error_message = "Funciona con HTTP (HTTPS falló)"
                    else:
                        estado = EstadoO_O.offline
                        error_message = f"HTTP falló con código: {status_code}"
                else:
                    estado = EstadoO_O.offline
                    error_message = "Error SSL/TLS"
                    
            except Exception as fallback_error:
                estado = EstadoO_O.offline
                error_message = f"Error SSL y fallback HTTP: {str(fallback_error)}"
        
        ### errores tipicos en caso de el control del link falle
        except requests.exceptions.ConnectionError as e:
            estado = EstadoO_O.offline
            error_message = f"Error de conexión: {str(e)}"
            
        except requests.exceptions.RequestException as e:
            estado = EstadoO_O.offline
            error_message = f"Error en la solicitud: {str(e)}"
            
        except Exception as e:
            estado = EstadoO_O.offline
            error_message = f"Error inesperado: {str(e)}"
        
        try: ### actualiza la bd
            sitio.estado = estado
            sitio.ultima_revision = datetime.now()
            self.db.commit()
        except Exception as db_error:
            error_message = f"{error_message} | Error BD: {str(db_error)}"

        ### crea el log 
        try:
            log = LogoModels (
            id_sitio = sitio.id,
            estado = estado.value,
            tiempo_respuesta = tiempo_respuesta,
            timestamp = datetime.now()
            )
            
            self.db.add(log)
            self.db.commit()
        except Exception as log_error:
            pass

        return {
            "id_sitio": id,
            "dominio": sitio.dominio,
            "url_verificada": url,
            "estado": estado.value,
            "codigo_respuesta": status_code,
            "tiempo_respuesta": f"{tiempo_respuesta} ms" if tiempo_respuesta else "N/A",
            "mensaje_error": error_message,
            "timestamp": datetime.now().isoformat()
        }



    def chequear_todos_los_sitios(self):
        sitios = self.db.query(SitiosModel).all()
        resultados = []
        
        for sitio in sitios:
            try:
                resultado = self.chequear_sitio(sitio.id)
                resultados.append(resultado)
            except Exception as e:
                resultados.append({
                    "id_sitio": sitio.id,
                    "dominio": sitio.dominio,
                    "error": str(e),
                    "estado": "error"
                })
        
        return resultados
