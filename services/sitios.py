from sqlalchemy.orm import Session
from models.sitios import Sitios as SitiosModel
from schemas.sitios import Sitios
from schemas.sitios import EstadoO_O
from models.log_chequeo import Log_chequeo as LogoModels
from schemas.log_chequeo import Log_chequeo, logOut
import requests
import time
from models.alertas import Alertas as AlertasModel
from models.usuarios import Usuarios as UsuariosModel
from fastapi import HTTPException
from datetime import date, datetime
from http.client import HTTPConnection
from urllib.request import urlopen


class SitiosService():
    def __init__(self, db) -> None:
       self.db = db
    
    def create_Sitios(self, sitios: Sitios):
        hoy = date.today()
        fecha_alta = sitios.fecha_alta

        vencimiento_domino = sitios.vencimiento_dominio
        hoy = date.today()
        
        if vencimiento_domino <= hoy:
            raise HTTPException(status_code=404, detail="la fecha del vencimiento debe ser posterior a hoy")
        
        if fecha_alta is None:
            raise ValueError("fecha_alta no puede ser nula")
        
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == sitios.id_cliente).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        ip = self.db.query(SitiosModel).filter(SitiosModel.ip == sitios.ip).first()
        if ip:
            raise HTTPException(status_code=404, detail="La direccion IP ya esta registrada")
        
        nuevo_sitio = SitiosModel(**sitios.dict())
                
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
        
        self.db.add(nuevo_sitio)
        self.db.commit()
        


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
        if not sitio:
            raise HTTPException(status_code=404, detail="Sitio no encontrado")
        
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
        
        tiempo_respuesta = 0
        estado = data.estado 

        try:
            start_time = time.time()
            response = requests.get(url, timeout=10, verify=False)
            end_time = time.time()

            tiempo_respuesta = int((end_time - start_time) * 1000)
            estado = "online" if response.status_code == 200 else "offline"

        except requests.exceptions.Timeout:
            estado = "offline"
            tiempo_respuesta = None
            error_message = "Timeout: El sitio no respondió a tiempo (10s)"

        except requests.exceptions.ConnectionError:
            estado = "offline"
            tiempo_respuesta = None
            error_message = f"No se pudo resolver el dominio: {url}"

        except requests.exceptions.RequestException as e:
            estado = "offline"
            tiempo_respuesta = None
            error_message = f"Error de conexión: {str(e)}"

        log = LogoModels(
            id_sitio = sitio.id,
            estado = data.estado, 
            tiempo_respuesta = tiempo_respuesta,
            timestamp = datetime.now()
        )
        self.db.add(log)


        hoy = datetime.now().date()
        
        if data.estado == "offline":

            alerta = AlertasModel(
                id_sitio = sitio.id,
                timestamp = datetime.now(),
                canal = "Sistema",  
                tipo_alertas = "Caida" , 
                fecha_alerta = hoy
            )
            self.db.add(alerta)
        else:
            self.db.query(AlertasModel).filter(AlertasModel.id_sitio == sitio.id).delete()
            self.db.commit()

        if data.vencimiento_dominio <= hoy:
            alerta = AlertasModel(
                id_sitio = sitio.id,
                timestamp = datetime.now(),
                canal = "Sistema",  
                tipo_alertas = "Vencimiento" , 
                fecha_alerta = hoy
            )
            self.db.add(alerta)
        else:
            self.db.query(AlertasModel).filter(AlertasModel.id_sitio == sitio.id).delete()
            self.db.commit()
            


        self.db.commit()
        return {"message": "Sitio actualizado correctamente"}
    

    def delete_sitios(self, id: int):
        sitios = self.db.query(SitiosModel).filter(SitiosModel.id == id).first()
        if sitios:
            self.db.delete(sitios)
            self.db.commit()
            return 

    
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
        
        #### errores tipicos en caso de el control del link falle
        except requests.exceptions.ConnectionError as e:
            estado = EstadoO_O.offline
            error_message = f"Error de conexión: {str(e)}"
            
        except requests.exceptions.RequestException as e:
            estado = EstadoO_O.offline
            error_message = f"Error en la solicitud: {str(e)}"
            
        except Exception as e:
            estado = EstadoO_O.offline
            error_message = f"Error inesperado: {str(e)}"
        
        try: ### actualiza la bd en sitios - alertas - log
            sitio.estado = estado
            sitio.ultima_revision = datetime.now()
            self.db.commit()

            if estado == "offline":
                hoy = datetime.now().date()
            
                alerta = AlertasModel (
                    id_sitio = sitio.id,
                    timestamp = datetime.now(),
                    canal = "update",
                    tipo_alertas = "Caida", 
                    fecha_alerta = hoy
                )
                self.db.add(alerta)
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


        hoy = datetime.now().date()
        for sitios in sitio:
            if sitios.estado == "offline":
                alerta = AlertasModel(
                    id_sitio = sitios.id,
                    timestamp = datetime.now(),
                    canal = "Sistema",  
                    tipo_alertas = "Caida" , 
                    fecha_alerta = hoy
                )
                self.db.add(alerta)
            else:
                self.db.query(AlertasModel).filter(AlertasModel.id_sitio == sitios.id).delete()
                self.db.commit()

        for sitios in sitio:
            if sitio.vencimiento_dominio <= hoy:
                alerta = AlertasModel(
                    id_sitio = sitio.id,
                    timestamp = datetime.now(),
                    canal = "Sistema",  
                    tipo_alertas = "Vencimiento" , 
                    fecha_alerta = hoy
                )
                self.db.add(alerta)
            else:
                self.db.query(AlertasModel).filter(AlertasModel.id_sitio == sitios.id).delete()
                self.db.commit()

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
        
        print(f"🔍 Verificando {len(sitios)} sitios...")
        
        for i, sitio in enumerate(sitios, 1):
            try:
                resultado = self.chequear_sitio(sitio.id)
                resultados.append(resultado)
                
            except Exception as e:
                resultados.append({
                    "id_sitio": sitio.id,
                    "dominio": sitio.dominio,
                    "estado": "error",
                    "mensaje_error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        hoy = datetime.now().date()
        for sitio in sitios:
            if sitio.estado == "offline":
                alerta = AlertasModel(
                    id_sitio = sitio.id,
                    timestamp = datetime.now(),
                    canal = "Sistema",  
                    tipo_alertas = "Caida" , 
                    fecha_alerta = hoy
                )
                self.db.add(alerta)
            else:
                self.db.query(AlertasModel).filter(AlertasModel.id_sitio == sitio.id).delete()
                self.db.commit()

        for sitio in sitios:
            if sitios.vencimiento_dominio <= hoy:
                alerta = AlertasModel(
                    id_sitio = sitios.id,
                    timestamp = datetime.now(),
                    canal = "Sistema",  
                    tipo_alertas = "Vencimiento" , 
                    fecha_alerta = hoy
                )
                self.db.add(alerta)
            else:
                self.db.query(AlertasModel).filter(AlertasModel.id_sitio == sitio.id).delete()
                self.db.commit()

        return resultados