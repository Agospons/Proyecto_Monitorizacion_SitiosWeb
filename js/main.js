import { authService } from "./authService.js";


document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".form");
    const container = document.querySelector(".login");

    const token = sessionStorage.getItem("token");
    const usuario = JSON.parse(sessionStorage.getItem("usuario") || "{}");

    if (token) {

        fetch("http://127.0.0.1:8000/socios", {
            headers: { Authorization: `Bearer ${token}` }
        })
            .then(res => {
            if (!res.ok) throw new Error("Token expirado");
            
            container.innerHTML = `<h2>Sesión activa</h2><p>Redirigiendo...</p>`;
            const destino = "dashboard.html";
            setTimeout(() => (window.location.href = destino), 1000);
            })
            .catch(err => {
            
            sessionStorage.removeItem("token");
            sessionStorage.removeItem("usuario");
            console.warn("Token inválido o expirado. Sesión limpia.");
            });

    return;
    }


    loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
        const response = await authService.login(email, password);
        console.log("Respuesta del backend:", response);

        sessionStorage.setItem("token", response.token);
        sessionStorage.setItem("usuario", JSON.stringify(response.usuario));
        console.log("Usuario guardado en sessionStorage:", response.usuario);

        const usuario = JSON.parse(sessionStorage.getItem("usuario"));

        alert(`¡Bienvenido ${usuario.nombre_completo}👋!`);
        const destino = "dashboard.html";
        window.location.href = destino;
        
    } catch (err) {
        alert("Error de autenticación: " + err.message);
    }
    });
    });