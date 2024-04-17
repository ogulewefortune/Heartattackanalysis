document.querySelectorAll('.toggleButton').forEach(function(button) {
    button.addEventListener('click', function() {
      var plotId = this.textContent.trim().replace(' ', '') + 'Plot';
      var plotDiv = document.getElementById(plotId);
      var isVisible = plotDiv.style.display === 'block';
  
      // Hide all plots
      document.querySelectorAll('.plot').forEach(function(plot) {
        plot.style.display = 'none';
      });
  
      // Show/hide the clicked plot
      plotDiv.style.display = isVisible ? 'none' : 'block';
    });
  });
  