export async function fetchConAuth(url, options = {}) {
  const token = sessionStorage.getItem("token");

  if (!options.headers) options.headers = {};
  options.headers.Authorization = `Bearer ${token}`;

  const response = await fetch(url, options);

  if (response.status === 401 || response.status === 403) {
    alert("Tu sesión expiró. Por favor iniciá sesión nuevamente.");
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("usuario");
    window.location.href = "index.html"; 
    return;
  }

  return response;


}
