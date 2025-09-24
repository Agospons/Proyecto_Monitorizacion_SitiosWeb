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
        try:
            sitio = self.db.query(SitiosModel).filter(SitiosModel.id == id).first()
            if not sitio:
                raise HTTPException(status_code=404, detail="Sitio Web no encontrado")

            url = sitio.dominio.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            tiempo_respuesta = None
            estado = "offline"
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
                
                tiempo_respuesta = int((end_time - start_time) * 1000)
                status_code = response.status_code
                
                if 200 <= response.status_code < 400:
                    estado = "online"
                else:
                    estado = "offline"
                    error_message = f"Código HTTP: {status_code}"
                    
            except requests.exceptions.Timeout:
                estado = "offline"
                error_message = "Timeout: El sitio no respondió a tiempo (10s)"
                
            except requests.exceptions.SSLError:
                try:
                    if url.startswith('https://'):
                        http_url = url.replace('https://', 'http://')
                        start_time = time.time()
                        response = requests.get(http_url, timeout=8, verify=False)
                        end_time = time.time()
                        tiempo_respuesta = int((end_time - start_time) * 1000)
                        status_code = response.status_code
                        
                        if 200 <= response.status_code < 400:
                            estado = "online"
                            error_message = "Funciona con HTTP (HTTPS falló)"
                        else:
                            estado = "offline"
                            error_message = f"HTTP falló con código: {status_code}"
                    else:
                        estado = "offline"
                        error_message = "Error SSL/TLS"
                        
                except Exception as fallback_error:
                    estado = "offline"
                    error_message = f"Error SSL y fallback HTTP: {str(fallback_error)}"
            
            except requests.exceptions.ConnectionError as e:
                estado = "offline"
                error_message = f"Error de conexión: {str(e)}"
                
            except requests.exceptions.RequestException as e:
                estado = "offline"
                error_message = f"Error en la solicitud: {str(e)}"
                
            except Exception as e:
                estado = "offline"
                error_message = f"Error inesperado: {str(e)}"
        
            try:
                sitio.estado = estado
                sitio.ultima_revision = datetime.now()
                self.db.commit()

                if estado == "offline":
                    hoy = datetime.now().date()
                    alerta_existente = self.db.query(AlertasModel).filter(
                        AlertasModel.id_sitio == sitio.id,
                        AlertasModel.tipo_alertas == "Caida",
                        AlertasModel.fecha_alerta == hoy
                    ).first()
                    
                    if not alerta_existente:
                        alerta = AlertasModel(
                            id_sitio=sitio.id,
                            timestamp=datetime.now(),
                            canal="Verificación",
                            tipo_alertas="Caida", 
                            fecha_alerta=hoy,
                            detalles=error_message
                        )
                        self.db.add(alerta)
                        self.db.commit()
                self._actualizar_alertas_automaticas()
        
            except Exception as db_error:
                return(f"Error actualizando BD: {db_error}")

            try:
                log = LogoModels(
                    id_sitio=sitio.id,
                    estado=estado,
                    tiempo_respuesta=tiempo_respuesta,
                    timestamp=datetime.now()
                )
                self.db.add(log)
                self.db.commit()
            except Exception as log_error:
                return(f"Error creando log: {log_error}")

            return {
                "id_sitio": id,
                "dominio": sitio.dominio,
                "url_verificada": url,
                "estado": estado,
                "codigo_respuesta": status_code,
                "tiempo_respuesta": tiempo_respuesta,
                "mensaje_error": error_message,
                "timestamp": datetime.now().isoformat()
                
            }

        except Exception as e:
            return(f"💥 Error en chequear_sitio para ID {id}: {e}")
            

    def chequear_todos_los_sitios(self):
        try:
            sitios = self.db.query(SitiosModel).all()
            resultados = []
            
            for i, sitio in enumerate(sitios, 1):
                try:

                    resultado = self.chequear_sitio(sitio.id)
                    resultados.append(resultado)
                    
                    return(f"✅ {sitio.dominio}: {resultado.get('estado', 'N/A')}")
                    
                except Exception as e:
                    error_msg = f"Error verificando {sitio.dominio}: {str(e)}"
                
                    resultados.append({
                        "id_sitio": sitio.id,
                        "dominio": sitio.dominio,
                        "estado": "error",
                        "mensaje_error": error_msg,
                        "timestamp": datetime.now().isoformat()
                    })

            self._actualizar_alertas_automaticas()
            
            return resultados
            
        except Exception as e:
            return [{"error": str(e)}]
            
    def _actualizar_alertas_automaticas(self):
        try:
            hoy = datetime.now().date()
            sitios = self.db.query(SitiosModel).all()
                
            for sitio in sitios:
                if sitio.estado == "offline":
                    alerta_existente = self.db.query(AlertasModel).filter(
                        AlertasModel.id_sitio == sitio.id,
                        AlertasModel.tipo_alertas == "Caida",
                        AlertasModel.fecha_alerta == hoy
                    ).first()
                    
                    if not alerta_existente:
                        nueva_alerta = AlertasModel(
                            id_sitio=sitio.id,
                            timestamp=datetime.now(),
                            canal="Sistema",
                            tipo_alertas="Caida",
                            fecha_alerta=hoy,
                            detalles=f"Sitio {sitio.dominio} no responde"
                        )
                        self.db.add(nueva_alerta)
                else:
                    eliminadas = self.db.query(AlertasModel).filter(
                        AlertasModel.id_sitio == sitio.id,
                        AlertasModel.tipo_alertas == "Caida"
                    ).delete()
            
                if sitio.vencimiento_dominio and sitio.vencimiento_dominio <= hoy:
                    alerta_existente = self.db.query(AlertasModel).filter(
                        AlertasModel.id_sitio == sitio.id,
                        AlertasModel.tipo_alertas == "Vencimiento",
                        AlertasModel.fecha_alerta == hoy
                    ).first()
                    
                    if not alerta_existente:
                        nueva_alerta = AlertasModel(
                            id_sitio=sitio.id,
                            timestamp=datetime.now(),
                            canal="Sistema",
                            tipo_alertas="Vencimiento",
                            fecha_alerta=hoy,
                            detalles=f"Dominio {sitio.dominio} vence el {sitio.vencimiento_dominio}"
                        )
                        self.db.add(nueva_alerta)
                else:
                    eliminadas = self.db.query(AlertasModel).filter(
                        AlertasModel.id_sitio == sitio.id,
                        AlertasModel.tipo_alertas == "Vencimiento"
                    ).delete()
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            try:
                if not isinstance(sitios, (list, tuple)):
                    if hasattr(sitios, 'id'):
                        # Si es un solo objeto, convertirlo a lista
                        sitios = [sitios]
                    else:
                        return
                
                hoy = datetime.now().date()
                alertas_creadas = 0
                alertas_eliminadas = 0

                for sitio in sitios:
                    try:
                        if not hasattr(sitio, 'id'):
                            continue

                        sitio_actualizado = self.db.query(SitiosModel).filter(
                            SitiosModel.id == sitio.id
                        ).first()
                        
                        if not sitio_actualizado:
                            continue


                        alerta_caida = self.db.query(AlertasModel).filter(
                            AlertasModel.id_sitio == sitio_actualizado.id,
                            AlertasModel.tipo_alertas == "Caida"
                        ).first()

                        if sitio_actualizado.estado == "offline":
                            if not alerta_caida:
                                nueva_alerta = AlertasModel(
                                    id_sitio=sitio_actualizado.id,
                                    timestamp=datetime.now(),
                                    canal="Sistema",
                                    tipo_alertas="Caida",
                                    fecha_alerta=hoy,
                                    detalles=f"Sitio {sitio_actualizado.dominio} no responde"
                                )
                                self.db.add(nueva_alerta)
                                alertas_creadas += 1
                        else:
                            if alerta_caida:
                                self.db.delete(alerta_caida)
                                alertas_eliminadas += 1

                        alerta_vencimiento = self.db.query(AlertasModel).filter(
                            AlertasModel.id_sitio == sitio_actualizado.id,
                            AlertasModel.tipo_alertas == "Vencimiento"
                        ).first()

                        if (sitio_actualizado.vencimiento_dominio and 
                            sitio_actualizado.vencimiento_dominio <= hoy):
                            if not alerta_vencimiento:
                                nueva_alerta = AlertasModel(
                                    id_sitio=sitio_actualizado.id,
                                    timestamp=datetime.now(),
                                    canal="Sistema",
                                    tipo_alertas="Vencimiento",
                                    fecha_alerta=hoy,
                                    detalles=f"Dominio {sitio_actualizado.dominio} vence el {sitio_actualizado.vencimiento_dominio}"
                                )
                                self.db.add(nueva_alerta)
                                alertas_creadas += 1
                        else:
                            if alerta_vencimiento:
                                self.db.delete(alerta_vencimiento)
                                alertas_eliminadas += 1
                                
                    except Exception as e:
                        continue

                self.db.commit()
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.db.rollback()