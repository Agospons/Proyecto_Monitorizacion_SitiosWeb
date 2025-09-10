import {fetchConAuth} from "./fetchAuth.js";

document.addEventListener("DOMContentLoaded", async () => {



    const token = sessionStorage.getItem("token");
    const usuario = JSON.parse(sessionStorage.getItem("usuario"));
    // Cambiar adminSaludo por usuarioSaludo
    // const saludo = document.getElementById("usuarioSaludo");

    // if (usuario) {
    //     saludo.textContent = `Hola ${usuario.nombre_completo} 👋`;
    // }

    
    document.getElementById("btnU").addEventListener("click", () => {
        window.location.href = "crudClientes.html";
    });

    
    document.getElementById("btnS").addEventListener("click", () => {
        window.location.href = "crudSitios.html";
    });
    const form = document.getElementById("crudForm");
    const tabla = document.getElementById("usuariosTabla");

    // Listar usuarios
    async function cargarUsuarios() {
    try {
        const res = await fetchConAuth("http://127.0.0.1:8000/usuarios");

        if (!res.ok) throw new Error("No se pudieron obtener usuarios");
        const data = await res.json();

        tabla.innerHTML = "";
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
            tabla.appendChild(tr);
        });
    } catch (err) {
        alert("Error al cargar usuarios: " + err.message);
    }
}

    

      await cargarUsuarios();

});      