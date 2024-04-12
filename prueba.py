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

<script>
    // Function to fetch product information from Flask server
    function fetchProductInfo() {
        // Make an AJAX request to the Flask route
        fetch('/reportproduct', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_name: 'YourProductName',
                machine_type: 'YourMachineType',
                product_info: ['product_id', 'product_price', 'expiration_date', 'product_quantity']
            })
        })
        .then(response => response.json())
        .then(data => {
            // Call a function to render the product information in the HTML
            renderProductInfo(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Function to render product information in HTML
    function renderProductInfo(products) {
        // Get the div element where you want to display the product information
        const productInfoDiv = document.getElementById('product-info');

        // Clear the previous content of the div
        productInfoDiv.innerHTML = '';

        // Loop through the product information and create HTML elements to display it
        for (const store in products) {
            if (Object.hasOwnProperty.call(products, store)) {
                const data = products[store];
                const table = document.createElement('table');
                const thead = document.createElement('thead');
                const tbody = document.createElement('tbody');

                // Create table headers
                const headerRow = document.createElement('tr');
                for (const key in data) {
                    if (Object.hasOwnProperty.call(data, key)) {
                        const th = document.createElement('th');
                        th.textContent = key;
                        headerRow.appendChild(th);
                    }
                }
                thead.appendChild(headerRow);
                table.appendChild(thead);

                // Create table rows
                const bodyRow = document.createElement('tr');
                for (const key in data) {
                    if (Object.hasOwnProperty.call(data, key)) {
                        const td = document.createElement('td');
                        td.textContent = data[key];
                        bodyRow.appendChild(td);
                    }
                }
                tbody.appendChild(bodyRow);
                table.appendChild(tbody);

                // Append the table to the productInfoDiv
                productInfoDiv.appendChild(table);
            }
        }
    }

    // Call the fetchProductInfo function when the page loads
    fetchProductInfo();
</script>





