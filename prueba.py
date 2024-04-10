<script>
  document.getElementById('vmForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    var formData = new FormData(this); // Get form data

    // Display selected store name and machine type
    document.getElementById('storeName').innerText = 'Store Name: ' + formData.get('store_name');
    document.getElementById('machineType').innerText = 'Machine Type: ' + formData.get('machine_type');

    // Display selected information based on checkboxes
    var checkboxes = document.querySelectorAll('.info-checkbox');
    checkboxes.forEach(function(checkbox) {
      var checkboxId = checkbox.id.split('-')[1];
      var infoElement = document.getElementById('info' + checkboxId.charAt(0).toUpperCase() + checkboxId.slice(1));
      if (checkbox.checked) {
        infoElement.innerText = checkbox.nextElementSibling.innerText + ':';

      } else {
        infoElement.innerText = '';
      }
    });

    // Show report section
    document.getElementById('reportSection').style.display = 'block';
  });

</script>






