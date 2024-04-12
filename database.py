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




def call_vm_info(store_name, machine_type,vm_info): #PREPARE STATEMENT 
  with engine.begin() as conn:

    #3 options selected 
    if "max_capacity" in vm_info and "working" in vm_info and "number_items" in vm_info:
      stmt = text("SELECT VendingMachine.MaxCapacity, VendingMachine.Working, VendingMachine.NumItems FROM VendingMachine WHERE VendingMachine.NameStore =:store_name AND VendingMachine.MachineType =:machine_type ")
      
    #2 options selected 
    elif "max_capacity" in vm_info and "working" in vm_info:
      stmt = text("SELECT VendingMachine.MaxCapacity, VendingMachine.Working FROM VendingMachine WHERE VendingMachine.NameStore =:store_name AND VendingMachine.MachineType =:machine_type ")

    elif "max_capacity" in vm_info and "number_items" in vm_info: 
      stmt = text("SELECT VendingMachine.MaxCapacity, VendingMachine.NumItems FROM VendingMachine WHERE VendingMachine.NameStore =:store_name AND VendingMachine.MachineType =:machine_type ")
    
    elif "working" in vm_info and "number_items" in vm_info: 
      stmt = text("SELECT VendingMachine.Working, VendingMachine.NumItems FROM VendingMachine WHERE VendingMachine.NameStore =:store_name AND VendingMachine.MachineType =:machine_type ")
      
    #1 options selected 
    elif "max_capacity" in vm_info:
      stmt = text("SELECT VendingMachine.MaxCapacity FROM VendingMachine WHERE VendingMachine.NameStore =:store_name AND VendingMachine.MachineType =:machine_type ")
      
    elif "working" in vm_info: 
        stmt = text("SELECT VendingMachine.Working FROM VendingMachine WHERE VendingMachine.NameStore =:store_name AND VendingMachine.MachineType =:machine_type ")
      
    elif "number_items" in vm_info:
        stmt = text("SELECT VendingMachine.NumItems FROM VendingMachine WHERE VendingMachine.NameStore =:store_name AND VendingMachine.MachineType =:machine_type ")

    result = conn.execute(stmt, {"store_name": store_name, "machine_type": machine_type})  
  
    info = [list(row) for row in result]  # Convert each tuple into a list


    return info


def call_product_info(product_name, machine_type, product_info):
  with engine.begin() as conn:
      columns = []
      for info in product_info:
          if info == "product_id":
            columns.append("Product.ID")
          elif info == "product_price":
            columns.append("Product.Price")
          elif info == "expiration_date":
            columns.append("Product.ExpirationDate")
          elif info == "product_quantity":
            columns.append("Product.Quantity")

      if columns:
          column_str = ', '.join(columns)
          stmt = text(f"SELECT Store.NameStore,{column_str} FROM Product JOIN VendingMachine ON Product.MachineID=VendingMachine.ID JOIN Store ON Store.NameStore= VendingMachine.NameStore WHERE Product.NameProduct =:product_name AND VendingMachine.MachineType = :machine_type")

      result = conn.execute(stmt, {"product_name": product_name, "machine_type": machine_type})
      info = [list(row) for row in result]

      #select min price and teh store in which is sell 
      sql_min_price = text("SELECT Product.Price, Store.NameStore  FROM Product JOIN VendingMachine ON VendingMachine.ID = Product.MachineID JOIN Store ON Store.NameStore = VendingMachine.NameStore WHERE Product.NameProduct = :product_name AND Product.Price = (SELECT MIN(Price) FROM Product WHERE Product.NameProduct = :product_name);")
    
      min_price1 = conn.execute(sql_min_price, {"product_name": product_name})
      min_price = [{"Store": row[1], "Min Price": row[0]} for row in min_price1]

      sql_max_price = text("SELECT Product.Price, Store.NameStore  FROM Product JOIN VendingMachine ON VendingMachine.ID = Product.MachineID JOIN Store ON Store.NameStore = VendingMachine.NameStore WHERE Product.NameProduct = :product_name AND Product.Price = (SELECT MAX(Price) FROM Product WHERE Product.NameProduct = :product_name);")
  
      max_price1 = conn.execute(sql_max_price, {"product_name": product_name})
      max_price = [{"Store": row[1], "Max Price": row[0]} for row in max_price1]
    
      sql_avg_price = text("SELECT ROUND(AVG(Product.Price),2) FROM  Product WHERE Product.NameProduct =:product_name;")
    
      avg_price = conn.execute(sql_avg_price, {"product_name": product_name})
      avg_price =  avg_price.scalar()
    
  return {"Info": info, "Minimum": min_price,"Maximum": max_price, "Average": avg_price}






