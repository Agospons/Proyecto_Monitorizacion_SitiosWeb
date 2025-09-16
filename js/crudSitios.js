import {fetchConAuth} from "./fetchAuth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const token = sessionStorage.getItem("token");
    const usuario = JSON.parse(sessionStorage.getItem("usuario"));
    const saludo = document.getElementById("adminSaludo");
    
    document.getElementById("btnHistorial").addEventListener("click", () => {
      window.location.href = "historialSitios.html";
    });

    if (usuario) {
      saludo.textContent = `Hola admin ${usuario.nombre_completo}  👋`;
    }


    const tabla = document.getElementById("sitiosTabla");
    const form = document.getElementById("crudForm");
    


    // Listar sitios
    async function cargarSitios() {
    try {
        const res = await fetchConAuth("http://127.0.0.1:8000/sitios");

        if (!res.ok) throw new Error("No se pudieron obtener sitios");
        const data = await res.json();

        tabla.innerHTML = "";
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
            <button type="button" class="btn btn-warning btn-sm" id="btnHistorial">Ver Historial</button>
            `;

            tr.dataset.id = s.id;
            tr.dataset.dominio = s.dominio;
            tr.dataset.ip = s.ip;
            tr.dataset.id_cliente = s.id_cliente;
            tr.dataset.notas = s.notas;
            tr.dataset.estado = s.estado;
            tr.dataset.ultima_revision = s.ultima_revision;
            tr.dataset.vencimiento_dominio = s.vencimiento_dominio;
            tr.dataset.estado_dominio = s.estado_dominio;
            tr.dataset.fecha_alta = s.fecha_alta;
            tr.dataset.servidor = s.servidor;

        tr.addEventListener("click", () => {
            document.getElementById("sitioid").value = s.id;
            document.getElementById("dominio").value = s.dominio;
            document.getElementById("ip").value = s.ip;
            document.getElementById("id_cliente").value = s.id_cliente;
            document.getElementById("notas").value = s.notas;
            document.getElementById("estado").value = s.estado;
            document.getElementById("ultima_revision").value = s.ultima_revision;
            document.getElementById("vencimiento_dominio").value = s.vencimiento_dominio;
            document.getElementById("estado_dominio").value = s.estado_dominio;
            document.getElementById("fechaAlta").value = s.fecha_alta;
            document.getElementById("servidor").value = s.servidor;

            form.querySelector("button[type='submit']").style.display = "none";
            btnActualizar.style.display = "inline-block";
            btnEliminar.style.display = "inline-block";
          });

          tabla.appendChild(tr);

        });
    } catch (err) {
    alert("Error al cargar sitios web: " + err.message);
    }
}

      
    form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nuevoSitios = {
      dominio: document.getElementById("dominio").value,
      ip: document.getElementById("ip").value,
      id_cliente: parseInt(document.getElementById("id_cliente").value),
      notas: document.getElementById("notas").value,
      estado: document.getElementById("estado").value,
      ultima_revision: document.getElementById("ultima_revision").value,
      vencimiento_dominio: document.getElementById("vencimiento_dominio").value,
      estado_dominio: document.getElementById("estado_dominio").value,
      fecha_alta: document.getElementById("fechaAlta").value,
      servidor: document.getElementById("servidor").value
    };
          console.log(nuevoSitios)

      try {
        const res = await fetch("http://127.0.0.1:8000/sitios", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify(nuevoSitios)
        });

        if (!res.ok) {
          const errorText = await res.text();
          throw new Error("Error al crear el sitio web: " + errorText);
        }
        alert("Sitio web creado correctamente");
        form.reset();
        await cargarSitios();
      } catch (err) {
        alert("Error: " + err.message);
      }
    /////////////////////////////////////////////////////
    //// CREAR LOGS AL CREAR EL SITIO WEB
    const sitioCreado = await resSitio.json();
    const ahora = new Date();
    const timestampHora = ahora.toTimeString().split(" ")[0]; 

    const nuevoLog = {
        id_sitio: sitioCreado.id,
        estado: sitioCreado.estado,
        tiempo_respuesta: 0, 
        timestamp: timestampHora 
    };
    
    const resLog = await fetch("http://127.0.0.1:8000/logeos", { 
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(nuevoLog)
      });

      if (!resLog.ok) {
          const errorText = await resLog.text();
          throw new Error("Error al crear el log: " + errorText);
      }

      alert("Sitio y log creados correctamente");
      form.reset();
      await cargarSitios();


    });
    
    const btnEliminar = document.getElementById("btnEliminar");

    
/////////////////////////////////////////////////////// 
// ACTUALIZAR SITIOS WEB
    
    btnActualizar.addEventListener("click", async () => {
    const id = document.getElementById("sitioid").value;

    const sitioActualizado = {
        ip: document.getElementById("ip").value,
        dominio: document.getElementById("dominio").value,
        id_cliente: document.getElementById("id_cliente").value,
        notas: document.getElementById("notas").value,
        estado: document.getElementById("estado").value,
        ultima_revision: document.getElementById("ultima_revision").value,
        vencimiento_dominio: document.getElementById("vencimiento_dominio").value,
        estado_dominio: document.getElementById("estado_dominio").value,
        fecha_alta: document.getElementById("fechaAlta").value,
        servidor: document.getElementById("servidor").value
    };

    
    try {
      const res = await fetch(`http://127.0.0.1:8000/sitios/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(sitioActualizado)
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error("Error al actualizar usuario: " + errorText);
      }

      alert("Sitio web actualizado");
      form.reset();
      btnActualizar.style.display = "none";
      btnEliminar.style.display = "none";
      form.querySelector("button[type='submit']").style.display = "inline-block";
      await cargarSitios();
    } catch (err) {
      alert("Error: " + err.message);
      console.error(err);
    }


    ////////////////////////////////////////////////
    ///// CREAR LOG AL ACTUALIZAR SITIO
    const sitioCreado = await resSitio.json();
    const ahora = new Date();
    const timestampHora = ahora.toTimeString().split(" ")[0]; // HH:MM:SS

    const nuevoLog = {
        id_sitio: sitioCreado.id,
        estado: sitioCreado.estado,
        tiempo_respuesta: 0, 
        timestamp: timestampHora
    };
    
    const resLog = await fetch("http://127.0.0.1:8000/logeos", { 
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(nuevoLog)
      });

      if (!resLog.ok) {
          const errorText = await resLog.text();
          throw new Error("Error al crear el log: " + errorText);
      }

      alert("Sitio y log actualizados correctamente");
      form.reset();
      await cargarSitios();

  });


  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  ELIMINAR SITIOS 
    btnEliminar.addEventListener("click", async () => {
      const id = document.getElementById("sitioid").value;
      if (!confirm("¿Seguro que querés eliminar este Sitio web?")) return;

        try {
        const res = await fetch(`http://127.0.0.1:8000/sitios/${id}`, {
            method: "DELETE",
            headers: {
            Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) throw new Error("Error al eliminar sitio web");

        alert("Sitio Web eliminado");
        form.reset();
        btnActualizar.style.display = "none";
        btnEliminar.style.display = "none";
        form.querySelector("button[type='submit']").style.display = "inline-block";
        await cargarSitios();
        } catch (err) {
        alert("Error: " + err.message);
        }
    });
  await cargarSitios();

    });



