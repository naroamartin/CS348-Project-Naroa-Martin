from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine(
    "mysql+pymysql://naroamartin:ZsQzfMRSjCc9j5G08exZ@cs348db.cbq6mk20o7yu.us-east-2.rds.amazonaws.com:3306/cs348db?charset=utf8mb4"
)

Session = sessionmaker(bind=engine)


#UPLOAD A NEW PRODUCT
def upload_product(product_name, product_price, expiration_date,
                   product_quantity, product_machineID):
  try:
    with Session() as session:
      # Inserting the new product into the database
      session.execute(
          text(
              "INSERT INTO Product (NameProduct, Price, ExpirationDate, Quantity, MachineID) VALUES (:name, :price, :expiration, :quantity, :machineID)"
          ), {
              "name": product_name,
              "price": product_price,
              "expiration": expiration_date,
              "quantity": product_quantity,
              "machineID": product_machineID
          })
      session.commit()
    return "Product uploaded successfully"
  except IntegrityError:
    # Handle integrity constraint violation (e.g., duplicate entry)
    return "Error: Product already exists or machine ID does not exist"
  except Exception as e:
    # Handle other exceptions
    return f"Error: {str(e)}"


def load_vending_machines():
  try:
    with engine.begin() as conn:
      result = text("SELECT * FROM VendingMachine")
      result = conn.execute(result)
      vending_machines = [{
          "id": row[0],
          "machine_type": row[1],
          "max_capacity": row[2],
          "working": row[3],
          "num_items": row[4],
          "store_id": row[5]
      } for row in result]
      return vending_machines

  except Exception as e:
    return f"Error: {str(e)}"


#FOR GETTING A MACHINE ID
def get_machine_id(machine_type, store_name):
  with Session() as session:
    query = text("""
            SELECT VendingMachine.id
            FROM VendingMachine 
            JOIN Store ON Store.NameStore = VendingMachine.NameStore
            WHERE VendingMachine.MachineType = :machine_type
            AND Store.NameStore =:store_name
        """)

    result = session.execute(query, {
        "machine_type": machine_type,
        "store_name": store_name
    })
    machine_ids = result.fetchall()

    if machine_ids:
      return machine_ids[0][0]
    else:
      return None


#ADDING A NEW VENING MATCHINE IN THE DATABASE
def upload_Vending_Machine(vm_type, vm_maxcapacity, vm_working, vm_numitems,
                           vm_namestore):
  try:
    with Session() as session:
      # Inserting the new product into the database
      session.execute(
          text(
              "INSERT INTO VendingMachine (MachineType, MaxCapacity,Working, NumItems, NameStore) VALUES (:vm_type, :vm_maxcapacity, :vm_working, :vm_numitems, :vm_namestore)"
          ), {
              "vm_type": vm_type,
              "vm_maxcapacity": vm_maxcapacity,
              "vm_working": vm_working,
              "vm_numitems": vm_numitems,
              "vm_namestore": vm_namestore
          })
      session.commit()
    return "Product uploaded successfully"
  except IntegrityError:
    # Handle integrity constraint violation (e.g., duplicate entry)
    return "Error: Product already exists or machine ID does not exist"
  except Exception as e:
    # Handle other exceptions
    return f"Error: {str(e)}"

#MODIFY NUMBER OF VM IN A STORE
def mod_store_vm_number(num_items, store_name):
  with Session() as session:
    try:
      session.execute(
          text(
              "UPDATE Store SET NumMachines= :num_items WHERE NameStore = :store_name"
          ), {
              "num_items": num_items,
              "store_name": store_name
          })
      session.commit()
    except Exception as e:
      session.rollback()
      # Handle the exception, e.g., log the error
      print("Error:", e)


#GETTING THE NUMBER OF MATCHINES IN A GIVEN STORE
def get_number_of_machines(store_name):
  with Session() as session:
    try:
      query = text(
          "SELECT DISTINCT(Store.NumMachines) FROM Store WHERE Store.NameStore=:store_name;"
      )
      result = session.execute(query, {"store_name": store_name})
      machine_number = result.fetchall()
      if machine_number:
        return machine_number[0][0]
      else:
        return None
    except Exception as e:
      # Handle the exception
      print("Error:", e)
      return None


