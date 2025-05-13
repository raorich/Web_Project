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
});