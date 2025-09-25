import {fetchConAuth} from "./fetchAuth.js";


document.addEventListener("DOMContentLoaded", async () => {
    const usuario = JSON.parse(sessionStorage.getItem("usuario"));
    const saludo = document.getElementById("usuarioSaludos");

    if (usuario) {
        saludo.textContent = `Bienvenido, ${usuario.nombre_completo}`;
    }

    document.getElementById("cerrar").addEventListener("click", () => {
        window.location.href = "index.html";
        });
    const statsContainer = document.querySelector(".textos");
    const token = sessionStorage.getItem("token");

    try {
        const res = await fetch("http://127.0.0.1:8000/dashboard/admin", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
        });

    const data = await res.json();

    statsContainer.innerHTML = `
        <p>✅ Sitios Online:  ${data.sitios_online}</p>
        <p>❌ Sitios Offline:  ${data.sitios_offline}</p>
        <p>⚠️ Sitios con Domino Vencido:  ${data.dominio_vencido}</p>
        
    `;
    } catch (err) {
        statsContainer.innerHTML = `<p>Error al cargar estadísticas: ${err.message}</p>`;
    }

    
    document.getElementById("btnU").addEventListener("click", () => {
        window.location.href = "crudClientes.html";
    });

    
    document.getElementById("btnS").addEventListener("click", () => {
        window.location.href = "crudSitios.html";
    });
    document.getElementById("cerrar").addEventListener("click", () => {
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("usuario");
        
        window.location.href = "index.html";
    });
    const tablaUsuarios = document.getElementById("usuariosTabla");
    
    
    async function cargarUsuarios() {    //////////// carga todos los usuarios /////////
    try {
        const res = await fetchConAuth("http://127.0.0.1:8000/usuarios");
        if (!res.ok) throw new Error("No se pudieron obtener usuarios");
        const data = await res.json();

        tablaUsuarios.innerHTML = "";
        data.forEach(u => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${u.id}</td>
            <td>${u.nombre_completo}</td>
            <td>${u.email}</td>
            <td>${u.telefono}</td>
            <td>${u.fecha_alta}</td>
            <td>${u.observaciones ?? ""}</td>
        `;
        tablaUsuarios.appendChild(tr);
        });
    } catch (err) {
        alert("Error al cargar usuarios");
    }
    }

        //// lista últimos 5 usuarios registrados
    async function cargarUltimosUsuarios() {
    try {
        const res = await fetchConAuth("http://127.0.0.1:8000/dashboard/admin");
        if (!res.ok) throw new Error("No se pudieron obtener los últimos usuarios");
        const data = await res.json();

        
        const ultimos = data.ultimos_usuarios;

        const tablaUltimos = document.getElementById("usuariosTabla");
        tablaUltimos.innerHTML = "";
        ultimos.forEach(u => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${u.id}</td>
            <td>${u.nombre_completo}</td>
            <td>${u.email}</td>
            <td>${u.telefono}</td>
            <td>${u.fecha_alta}</td>
            <td>${u.observaciones ?? ""}</td>
        `;
        tablaUltimos.appendChild(tr);
        });
    } catch (err) {
        alert(err.message);
    }
    }
    
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    const tablaSitios = document.getElementById("sitiosTabla");
    
    async function cargarSitios() { //////////// Carga todos los sitios /////////
    try {
        const res = await fetchConAuth("http://127.0.0.1:8000/sitios");
        if (!res.ok) throw new Error("No se pudieron obtener sitios");
        const data = await res.json();

        tablaSitios.innerHTML = "";
        data.forEach(s => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${s.id}</td>
            <td>${s.dominio}</td>
            <td>${s.ip}</td>
            <td>${s.id_cliente}</td>
            <td>${s.notas}</td>
            <td>${s.estado}</td>
            <td>${s.ultima_revision}</td>
            <td>${s.vencimiento_dominio}</td>
            <td>${s.estado_dominio}</td>
            <td>${s.fecha_alta}</td>
            <td>${s.servidor}</td>
        `;
        tablaSitios.appendChild(tr);
        });
    } catch (err) {
        alert("Error al cargar sitios: " + err.message);
    }
    }

    
    async function cargarUltimosSitios() {  ///////// Carga los sitios pero solo los que estan ofline /////////
    try {
        const res = await fetchConAuth("http://127.0.0.1:8000/dashboard/admin");
        if (!res.ok) throw new Error("No se pudieron obtener los últimos sitios");
        const data = await res.json();

        const ultimos = data.web_no_online;

        const tablaUltimos = document.getElementById("sitiosTabla");
        tablaUltimos.innerHTML = "";
        ultimos.forEach(s => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${s.id}</td>
            <td>${s.dominio}</td>
            <td>${s.ip}</td>
            <td>${s.id_cliente}</td>
            <td>${s.notas}</td>
            <td style="color:${s.estado === "online" ? "green" : "red"}">
            ${s.estado}
            </td><td>${s.ultima_revision}</td>
            <td>${s.vencimiento_dominio}</td>
            <td>${s.estado_dominio}</td>
            <td>${s.fecha_alta}</td>
            <td>${s.servidor}</td>
            
        `;
        tablaUltimos.appendChild(tr);
        });
    } catch (err) {
        alert("Error al cargar últimos sitios: " + err.message);
    }
    }



    async function cargarSitiosOffline() { ///////// Muestra los sitios offline /////////
    try {
        const res = await fetch("http://127.0.0.1:8000/sitios");
        if (!res.ok) throw new Error("No se pudieron obtener sitios");
        const data = await res.json();

        const offline = data.filter(s => s.estado.toLowerCase() === "offline");

        const tabla = document.getElementById("sitiosTabla");
        tabla.innerHTML = "";

        if (offline.length === 0) {
        tabla.innerHTML = `
            <tr>
            <td colspan="11" style="text-align:center; color:green;">
                ✅ Todos los sitios están online
            </td>
            </tr>
        `;
        return;
        }

        offline.forEach(s => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${s.id}</td>
            <td>${s.dominio}</td>
            <td>${s.ip}</td>
            <td>${s.id_cliente}</td>
            <td>${s.notas}</td>
            <td style="color:red"> ❌${s.estado}</td>
            <td>${s.ultima_revision}</td>
            <td>${s.vencimiento_dominio}</td>
            <td>${s.estado_dominio}</td>
            <td>${s.fecha_alta}</td>
            <td>${s.servidor}</td>
        `;
        tabla.appendChild(tr);
        });
    } catch (err) {
        console.error("Error al cargar sitios offline:", err);
    }
    }

    

    const btnHistorial = document.getElementById("btnH");
    const idSitio = document.getElementById("id_sitio");
    const historialTabla = document.getElementById("historialTabla");

    ////// función para obtener historial desde el backend
    async function cargarHistorial(idSitio) {
        try {
        const token = sessionStorage.getItem("token");

        const res = await fetch(`http://127.0.0.1:8000/dashboard/admin/${idSitio}`, {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error("Error al obtener historial: " + errorText);
        }

        const data = await res.json();

        historialTabla.innerHTML = "";

        data.historial_sitios.forEach(log => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
            <td>${log.id}</td>
            <td>${log.id_sitio}</td>
            <td>${log.estado}</td>
            <td>${log.tiempo_respuesta ?? "-"}</td>
            <td>${log.timestamp}</td>
            `;
            historialTabla.appendChild(tr);
        });

        if (data.historial_sitios.length === 0) {
            historialTabla.innerHTML = `<tr><td colspan="5">No hay historial para este sitio</td></tr>`;
        }

        } catch (err) {
        alert(err.message);
        }
    }

    btnHistorial.addEventListener("click", () => {
        const idS = idSitio.value.trim();
        if (!idS) {
        alert("Por favor ingrese un ID de sitio");
        return;
        }
        cargarHistorial(idS);
    });



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////controlar todos los sitios web
    
    const btnVerificar = document.getElementById("button");
    
    btnVerificar.addEventListener("click", async () => {
        await verificarTodosLosSitios();
    });


    //////////////// funcion principal luego de precionar el boton de verificar sitios en el dashboard de resumen general
    async function verificarTodosLosSitios() {
    try {
        console.log('🔍 Iniciando verificación de todos los sitios...');

        const originalText = btnVerificar.textContent;
        btnVerificar.textContent = "⏳ Verificando...";
        btnVerificar.disabled = true;

        const token = sessionStorage.getItem('token');
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        console.log('📡 Enviando solicitud de verificación...');
        const res = await fetch(`http://127.0.0.1:8000/sitios/verificar/todos`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        });

        console.log('📊 Status de respuesta:', res.status);
        
        if (!res.ok) {
            const errorText = await res.text();
            console.error('❌ Error del servidor:', errorText);
            throw new Error("Error al verificar sitios: " + errorText);
        }

        const resultados = await res.json();
        console.log('✅ Resultados de verificación recibidos:', resultados);
        
        if (!Array.isArray(resultados)) {
            throw new Error("Formato de respuesta inválido");
        }

        // Mostrar resultados
        mostrarResultadosVerificacion(resultados);
        
        // Actualizar la interfaz
        await cargarSitiosOffline();
        await actualizarResumen();

    } catch (err) {
        console.error("❌ Error en verificación:", err);
        mostrarAlerta(`❌ Error: ${err.message}`, "error");
    } finally {
        // Restaurar botón
        btnVerificar.textContent = "Verificar estado";
        btnVerificar.disabled = false;
        console.log('✅ Verificación completada');
    }
}

    function mostrarResultadosVerificacion(resultados) { //////////// muetra los resultados luego de que se hayan controlado los sitios

        console.log('📈 Procesando resultados:', resultados);
        
        const online = resultados.filter(s => s.estado === "online").length;
        const offline = resultados.filter(s => s.estado === "offline").length;
        const errores = resultados.filter(s => s.estado === "error").length;
        const total = resultados.length;

        let mensaje = `✅ Verificación completada\n`;
        mensaje += `📊 Total sitios: ${total}\n`;
        mensaje += `🟢 Online: ${online}\n`;
        mensaje += `🔴 Offline: ${offline}\n`;
        mensaje += `⚠️ Errores: ${errores}`;

        if (offline > 0 || errores > 0) {
            mensaje += `\n\n❌ Problemas detectados:\n`;
            
            resultados.filter(s => s.estado === "offline").forEach(sitio => {
                mensaje += `• 🔴 ${sitio.dominio} - ${sitio.mensaje_error || 'Sin conexión'}\n`;
            });
            
            resultados.filter(s => s.estado === "error").forEach(sitio => {
                mensaje += `• ⚠️ ${sitio.dominio} - ${sitio.mensaje_error || 'Error de verificación'}\n`;
            });
        }

        mostrarAlerta(mensaje, offline > 0 ? "warning" : "success");
    }


    function mostrarAlerta(mensaje, tipo = "info") {//// muestra akerta en caso de que haya un sitio offline
    
        const alertasAnteriores = document.querySelectorAll('.alerta-flotante');
        alertasAnteriores.forEach(alerta => alerta.remove());
        
        const alertaDiv = document.createElement('div');
        alertaDiv.className = 'alerta-flotante';
        alertaDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-family: Arial, sans-serif;
            z-index: 10000;
            max-width: 500px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            white-space: pre-line;
            font-size: 14px;
        `;

        const colores = {
            success: '#4CAF50',
            error: '#f44336',
            warning: '#ff9800',
            info: '#2196F3'
        };

        alertaDiv.style.backgroundColor = colores[tipo] || colores.info;
        alertaDiv.textContent = mensaje;
        
        document.body.appendChild(alertaDiv);

        setTimeout(() => {
            if (alertaDiv.parentNode) {
                alertaDiv.parentNode.removeChild(alertaDiv);
            }
        }, 8000);
    }


    async function actualizarResumen() { ////////// actualiza la lista de resumen general ////////////
        try {
            const token = sessionStorage.getItem("token");
            const res = await fetch("http://127.0.0.1:8000/dashboard/admin", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (res.ok) {
                const data = await res.json();
                const statsContainer = document.querySelector(".textos");
                
                statsContainer.innerHTML = `
                    <p>✅Sitios Online:  ${data.sitios_online}</p>
                    <p>❌Sitios Offline:  ${data.sitios_offline}</p>
                    <p>⚠ Sitios con Dominio Vencido:  ${data.dominio_vencido}</p>
                `;
            }
        } catch (err) {
            console.error("Error actualizando estadísticas:", err);
        }
    }




////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    const btnControlID = document.getElementById("buttonVer");
    const idsitioCont = document.getElementById("idSitio");
    const resultadosTextos = document.getElementById("resultados-textos");

    btnControlID.addEventListener("click", async () => {
        await verificarSitioPorId();
    });

//////////////// verifica el sitio especifico teniendo el id 
    async function verificarSitioPorId() {
        const idSitio = idsitioCont.value.trim();
        
        if (!idSitio) {
            mostrarResultado("Por favor, ingrese un ID de sitio válido.", "error");
            return;
        }
        
        try {
            const originalText = btnControlID.textContent;
            btnControlID.textContent = "⏳ Verificando...";
            btnControlID.disabled = true;

            const token = sessionStorage.getItem("token");
            const res = await fetch(`http://127.0.0.1:8000/sitios/verificar/${idSitio}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!res.ok) {
                const errorText = await res.text();
                throw new Error("Error al verificar el sitio: " + errorText);
            }

            const resultado = await res.json();
            mostrarResultadoVerificacion(resultado);
            
        } catch (err) {
            console.error("Error en verificación:", err);
            mostrarResultado(`❌ Error: ${err.message}`, "error");
        } finally {
            btnControlID.textContent = "Verificar estado";
            btnControlID.disabled = false;
        }
    }

    
    function mostrarResultadoVerificacion(resultado) { ////// muetra el resultado de la verificación
        let mensaje = "";
        
        if (resultado.estado === "online") {
            mensaje = `✅ Sitio <strong>${resultado.dominio || resultado.id}</strong> está <strong>ACTIVO</strong>`;
            mensaje += `\n⏱ Tiempo de respuesta: ${resultado.tiempo_respuesta || 'N/A'} ms`;
            mostrarResultado(mensaje, "success");
        } else {
            mensaje = `❌ Sitio <strong>${resultado.dominio || resultado.id}</strong> está <strong>INACTIVO</strong>`;
            mensaje += `\n🔧 Error: ${resultado.mensaje_error || 'Sin conexión'}`;
            mostrarResultado(mensaje, "error");
        }
    }

    function mostrarResultado(mensaje, tipo = "info") {////// muestra resultados en el contenedor 
        
        resultadosTextos.innerHTML = "";
        
        const mensajeDiv = document.createElement('div');
        mensajeDiv.innerHTML = mensaje.replace(/\n/g, '<br>');
        
        /////estilos
        const estilos = {
            success: {
                color: '#155724',
                backgroundColor: '#d4edda',
                borderColor: '#c3e6cb',
                padding: '12px',
                borderRadius: '5px',
                borderLeft: '5px solid #28a745'
            },
            error: {
                color: '#721c24',
                backgroundColor: '#f8d7da',
                borderColor: '#f5c6cb',
                padding: '12px',
                borderRadius: '5px',
                borderLeft: '5px solid #dc3545'
            },
            info: {
                color: '#004085',
                backgroundColor: '#cce5ff',
                borderColor: '#b8daff',
                padding: '12px',
                borderRadius: '5px',
                borderLeft: '5px solid #007bff'
            }
        };
        
        Object.assign(mensajeDiv.style, estilos[tipo] || estilos.info);
        
        resultadosTextos.appendChild(mensajeDiv);
    }

    
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    function formatearTimestamp(timestamp) {
        if (!timestamp) return 'N/A';
        
        try {
            const fecha = new Date(timestamp);
            if (isNaN(fecha.getTime())) {
                return String(timestamp);
            }
            return fecha.toLocaleString('es-ES');
        } catch (error) {
            console.warn('Error formateando timestamp:', timestamp, error);
            return String(timestamp);
        }
    }

    function mostrarError(mensaje) {
        const listaAlertas = document.getElementById('listaAlertas');
        if (listaAlertas) {
            listaAlertas.innerHTML = `<div class="error-alerta">❌ ${mensaje}</div>`;
        }
        console.error(mensaje);
    }

    // async function diagnosticarAlertas() {
    //     try {
    //         const token = sessionStorage.getItem('token');
    //         const response = await fetch('http://127.0.0.1:8000/alertas', {
    //             method: 'GET',
    //             headers: {
    //                 'Authorization': `Bearer ${token}`,
    //                 'Content-Type': 'application/json'
    //             }
    //         });

    //         console.log('🔍 DIAGNÓSTICO DE ALERTAS:');
    //         console.log('Status:', response.status);
            
    //         const rawText = await response.text();
    //         console.log('Respuesta cruda:', rawText);
            
    //         if (response.ok) {
    //             const alertas = JSON.parse(rawText);
    //             console.log('✅ Alertas parseadas:', alertas);
    //             console.log('📊 Tipo de datos:', typeof alertas);
    //             console.log('🔢 Es array?', Array.isArray(alertas));
    //             console.log('📈 Longitud:', alertas.length);
                
    //             if (alertas.length > 0) {
    //                 console.log('👀 Primera alerta ejemplo:', alertas[0]);
    //                 console.log('🗂 Campos de la primera alerta:', Object.keys(alertas[0]));
    //             }
    //         }
            
    //     } catch (error) {
    //         console.error('❌ Error en diagnóstico:', error);
    //     }
    // }

    async function obtenerAlertas() {
        try {
            const token = sessionStorage.getItem('token');
            if (!token) {
                throw new Error('No hay token de autenticación');
            }

            console.log('🔍 Solicitando alertas...');
            const response = await fetch('http://127.0.0.1:8000/alertas', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            console.log('📊 Status de respuesta:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ Error del servidor:', errorText);
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }

            const alertas = await response.json();
            console.log('✅ Alertas recibidas:', alertas);
            console.log('📋 Número de alertas:', alertas.length);
            
            return alertas;
            
        } catch (error) {
            console.error('💥 Error al obtener alertas:', error);
            return [];
        }
    }

    function mostrarAlertasEnHTML(alertas) {
        const listaAlertas = document.getElementById('listaAlertas');
        const contadorAlertas = document.getElementById('contadorAlertas');
        
        if (!listaAlertas) {
            console.error('❌ Elemento listaAlertas no encontrado en el DOM');
            return;
        }
        
        console.log('🎯 Mostrando alertas en HTML. Total:', alertas ? alertas.length : 0);
        
        if (contadorAlertas) {
            contadorAlertas.textContent = alertas ? alertas.length : 0;
            console.log('🔢 Contador actualizado a:', contadorAlertas.textContent);
        }
        
        if (!alertas || alertas.length === 0) {
            console.log('ℹ️ No hay alertas para mostrar');
            listaAlertas.innerHTML = `
                <div class="sin-alertas">
                    ✅ No hay alertas activas
                    <div style="font-size: 0.8em; margin-top: 5px; color: #666;">
                        El sistema no detecta problemas actualmente
                    </div>
                </div>
            `;
            return;
        }
        
        console.log('🛠 Creando HTML para', alertas.length, 'alertas');
        
        const alertasHTML = alertas.map((alerta, index) => {
            console.log(`📝 Procesando alerta ${index + 1}:`, alerta);
            
            const tipo = alerta.tipo_alertas || 'Desconocido';
            const idSitio = alerta.id_sitio || 'N/A';
            const canal = alerta.canal || 'Sistema';
            const timestamp = formatearTimestamp(alerta.timestamp || alerta.fecha_alerta);
            const detalles = alerta.detalles || '';
            
            const esCaida = tipo === 'Caida';
            
            return `
                <div class="alerta-item ${esCaida ? 'alerta-caida' : 'alerta-vencimiento'}">
                    <div class="alerta-icono">
                        ${esCaida ? '⚠️' : '📅'}
                    </div>
                    <div class="alerta-contenido">
                        <strong>${esCaida ? 'Caída del sitio' : 'Vencimiento de dominio'}</strong>
                        <div class="alerta-detalle">
                            Sitio ID: ${idSitio} | 
                            Canal: ${canal} | 
                            Hora: ${timestamp}
                        </div>
                        ${detalles ? `<div class="alerta-detalle-adicional">${detalles}</div>` : ''}
                        <div class="alerta-id" style="font-size: 0.7em; color: #888;">
                            ID: ${alerta.id || 'N/A'} | Fecha: ${alerta.fecha_alerta || 'N/A'}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        listaAlertas.innerHTML = alertasHTML;
        console.log('✅ HTML de alertas generado correctamente');
    }
    async function mostrarTodasLasAlertasTemporalmente() {
        console.log('📋 Mostrando todas las alertas...');
        await mostrarAlertasHoy();
    }

    async function inicializarDashboard() {
        try {
            console.log('🎬 Inicializando dashboard...');
            
            // Cargar datos principales
            await cargarSitios();
            await cargarUltimosSitios();
            await cargarUsuarios();
            await cargarUltimosUsuarios();
            await cargarSitiosOffline();
            
            // Cargar alertas (IMPORTANTE)
            await mostrarAlertasHoy();
            
            console.log('✅ Dashboard inicializado correctamente');
            
        } catch (error) {
            console.error('❌ Error al inicializar dashboard:', error);
        }
    }

    setInterval(cargarSitiosOffline, 30000);
    setInterval(async () => {
        console.log('🔄 Actualizando alertas automáticamente...');
    }, 60000); 

    inicializarDashboard();


    async function mostrarAlertasHoy() {
        try {
            const alertas = await obtenerAlertas();
            mostrarAlertasEnHTML(alertas);
            
        } catch (error) {
            console.error('Error al mostrar alertas:', error);
            mostrarError('Error al cargar alertas: ' + error.message);
        }
    }



    setInterval(cargarSitiosOffline, 30000);
    await cargarSitios();
    await cargarUltimosSitios();
    await cargarUsuarios();
    await cargarUltimosUsuarios();
    cargarSitiosOffline();
    await mostrarAlertasHoy();
    mostrarTodasLasAlertasTemporalmente();
    

    setInterval(cargarSitiosOffline, 30000);



});      