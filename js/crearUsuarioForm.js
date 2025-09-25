document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector(".formC");
    const loginError = document.getElementById("loginError");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value.trim();
        const telefono = document.getElementById("telefono").value.trim();
        const email = document.getElementById("emailC").value.trim();
        const password1 = document.getElementById("password1").value;
        const password2 = document.getElementById("password2").value;

        if (!validarFormulario(nombre, telefono, email, password1, password2)) {
            return;
        }

        const btn = document.querySelector(".btnC");
        const originalText = btn.textContent;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creando...';
        btn.disabled = true;

        try {
            const nuevoUsuario = {
                nombre_completo: nombre,
                telefono: parseInt(telefono), 
                email: email,
                password: password1,
                fecha_alta: new Date().toISOString().split('T')[0], 
                observaciones: ""
            };

            console.log("Enviando usuario:", nuevoUsuario);

            const res = await fetch(`http://127.0.0.1:8000/usuarios`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(nuevoUsuario)
            });

            const responseData = await res.json();

            if (res.ok) {
                alert("Usuario creado correctamente", "success");
                form.reset();
                
                // Redirigir después de 2 segundos
                setTimeout(() => {
                    window.location.href = "index.html";
                }, 2000);
            } else {
                throw new Error(responseData.detail || "Error al crear usuario");
            }
        } catch (err) {
            console.error("Error completo:", err);
            alert("Error: " + err.message, "error");
        } finally {
            // Restaurar botón
            btn.textContent = originalText;
            btn.disabled = false;
        }
    });

    document.getElementById("password2").addEventListener("input", function() {
        const password1 = document.getElementById("password1").value;
        const password2 = this.value;
        
        if (password2 && password1 !== password2) {
            this.style.borderColor = "red";
        } else {
            this.style.borderColor = "";
        }
    });
});

function validarFormulario(nombre, telefono, email, password1, password2) {
    const loginError = document.getElementById("loginError");
    
    loginError.style.display = "none";
    loginError.textContent = "";
    
    if (nombre.length < 2 || nombre.length > 50) {
        alert("El nombre debe tener entre 2 y 50 caracteres", "error");
        return false;
    }
    
    if (!telefono || telefono.length < 7 || isNaN(telefono)) {
        alert("Ingrese un número de teléfono válido", "error");
        return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Ingrese un email válido", "error");
        return false;
    }
    
    if (password1.length < 6) {
        alert("La contraseña debe tener al menos 6 caracteres", "error");
        return false;
    }
    
    if (password1 !== password2) {
        alert("Las contraseñas no coinciden", "error");
        return false;
    }
    
    return true;
}

function mostrarMensaje(mensaje, tipo) {
    const loginError = document.getElementById("loginError");
    loginError.textContent = mensaje;
    loginError.className = tipo === "error" ? "error" : "success";
    loginError.style.display = "block";
    
    if (tipo === "success") {
        setTimeout(() => {
            loginError.style.display = "none";
        }, 5000);
    }
}