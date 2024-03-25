from flask import Flask, render_template, request

from database import upload_Vending_Machine, mod_store_vm_number, get_number_of_machines



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
  
    number = get_number_of_machines(store_name)
    if number is not None:
        number += 1
        mod_store_vm_number(number, store_name)
  
    if status== "Working":
      upload_Vending_Machine(machine_type, MaxCapacity,1,0, store_name)
    if status== "Not Working":
      upload_Vending_Machine(machine_type, MaxCapacity,1,0, store_name)
    return 'Store added successfully'
  
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