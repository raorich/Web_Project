document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
      button.addEventListener('click', function() {
        // Remover clase active de todos
        filterButtons.forEach(btn => btn.classList.remove('active'));
        
        // Añadir al botón clickeado
        this.classList.add('active');
        
        // Obtener valor del filtro
        const filterValue = this.textContent.trim();
        console.log('Productos filtrados:', filterValue);
        /*
        // Lógica de filtrado (ejemplo con Fetch API)
        fetch(`/filtrar-productos/?categoria=${filterValue}`)
          .then(response => response.json())
          .then(data => {
            // Actualizar la vista con los productos filtrados
            console.log('Productos filtrados:', data);
          });
        */
      });
    });
  });