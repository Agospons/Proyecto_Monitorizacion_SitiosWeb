import {fetchConAuth} from "./fetchAuth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const token = sessionStorage.getItem("token");
    const usuario = JSON.parse(sessionStorage.getItem("usuario"));
    const saludo = document.getElementById("adminSaludo");

    if (usuario) {
      saludo.textContent = `Hola admin ${usuario.nombre_completo}  👋`;
    }

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
            <td>${u.telfono}</td>
            <tr>${u.fecha_alta}</td>
            <td>${u.observaciones}</td>
            <a href="#" class="btn btn-warning btn-sm edit">Edit</a>
            <a href="#" class="btn btn-danger btn-sm delete">Delete</a>
            `;

            tr.dataset.id = u.id;
            tr.dataset.nombre_completo = u.nombre_completo;
            tr.dataset.email = u.email;
            tr.dataset.telfono = u.telfono;
            tr.dataset.fecha_alta = u.fecha_alta;
            tr.dataset.observaciones = u.observaciones;
            tr.dataset.password = u.password;

          tr.addEventListener("click", () => {
              document.getElementById("usuarioId").value = u.id;
              document.getElementById("nombre").value = u.nombre_completo;
              document.getElementById("telefono").value = u.telfono;
              document.getElementById("email").value = u.correo;
              document.getElementById("fechaAlta").value = u.fecha_alta;
              document.getElementById("observaciones").value = u.observaciones;
              document.getElementById("password").value = u.password;

              form.querySelector("button[type='submit']").style.display = "none";
              btnActualizar.style.display = "inline-block";
              btnEliminar.style.display = "inline-block";
          });

          tabla.appendChild(tr);

        });
      } catch (err) {
        alert("Error al cargar usuarios: " + err.message);
      }
}

      
      form.addEventListener("submit", async (e) => {
        e.preventDefault();

      const nuevoUsuario = {
        nombre_completo: document.getElementById("nombre").value,
        email: document.getElementById("email").value,
        telefono: document.getElementById("telefono").value,
        observaciones: document.getElementById("observaciones").value,
        fecha_alta: document.getElementById("fechaAlta").value,
        password: document.getElementById("password").value,
      };

        console.log(nuevoUsuario)

        try {
          const res = await fetch("http://127.0.0.1:8000/usuarios", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(nuevoUsuario)
          });

          if (!res.ok) throw new Error("Error al crear usuario");

          alert("Usuario creado correctamente");
          form.reset();
          await cargarUsuarios();
        } catch (err) {
          alert("Error: " + err.message);
        }
      });
    


    const btnEliminar = document.getElementById("btnEliminar");


    // ACTUALIZAR USUARIOS

    btnActualizar.addEventListener("click", async () => {
    const id = document.getElementById("usuarioId").value;

    const usuarioActualizado = {
      nombre_completo: document.getElementById("nombre").value,
      email: document.getElementById("email").value,
      telefono: parseInt(document.getElementById("telefono").value),
      fecha_alta: document.getElementById("fechaAlta").value,
      observaciones: document.getElementById("observaciones").value
    };

    const passwordValue = document.getElementById("password").value;
    if (passwordValue.trim() !== "") {
      usuarioActualizado.password = passwordValue; // solo si lo escribís
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/usuarios/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(usuarioActualizado)
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error("Error al actualizar usuario: " + errorText);
      }

      alert("Usuario actualizado");
      form.reset();
      btnActualizar.style.display = "none";
      btnEliminar.style.display = "none";
      form.querySelector("button[type='submit']").style.display = "inline-block";
      await cargarUsuarios();
    } catch (err) {
      alert("Error: " + err.message);
      console.error(err);
    }
  });


    //  ELIMINAR USUARIOS 
    btnEliminar.addEventListener("click", async () => {
      const id = document.getElementById("usuarioId").value;
      if (!confirm("¿Seguro que querés eliminar este usuario?")) return;

        try {
        const res = await fetch(`http://127.0.0.1:8000/usuarios/${id}`, {
            method: "DELETE",
            headers: {
            Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) throw new Error("Error al eliminar usuario");

        alert("Usuario eliminado");
        form.reset();
        btnActualizar.style.display = "none";
        btnEliminar.style.display = "none";
        form.querySelector("button[type='submit']").style.display = "inline-block";
        await cargarUsuarios();
        } catch (err) {
        alert("Error: " + err.message);
        }
    });
  await cargarUsuarios();

    });
