import {fetchConAuth} from "./fetchAuth.js";


document.addEventListener("DOMContentLoaded", async () => {
    const usuario = JSON.parse(sessionStorage.getItem("usuario"));
    const saludo = document.getElementById("usuarioSaludos");

    if (usuario) {
      saludo.textContent = `Bienvenido, ${usuario.nombre_completo}`;
    }

    const statsContainer = document.querySelector(".textos");
    const usuaTabla = document.getElementById("usuariosTabla")
    const token = sessionStorage.getItem("token");
    
    

    // Cambiar adminSaludo por usuarioSaludo
    // const saludo = document.getElementById("usuarioSaludo");

    // if (usuario) {
    //     saludo.textContent = `Hola ${usuario.nombre_completo} 👋`;
    // }

    try {
        const res = await fetch("http://127.0.0.1:8000/dashboard/admin", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
        });

    const data = await res.json();

    statsContainer.innerHTML = `
        <p>Sitios Online:  ${data.sitios_online}</p>
        <p>Sitios Offline:  ${data.sitios_offline}</p>
        <p>Sitios con Domino Vencido:  ${data.dominio_vencido}</p>
        
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
        alert("Error al cargar usuarios: " + err.message);
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
        alert("Error al cargar últimos usuarios: " + err.message);
    }
    }


    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    const tablaSitios = document.getElementById("sitiosTabla");
        // Listar todos los sitios
    async function cargarSitios() {
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

        // Listar últimos 5 sitios registrados
    async function cargarUltimosSitios() {
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
            <td>${s.estado}</td>
            <td>${s.ultima_revision}</td>
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


    await cargarSitios();
    await cargarUltimosSitios();
    await cargarUsuarios();
    await cargarUltimosUsuarios();

    }
    
);      