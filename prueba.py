<body>
   <!-- Edit a Store-->
  <div class="container text-center">
    <div class="row">
      <!-- First Column -->
      <div class="col-md-6">
        <div class="wrapper wrapper1">
          <div class="header"> 
            <h1>Edit Vending Machine</h1>
          </div>

          <div class= "content">
            <div class= "mx-4 mt-4">
              <div id="edit-vm">
                <form method="post" action="/display_books">
                  <div class="row g-2 m-4">
                    <div class="col-md">
                      <label for="store_name" class="form-label">Store Name</label>
                      <input type="text" class="form-control" id="store_name" name="store_name" placeholder="Enter a Name">
                    </div>
                    <div class="col-md">
                      <p>Select Type</p>
                      <select id="machine_type" name="machine_type" class="form-select mb-1" aria-label="Default select example">
                        <option value="Food">Food</option>
                        <option value="Coffee">Coffee</option>
                        <option value="Drink">Drink</option>
                        <option value="Snacks">Snack</option>
                      </select> 
                    </div>
                    <div class="col-md">
                      <!-- New Column -->
                      <label for="product_name" class="form-label">Product Name</label>
                      <input type="text" class="form-control" id="product_name" name="product_name" placeholder="Enter a Name">
                    </div>
                    <div class="col-md">
                      <button class="button" type="submit">Find</button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Second Column -->
      <div class="col-md-6">
        <div class="wrapper wrapper2">
          <div class="header"> 
            <h1>Edit Product</h1>
          </div>

          <div class= "content">
            <div class= "mx-4 ">
              <div id="edit-product">
                
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</body>






