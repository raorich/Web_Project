document.addEventListener('DOMContentLoaded', function () {
  const filterButtons = document.querySelectorAll('.filter-btn');

  filterButtons.forEach(button => {
    button.addEventListener('click', function () {
      // Remover clases de todos los botones
      filterButtons.forEach(btn =>
        btn.classList.remove('bg-amber-500')
      );

      // Añadir clases al botón clickeado
      this.classList.add('bg-amber-500');
    });
  });    
  if (window.location.pathname === '/perfil/') {
    document.getElementById('open-form').addEventListener('click', function(event) {
      event.preventDefault();
      document.getElementById('form-modal').style.display = 'block';
      document.getElementById('overlay').style.display = 'block';
    });
  
    document.getElementById('close-form').addEventListener('click', function() {
        document.getElementById('form-modal').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    });
  }
});