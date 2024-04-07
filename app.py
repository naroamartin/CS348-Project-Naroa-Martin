from flask import Flask, render_template, request

from database import upload_Vending_Machine, mod_store_vm_number, get_number_of_machines, get_machine_types,get_machine_id,get_product_types,upload_product,get_MaxCapacity_NumItems,mod_product_number, get_product_id,get_product_number,remove_product,delete_vending_machine, update_veding_machine, update_product,get_quantity,get_products, get_price_expiration, call_vm_info



app = Flask(__name__) 


@app.route("/")
def home():
  return render_template ("home.html")

@app.route('/add') 
def add():
    return render_template('add.html')




@app.route("/add_vm", methods=['POST'])
def add_vm():
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
      return render_template("add_message-VM1.html")
    elif machine_type in vect: 
      return render_template("add_message-VM2.html")





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
          return render_template("add_message1.html")
         
        elif totalcapacity>capacity[0]:
          return render_template("add_message2.html")
        
      elif product_name in products:
         return render_template("add_message3.html")
      
    elif machine_type not in vect: 
       return render_template("add_message4.html")




@app.route("/delete_product", methods=['POST'])
def delete_product():
  
  machine_type = request.form['machine_type']
  store_name =request.form['store_name']
  product_name =request.form['product_name']

  vect=get_product_types(store_name, machine_type)

  if product_name in vect: 
    product_id=get_product_id(product_name,store_name ,machine_type)
    machine_id=get_machine_id(machine_type, store_name)
    
    if product_id is not None:
      items_product= get_product_number(product_name,store_name ,machine_type)
      items=get_MaxCapacity_NumItems(machine_id)
      num_items_vm=items[1]
      total_items= num_items_vm- items_product
      mod_product_number(total_items, machine_id)
      
      remove_product(product_id)
      return render_template("delete_message1.html")
      
    elif product_ is None: 
      return render_template("delete_message2.html")
  elif product_name not in vect:
      return render_template("delete_message3.html")



@app.route("/delete_machine", methods=['POST'])
def delete_machine():
    machine_type = request.form['machine_type']
    store_name = request.form['store_name']
    vect = get_machine_types(store_name)

    if machine_type in vect:
        number = get_number_of_machines(store_name)
        if number is not None:
            number -= 1
            mod_store_vm_number(number, store_name)
          
        delete_vending_machine(store_name, machine_type)
        return  render_template("delete_message-VM1.html")
    elif machine_type not in vect:
        return render_template("delete_message-VM2.html")


@app.route("/edit_vm", methods=['POST'])
def edit_vm():
    store_name = request.form['store_name']
    machine_type= request.form['machine_type']
    maxcapacity = request.form['maxcapacity']
    working = request.form['working']
  
    machine_id=get_machine_id(machine_type,store_name)
    capacity=get_MaxCapacity_NumItems(machine_id)
    
   
    vect=get_machine_types(store_name)

    if machine_type in vect:
      items= capacity[1]

      if maxcapacity.strip():
        maxcapacity= int(maxcapacity)
      else: 
        maxcapacity= capacity[0]


      if maxcapacity >= items:
    
        update_veding_machine(store_name,machine_type,maxcapacity,working)
        return render_template("edit_message1.html")
        
      elif maxcapacity < items:
        return render_template("edit_message2.html")
        
    elif machine_type not in vect: 
      return render_template("edit_message3.html")
      
    




@app.route("/edit_product", methods=['POST'])
def edit_product():
    store_name = request.form['store_name']
    product_name = request.form['product_name']
    machine_type= request.form['machine_type']
    price = request.form['price']
    expiration_date = request.form['expiration_date']
    quantity = request.form['quantity']
  
    vect=get_machine_types(store_name)
    machine_id=get_machine_id(machine_type,store_name)
  
    if quantity.strip():  
      quantity = int(quantity)
    else: 
      quantity = get_quantity(product_name,machine_id)

    price1,date = get_price_expiration(store_name, machine_type, product_name)
  
    if price == '':
      price = price1
    if expiration_date == '':
      expiration_date = date
  

    if machine_id is not None and machine_type in vect and quantity is not None:

      products = get_product_types(store_name,machine_type)
      if product_name in products: 
        
        capacity=get_MaxCapacity_NumItems(machine_id)
        actual_quantity= get_quantity(product_name,machine_id)
        subs= quantity - actual_quantity
        totalcapacity= capacity[1]+subs
        if totalcapacity<=capacity[0]:
          update_product(store_name, product_name, machine_type, price, expiration_date, quantity)
          mod_product_number(totalcapacity, machine_id)
          return render_template("edit_message_p1.html")

        elif totalcapacity>capacity[0]:
          return render_template("edit_message_p2.html")
      elif product_name not in products or quantity is None :
        return render_template("edit_message_p3.html")

    elif machine_type not in vect: 
      return render_template("edit_message_p4.html")


@app.route("/show_products", methods=['POST'])
def display_books():
    store_name = request.form['store_name']
    machine_type = request.form['machine_type']
    products,price,date = get_products(store_name, machine_type)
    # Assuming you have a display.html template where you want to show the results
    return render_template("info.html", products=products,price=price,date=date)


@app.route("/reportvm", methods=['POST'])
def reportvm():
    store_name = request.form['store_name']
    machine_type = request.form['machine_type']
    
    vect=get_machine_types(store_name)
    if machine_type in vect: 
      result = call_vm_info(store_name, machine_type,vm_info)
    return result,store_name,machine_type #tengo que arreglar esto 


  
@app.route('/delete')
def delete():
      return render_template('delete.html')
  
@app.route('/edit')
def edit():
      return render_template('edit.html')
  
@app.route('/info')
def info():
    return render_template('info.html')
  
@app.route('/report_options')
def report_options():
    return render_template('report_options.html')

@app.route('/report_product')
def report_product():
    return render_template('report_product.html')

@app.route('/report_vm')
def report_vm():
    return render_template('report_vm.html')

@app.route('/report_general')
def report_general():
    return render_template('report_general.html')





  
if __name__ == '__main__':        
  app.run(host='0.0.0.0', debug=True)