from flask import Flask, render_template, request

from database import upload_Vending_Machine, mod_store_vm_number, get_number_of_machines, get_machine_types,get_machine_id,get_product_types,upload_product,get_MaxCapacity_NumItems,mod_product_number



app = Flask(__name__) 


@app.route("/")
def home():
  return render_template ("home.html")

@app.route('/add')
def add():
    return render_template('add.html')



@app.route("/add_store", methods=['POST'])
def add_store():
    machine_type = request.form['machine_type']
    MaxCapacity = request.form['MaxCapacity']
    status = request.form['status']
    store_name = request.form['store_name']
  
    vect=get_machine_types(store_name)
    if machine_type not in vect:
        
      number = get_number_of_machines(store_name)
      if number is not None:
          number += 1
          mod_store_vm_number(number, store_name)
    
      if status== "Working":
        upload_Vending_Machine(machine_type, MaxCapacity,1,0, store_name)
      if status== "Not Working":
        upload_Vending_Machine(machine_type, MaxCapacity,1,0, store_name)
      return 'Store added successfully'
    elif machine_type in vect: 
      return 'The store already has that type of machine'




@app.route("/add_product", methods=['POST'])
def add_product():
    machine_type = request.form['machine_type']
    store_name = request.form['store_name']
    product_name = request.form['product_name']
    product_price = request.form['product_price']
    expiration_date = request.form['expiration_date']
    quantity = int(request.form['quantity']) 
  
    vect=get_machine_types(store_name)
    machine_id=get_machine_id(machine_type,store_name)
    
    if machine_id is not None and machine_type in vect:

      products = get_product_types(store_name,machine_type)
      if product_name not in products: 
        capacity=get_MaxCapacity_NumItems(machine_id)
        totalcapacity= capacity[1]+quantity
        print(totalcapacity)
        if totalcapacity<=capacity[0]:
          upload_product(product_name, product_price, expiration_date, quantity, machine_id)
          mod_product_number(totalcapacity, machine_id)
          return 'Product added successfully'
         
        elif totalcapacity>capacity[0]:
          return 'There is not enough space in the machine'
      elif product_name in products:
        return 'The product already exists'
      
    elif machine_type not in vect: 
      return 'The machine does not exist or there is not that type of machine in that store'


@app.route('/delete')
def delete():
      return render_template('delete.html')
  
@app.route('/edit')
def edit():
      return render_template('edit.html')
  
@app.route('/info')
def info():
    return render_template('info.html')



  
if __name__ == '__main__':        
  app.run(host='0.0.0.0', debug=True)