#GETTING THE MACHINE TYPES IN A GIVEN STORE
def get_machine_types(store_name):
  with Session() as session:
    try:
      query = text(
          "SELECT VendingMachine.MachineType FROM VendingMachine WHERE VendingMachine.NameStore=:store_name;"
      )
      result = session.execute(query, {"store_name": store_name})
      machine_type = result.fetchall()
      if machine_type:
        return [row[0] for row in machine_type]

    except Exception as e:
      # Handle the exception
      print("Error:", e)
      return None

#GETTING ALL PRODUCTS OF A CERTAIN MACHINE IN A STORE
def get_product_types(store_name, machine_type):
  with Session() as session:
    try:
      query = text(
          "SELECT Product.NameProduct FROM Product JOIN VendingMachine ON  VendingMachine.ID= Product.MachineID  WHERE VendingMachine.NameStore= :store_name AND VendingMachine.MachineType= :machine_type;"
      )
      result = session.execute(query, {
          "store_name": store_name,
          "machine_type": machine_type
      })
      product_type = result.fetchall()
      if product_type:
        return [row[0] for row in product_type]
      else:
        return []

    except Exception as e:
      # Handle the exception
      print("Error:", e)
      return None

#GET THE MAXCAPACITY AND ACTUAL NUMBER OF ITEMS IN A MATCHINE
def get_MaxCapacity_NumItems(machine_id):
  with Session() as session:
    try:
      query = text(
          "SELECT VendingMachine.MaxCapacity, VendingMachine.NumItems FROM VendingMachine WHERE VendingMachine.ID=:machine_id;"
      )
      result = session.execute(query, {"machine_id": machine_id})
      capacity = result.fetchone()  # Fetch one row as we expect one result
      if capacity:
        return capacity
      else:
        # You could return a default value like -1
        return -1
    except Exception as e:
      # Handle the exception
      print("Error:", e)
      # You could also raise an exception here instead of returning a default value
      return -1

#MODIFY THE PRODUCT NUMBER IN A VENDING MACHINE
def mod_product_number(num_items, machine_id):
  with Session() as session:
    try:
      session.execute(
          text(
              "UPDATE VendingMachine SET VendingMachine.NumItems=:num_items WHERE VendingMachine.ID = :machine_id"
          ), {
              "num_items": num_items,
              "machine_id": machine_id
          })
      session.commit()
    except Exception as e:
      session.rollback()
      # Handle the exception, e.g., log the error
      print("Error:", e)

#GET THE NUMBER OF PRODUCTS IN A MATCHINE
def get_product_id(product_name, store_name, machine_type):
  with Session() as session:
    query = text("""
      SELECT Product.ID 
      FROM Product  
      JOIN VendingMachine ON VendingMachine.ID = Product.MachineID
      WHERE VendingMachine.MachineType =:machine_type
      AND VendingMachine.NameStore =:store_name
      AND Product.NameProduct= :product_name;
        """)
  
    result = session.execute(query, {
        "machine_type": machine_type,
        "store_name": store_name,
        "product_name": product_name})
    machine_ids = result.fetchall()

    if machine_ids:
      return machine_ids[0][0]
    else:
      return None

def get_product_number(product_name, store_name, machine_type):
  with Session() as session:
    query = text("""
      SELECT Product.Quantity
      FROM Product  
      JOIN VendingMachine ON VendingMachine.ID = Product.MachineID
      WHERE VendingMachine.MachineType =:machine_type
      AND VendingMachine.NameStore =:store_name
      AND Product.NameProduct= :product_name;
        """)

    result = session.execute(query, {
        "machine_type": machine_type,
        "store_name": store_name,
        "product_name": product_name

    })
    machine_ids = result.fetchall()

    if machine_ids:
      return machine_ids[0][0]
    else:
      return None
      

def remove_product(product_id): # ORM
  with Session.begin() as session:
      session.execute(text("DELETE FROM Product WHERE Product.ID = :id"), {"id": product_id})
      session.commit()



vec= get_product_types('Rockade', 'Coffee')
print(vec)
