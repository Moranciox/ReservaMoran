// main.js
document.addEventListener("DOMContentLoaded", function () {
  // Obtén una referencia al botón y al div de contenido dinámico
  const mostrarHTMLBtn = document.getElementById("mostrarHTMLBtn");
  const contenidoDinamico = document.getElementById("contenidoDinamico");
  
  // Asocia un evento de clic al botón
  mostrarHTMLBtn.addEventListener("click", function () {
    // Realiza una solicitud GET para cargar el contenido del archivo de plantilla
    fetch("/formBus/")
      .then(response => response.text())
      .then(html => {
        // Asigna el HTML cargado al div de contenido dinámico
        contenidoDinamico.innerHTML = html;
      })
      .catch(error => {
        console.error("Error al cargar el archivo de plantilla:", error);
      });
  });
});


