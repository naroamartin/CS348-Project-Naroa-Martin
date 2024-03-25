from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine("mysql+pymysql://naroamartin:ZsQzfMRSjCc9j5G08exZ@cs348db.cbq6mk20o7yu.us-east-2.rds.amazonaws.com:3306/cs348db?charset=utf8mb4")

Session = sessionmaker(bind=engine)

def upload_product(product_name, product_price, expiration_date, product_quantity, product_machineID):
  try:
      with Session() as session:
          # Inserting the new product into the database
          session.execute(
              text("INSERT INTO Product (NameProduct, Price, ExpirationDate, Quantity, MachineID) VALUES (:name, :price, :expiration, :quantity, :machineID)"),
              {"name": product_name, "price": product_price, "expiration": expiration_date, "quantity": product_quantity, "machineID": product_machineID}
          )
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
          vending_machines = [{"id": row[0], "machine_type": row[1], "max_capacity": row[2], "working": row[3], "num_items": row[4], "store_id": row[5]} for row in result]
          return vending_machines

  except Exception as e:
      return f"Error: {str(e)}"


#FOR GETTING CITY NAMES WHEN THE TYPE IS SELECTED
def get_city(machine_type):
  with Session() as session:
      query = text("""
        SELECT DISTINCT(Store.City)
        FROM Store 
        JOIN VendingMachine ON Store.NameStore = VendingMachine.NameStore
        WHERE VendingMachine.MachineType =:machine_type;
      """)

      result = session.execute(query, {"machine_type": machine_type})
      machine_types = result.fetchall()

      if machine_types:
          return [row[0] for row in machine_types]  # Return a list of machine IDs
      else:
          return None


#FOR GETTING STORE NAMES WHEN THE TYPE AND THE CITY ARE SELECTED
def get_store(machine_type, city):
  with Session() as session:
      query = text("""
          SELECT DISTINCT(Store.NameStore)
          FROM Store 
          JOIN VendingMachine ON Store.NameStore = VendingMachine.NameStore
          WHERE VendingMachine.MachineType = :machine_type
          AND Store.City = :city
      """)

      result = session.execute(query, {"machine_type": machine_type, "city": city})
      store_names = result.fetchall()

      if store_names:
          return [row[0] for row in store_names]  # Return a list of store_names
      else:
          return None

#FOR GETTING A MACHINE ID 
def get_machine_id(machine_type, city, store_name):
    with Session() as session:
        query = text("""
            SELECT VendingMachine.id
            FROM VendingMachine 
            JOIN Store ON Store.NameStore = VendingMachine.NameStore
            WHERE VendingMachine.MachineType = :machine_type
            AND Store.City = :city
            AND Store.NameStore = :store_name
        """)

        result = session.execute(query, {"machine_type": machine_type, "city": city, "store_name": store_name})
        machine_ids = result.fetchall()

        if machine_ids:
            return [row[0] for row in machine_ids]  # Return a list of machine IDs
        else:
            return None


def upload_Vending_Machine(vm_type, vm_maxcapacity, vm_working, vm_numitems, vm_namestore):
  try:
      with Session() as session:
          # Inserting the new product into the database
          session.execute(
              text("INSERT INTO VendingMachine (MachineType, MaxCapacity,Working, NumItems, NameStore) VALUES (:vm_type, :vm_maxcapacity, :vm_working, :vm_numitems, :vm_namestore)"),
              {"vm_type": vm_type, "vm_maxcapacity": vm_maxcapacity, "vm_working": vm_working, "vm_numitems": vm_numitems, "vm_namestore": vm_namestore}
          )
          session.commit()
      return "Product uploaded successfully"
  except IntegrityError:
      # Handle integrity constraint violation (e.g., duplicate entry)
      return "Error: Product already exists or machine ID does not exist"
  except Exception as e:
      # Handle other exceptions
      return f"Error: {str(e)}"

def mod_store_vm_number(num_items, store_name):
  with Session() as session:
      try:
          session.execute(
              text("UPDATE Store SET NumMachines= :num_items WHERE NameStore = :store_name"),
              {"num_items": num_items, "store_name": store_name}
          )
          session.commit()
      except Exception as e:
          session.rollback()
          # Handle the exception, e.g., log the error
          print("Error:", e)

def get_number_of_machines(store_name):
  with Session() as session:
      try:
          query = text("SELECT DISTINCT(Store.NumMachines) FROM Store WHERE Store.NameStore=:store_name;")
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
