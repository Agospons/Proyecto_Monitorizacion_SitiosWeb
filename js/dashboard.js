import {fetchConAuth} from "./fetchAuth.js";


document.addEventListener("DOMContentLoaded", async () => {
    const usuario = JSON.parse(sessionStorage.getItem("usuario"));
    const saludo = document.getElementById("usuarioSaludos");

    if (usuario) {
        saludo.textContent = `Bienvenido, ${usuario.nombre_completo}`;
    }

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
        <p>✅Sitios Online:  ${data.sitios_online}</p>
        <p>❌Sitios Offline:  ${data.sitios_offline}</p>
        <p> ⚠ Sitios con Domino Vencido:  ${data.dominio_vencido}</p>
        
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
        window.location.href = "index.html";
    });


    const tablaUsuarios = document.getElementById("usuariosTabla");
        // Listar todos los usuarios
    async function cargarUsuarios() {
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

        // Listar últimos 5 usuarios registrados
    async function cargarUltimosUsuarios() {
    try {
        const res = await fetchConAuth("http://127.0.0.1:8000/dashboard/admin");
        if (!res.ok) throw new Error("No se pudieron obtener los últimos usuarios");
        const data = await res.json();

        // ⚠️ Ahora usamos data.ultimos_usuarios
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
}

    const btnHistorial = document.getElementById("btnH");
    const inputIdSitio = document.getElementById("id_sitio");
    const historialTabla = document.getElementById("historialTabla");

    // Función para obtener historial desde el backend
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
        const idSitio = inputIdSitio.value.trim();
        if (!idSitio) {
        alert("Por favor ingrese un ID de sitio");
        return;
        }
        cargarHistorial(idSitio);
    });

    await cargarSitios();
    await cargarUltimosSitios();
    await cargarUsuarios();
    await cargarUltimosUsuarios();
    cargarSitiosOffline();

    setInterval(cargarSitiosOffline, 30000);



});      