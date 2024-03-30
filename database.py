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


#REMOVE THE PRODUCT NUMBER IN A VENDING MACHINE
def remove_product(product_id): # ORM
  with Session.begin() as session:
      session.execute(text("DELETE FROM Product WHERE Product.ID = :id"), {"id": product_id})
      session.commit()


#DELETE A VENDING MACHINE
def delete_vending_machine(store_name,machine_type): # ORM
  with Session.begin() as session:
    machine_id= get_machine_id(machine_type, store_name)
    if machine_id:
      # Delete the products of the store
      session.execute(text("DELETE FROM Product WHERE Product.MachineID = :id"), {"id": machine_id})
      # Delete the Vening Machine
      session.execute(text("DELETE FROM VendingMachine WHERE VendingMachine.ID = :id"), {"id": machine_id})
      

#UPDATE A VENDING MACHINE
def update_veding_machine(store_name, machine_type, max_capacity, working):
  with Session.begin() as session:
      # Prepare the SQL UPDATE statement
      update_statement = "UPDATE VendingMachine SET "
      update = []

      if max_capacity is not None: 
          update.append(f"MaxCapacity = :max_capacity")

      if working is not None and working.isdigit():
          update.append(f"Working = :working")

      update_statement += ", ".join(update)
      update_statement += " WHERE VendingMachine.MachineType = :machine_type AND VendingMachine.NameStore = :store_name"

      session.execute(
          text(update_statement),
          {"store_name": store_name, "machine_type": machine_type, "max_capacity": max_capacity, "working": working}
      )

      session.commit()



#UPDATE A PRODUCT FROM A VENDING MACHINE
def update_product(store_name, product_name, machine_type, price, expiration_date, quantity):
  with Session.begin() as session:
    machine_id = get_machine_id(machine_type, store_name)
    # Prepare the SQL UPDATE statement
    update_statement = """
        UPDATE Product
        SET Price = :price, ExpirationDate = :expiration_date, Quantity = :quantity
        WHERE Product.NameProduct = :product_name AND Product.MachineID = :machine_id
    """

    # Execute the SQL statement with provided parameters
    session.execute(
        text(update_statement),
        {
            "product_name": product_name,
            "machine_id": machine_id,  # Corrected from machine_type
            "price": price,
            "expiration_date": expiration_date,
            "quantity": quantity
        }
    )

    session.commit()


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

#GET THE MAXCAPACITY AND NUMBER ITEMS IN A MATCHINE
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

#GET THE PRODUCT NUMBER IN A VENDING MACHINE
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




def get_quantity(product_name, machine_id):
  with Session() as session:
      try:
          query = text(
              "SELECT Product.Quantity FROM Product WHERE Product.MachineID = :machine_id AND Product.NameProduct = :product_name;"
          )
          result = session.execute(query, {"machine_id": machine_id, "product_name": product_name})
          quantity = result.fetchone()  # Fetch one row as we expect one result
          if quantity:
              return quantity[0]  # Return the quantity value from the fetched row
          else:
              # Return a default value like -1 if no quantity is found
              return -1
      except Exception as e:
          # Handle the exception
          print("Error:", e)
          # Return a default value like -1 in case of any exception
          return -1


#use only for displaying data 
def get_products(store_name,machine_type):
  with Session.begin() as session:
    
      products_query = text("""
          SELECT Product.NameProduct, Product.Price , Product.ExpirationDate 
          FROM Product
          JOIN VendingMachine ON VendingMachine.ID = Product.MachineID
          WHERE VendingMachine.NameStore=:store_name AND VendingMachine.MachineType =:machine_type;
      """)

      result = session.execute(products_query, {"store_name": store_name, "machine_type": machine_type}).fetchall()
      # Extract titles from the result
      products = [row[0] for row in result]
      price= [row[1] for row in result]
      date= [row[2] for row in result]
      return products,price,date


def get_price_expiration(store_name,machine_type,product_name):
  with Session.begin() as session:

      products_query = text("""
          SELECT Product.Price , Product.ExpirationDate 
          FROM Product
          JOIN VendingMachine ON VendingMachine.ID = Product.MachineID
          WHERE VendingMachine.NameStore=:store_name AND VendingMachine.MachineType =:machine_type AND Product.NameProduct =:product_name;;
      """)

      result = session.execute(products_query, {"store_name": store_name, "machine_type": machine_type, "product_name": product_name}).fetchall()
      # Extract titles from the result
      price= [row[0] for row in result]
      date= [row[1] for row in result]
      return price,date




hola= update_veding_machine('Rockade', 'Coffee', 250, None)
print(hola)