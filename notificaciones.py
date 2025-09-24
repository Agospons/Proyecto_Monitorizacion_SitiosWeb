import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import time
from models.alertas import Alertas as AlertasModel
from models.sitios import Sitios as SitiosModel



CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email_from': 'sofiapons16@gmail.com', ######## mail el cual va a mandar las notificaciones 
    'email_password': 'rnkr bhwc okii adrs', ######### general otra contraseña si pasa el cambio de mail
    'database_url': 'mysql+pymysql://root:Agostina25@localhost:3306/Proyecto_Monitorizacion_SitiosWeb'
}
####### en caso de pasar archivos a otra computadora general el taskschd.msc para que sea automatico el envio de mails 

def test_conexiones():
    print("🔍 Probando conexiones...")
    
    try:
        engine = create_engine(CONFIG['database_url'])
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión MySQL exitosa")
    except Exception as e:
        print(f"❌ Error MySQL: {e}")
        return False
    
    try:
        server = smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port'])
        server.starttls()
        server.login(CONFIG['email_from'], CONFIG['email_password'])
        server.quit()
        print("✅ Conexión Email exitosa")
    except Exception as e:
        print(f"❌ Error Email: {e}")
        return False
    
    return True


def obtener_dominios_por_vencer(dias_antes=7):
    try:
        engine = create_engine(CONFIG['database_url'])
        Session = sessionmaker(bind=engine)
        session = Session()
        
        fecha_limite = datetime.now().date() + timedelta(days=dias_antes)
        
        query = text("""
            SELECT 
                s.id, s.dominio, s.servidor, s.ip, s.id_cliente, 
                s.notas, s.estado, s.ultima_revision, s.vencimiento_dominio,
                s.estado_dominio, s.fecha_alta,
                u.id, u.nombre_completo, u.email, u.telefono, 
                u.observaciones, u.fecha_alta, u.password
            FROM sitios s 
            JOIN usuarios u ON s.id_cliente = u.id 
            WHERE s.vencimiento_dominio BETWEEN :hoy AND :limite
        """)
        
        result = session.execute(query, {
            'hoy': datetime.now().date(),
            'limite': fecha_limite
        })
        
        dominios = result.fetchall()
        print(f"📊 Encontrados {len(dominios)} dominios por vencer en {dias_antes} días")
        
        session.close()
        return dominios
        
    except Exception as e:
        print(f"❌ Error obteniendo dominios: {e}")
        return []


def enviar_email(destinatario, asunto, cuerpo, id_sitio=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = CONFIG['email_from']
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'html'))

        server = smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port'])
        server.starttls()
        server.login(CONFIG['email_from'], CONFIG['email_password'])
        server.send_message(msg)
        server.quit()
        
        ###### CREA ALERTA ############
        if id_sitio:
            crear_alerta_vencimiento(id_sitio)
        
        print(f"✅ Email enviado a: {destinatario}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

def crear_alerta_vencimiento(id_sitio):
    try:
        engine = create_engine(CONFIG['database_url'])
        Session = sessionmaker(bind=engine)
        session = Session()
        
        nueva_alerta = AlertasModel(
            id_sitio=id_sitio,
            timestamp=datetime.now().time(),  
            tipo_alertas="vencimiento",       
            canal="email"                     
        )
        
        session.add(nueva_alerta)
        session.commit()
        session.close()
        
        print(f"✅ Alerta creada para sitio ID: {id_sitio}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando alerta: {e}")
        return False


def main():
    print("🚀 Iniciando notificador de dominios...")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    if not test_conexiones():
        print("❌ No se pueden establecer las conexiones necesarias")
        return
    
    print("\n🔍 Buscando dominios que vencen en 7 días...")
    dominios = obtener_dominios_por_vencer(7)

    if not dominios:
        print("✅ No hay dominios por vencer")
        return
    
    print(f"\n📧 Enviando {len(dominios)} notificaciones...")
    
    for dominio in dominios:
        datos = {
            'id_sitio': dominio[0],
            'dominio': dominio[1],
            'servidor': dominio[2],
            'ip': dominio[3],
            'id_cliente': dominio[4],
            'notas': dominio[5],
            'estado': dominio[6],
            'ultima_revision': dominio[7],
            'vencimiento_dominio': dominio[8],
            'estado_dominio': dominio[9],
            'fecha_alta_sitio': dominio[10],
            'id_usuario': dominio[11],
            'nombre_completo': dominio[12],
            'email': dominio[13],
            'telefono': dominio[14],
            'observaciones': dominio[15],
            'fecha_alta_usuario': dominio[16],
            'password': dominio[17]
        }
        
        print(f"📋 Datos: {datos['dominio']} vence {datos['vencimiento_dominio']}")
        
        if isinstance(datos['vencimiento_dominio'], str):
            try:
                fecha_vencimiento = datetime.strptime(datos['vencimiento_dominio'], '%Y-%m-%d').date()
                dias_restantes = (fecha_vencimiento - datetime.now().date()).days
            except ValueError:
                print(f"❌ Formato de fecha inválido: {datos['vencimiento_dominio']}")
                continue
        else:
            dias_restantes = (datos['vencimiento_dominio'] - datetime.now().date()).days
        
        asunto = f"⚠️ Vencimiento de dominio: {datos['dominio']} - {dias_restantes} días"
        
        cuerpo = f"""
        <html>
        <body>
            <h2>⚠️ Recordatorio de Vencimiento de Dominio</h2>
            <p>Hola <strong>{datos['nombre_completo']}</strong>,</p>
            <p>Tu dominio <strong>{datos['dominio']}</strong> vence en <strong>{dias_restantes} días</strong>.</p>
            <p><strong>Fecha de vencimiento:</strong> {datos['vencimiento_dominio']}</p>
            <p>Por favor, realiza la renovación a tiempo.</p>
            <br>
            <p>Saludos cordiales,<br>Equipo de Soporte</p>
        </body>
        </html>
        """
        
    if enviar_email(datos['email'], asunto, cuerpo, id_sitio=datos['id_sitio']):
        print(f"✅ Notificación enviada a {datos['email']}")
    else:
        print(f"❌ Error enviando a {datos['email']}")


def ejecutar_automaticamente():
    while True:
        print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Ejecutando...")
        main()
        print("⏰ Próxima ejecución en 24 horas...")
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    ejecutar_automaticamente()