def call_stores():
  with engine.begin() as conn:
     stmt = text("SELECT NameStore, City, Address, NumMachines FROM Store")
     store1 = conn.execute(stmt)
     stores = [{"Store Name": row[0], "City": row[1],"Address": row[2],"Number of Machines": row[3]} for row in store1]

     stmt_space = text("SELECT Store.NameStore,VendingMachine.MachineType,(VendingMachine.MaxCapacity-VendingMachine.NumItems) AS Availability FROM VendingMachine JOIN Store ON VendingMachine.NameStore = Store.NameStore")
     result = conn.execute(stmt_space)

     stores_availability = [{"Store Name": row[0], "Machine Type": row[1],"Availability": row[2]} for row in result]

     return stores,stores_availability



def call_product():
  with engine.begin() as conn:
     stmt = text("SELECT DISTINCT(Product.NameProduct), ROUND(AVG(Product.Price),2),ROUND(AVG(Product.Quantity),2) FROM Product GROUP BY NameProduct")
     distinct_product1 = conn.execute(stmt)
     distinct_product = [{"Product Name": row[0], "Average Price": row[1],"Average Quantity": row[2]} for row in  distinct_product1]
     return distinct_product


def call_vm():
  with engine.begin() as conn:
      stmt = text("""
          SELECT DISTINCT(MachineType),
                 ROUND(AVG(NumItems), 2) AS AvgNumItems,
                 ROUND(AVG(MaxCapacity), 2) AS AvgMaxCapacity,
                 COUNT(CASE WHEN Working = 1 THEN 1 ELSE NULL END) AS WorkingMachines
          FROM VendingMachine
          GROUP BY VendingMachine.MachineType
      """)

      distinct_vm1 = conn.execute(stmt)
      distinct_vm = [
          {
              "Machine Type": row[0],
              "Average Number of Items": row[1],
              "Average Maximum Capacity": row[2],
              "Number of Working Machines": row[3]
          }
          for row in distinct_vm1
      ]
      return distinct_vm


def call_employees():
  with engine.begin() as conn:
      stmt = text("""
         SELECT Employees.ID,Employees.Name, Employees.Address, Employees.PhoneNumber,Employees.NameStore, COUNT(*) AS NumWorkers
FROM Employees GROUP BY Employees.NameStore;
      """)

      employees1 = conn.execute(stmt)
      employees = [
          {
              "ID": row[0],
              "Name": row[1],
              "Address": row[2],
              "Phone Number": row[3],
              "Store Name": row[4],
              "Number of Workers in Store": row[5]
          }
          for row in employees1
      ]
      return employees

def check_product(product_name): 
  with Session() as session:
    try:
        query = text(
            "SELECT DISTINCT(VendingMachine.MachineType) FROM VendingMachine JOIN Product ON Product.MachineID = VendingMachine.ID WHERE Product.NameProduct=:product_name")
        result = session.execute(query, {"product_name": product_name})
        types = result.fetchall() 
        if  types:
            return [row[0] for row in types]
        else:
           
            return -1
    except Exception as e:
       
        print("Error:", e)
        
        return -1

def check_store(): 
  with Session() as session:
    try:
        query = text(
            "SELECT DISTINCT(NameStore) FROM Store")
        result = session.execute(query)
        stores = result.fetchall() 
        if  stores:
            return [row[0] for row in stores]
        else:

            return -1
    except Exception as e:

        print("Error:", e)

        return -1

result = check_store()
if 'Ametsa' in result:
  print("Store found")
   