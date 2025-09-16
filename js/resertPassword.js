// const nodemailer = require('nodemailer');
// const crypto = require('crypto'); // Para generar un token único

// // Configuración del transporte de correo
// const transporter = nodemailer.createTransport({
//   service: 'gmail', // Puedes usar otro servicio como Outlook, Yahoo, etc.
//   auth: {
//     user: 'tu_correo@gmail.com', // Tu correo electrónico
//     pass: 'tu_contraseña_de_aplicación' // Contraseña de aplicación (no la contraseña normal)
//   }
// });

// // Función para enviar el correo de recuperación
// async function enviarCorreoRecuperacion(emailUsuario) {
//   try {
//     // Generar un token único
//     const token = crypto.randomBytes(32).toString('hex');

//     // URL de recuperación (ajusta según tu frontend)
//     const urlRecuperacion = `https://tu-dominio.com/recuperar-contraseña?token=${token}`;

//     // Configuración del correo
//     const mailOptions = {
//       from: '"Soporte" <tu_correo@gmail.com>', // Remitente
//       to: emailUsuario, // Correo del destinatario
//       subject: 'Recuperación de contraseña',
//       html: `
//         <h1>Recuperación de contraseña</h1>
//         <p>Haz clic en el siguiente enlace para restablecer tu contraseña:</p>
//         <a href="${urlRecuperacion}">${urlRecuperacion}</a>
//         <p>Si no solicitaste este cambio, ignora este correo.</p>
//       `
//     };

//     // Enviar el correo
//     await transporter.sendMail(mailOptions);
//     console.log('Correo enviado correctamente.');
//   } catch (error) {
//     console.error('Error al enviar el correo:', error);
//   }
// }

// // Llamada de ejemplo
// enviarCorreoRecuperacion('usuario@ejemplo.com');
