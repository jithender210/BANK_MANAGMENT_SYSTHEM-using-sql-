from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3



class Bankdatabase(ABC):
    
    def __init__(self,db_name="bank_system.db"):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS customers(customer_id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT , age INTEGER , email TEXT , phone TEXT , address TEXT )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS accounts(account_no INTEGER PRIMARY KEY AUTOINCREMENT , customer_id INTEGER ,account_type TEXT CHECK(account_type IN ('saving', 'current')), balance REAL DEFAULT 0.0 , created_at  TEXT  ,FOREIGN KEY(customer_id) REFERENCES customers(customer_id))")
        self.conn.commit()

    @abstractmethod
    def add_customer(self,*args):
        pass 

    @abstractmethod
    def open_account(self,*args):
        pass

    @abstractmethod
    def view_account(self,*args):
        pass
    #@abstractmethod
    #def view_balance(self,*args):
      #  pass



class Banksystem(Bankdatabase):
    def __init__(self):
        super().__init__()
         
    def add_customer(self,name,age,email,phone_no,address):
        self.cursor.execute("INSERT INTO customers(name,age,email,phone,address) VALUES (?,?,?,?,?)",(name,age,email,phone_no,address))
        self.conn.commit()
        return self.cursor.lastrowid
    def open_account(self, customer_id,account_type,balance):
        try:

            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO accounts(customer_id,account_type,balance,created_at) VALUES (?,?,?,?)",(customer_id,account_type,balance,created_at))
            self.conn.commit()
            print("Your account has been created sucessfully!!✅✅")
            return self.cursor.lastrowid
        except:
            print(" PLEASE CHECK THE ENTERED DETAILS ⚠️")
    def view_account(self, account_no):
        self.cursor.execute("SELECT c.name,c.email,c.phone,a.account_no,a.account_type,a.balance,a.created_at FROM accounts a  JOIN customers c ON a.customer_id=c.customer_id WHERE a.account_no= ?",(account_no,))
        result=self.cursor.fetchall()
        print(result)
        if result :
            for row in result:
                print(f" YOUR ACCOUNT NO IS  {row[3]}")
                print(f"Name :  {row[0]}")
                print(f"Phone number :  {row[2]}")
                print(f"Account type:  {row[4]}")
                print(f"Balance: {row[5]}")
                
        else:
            print ("Account not found ⚠️ ⚠️ ‼️❗❗\nPlease create an account ")
        return  result
    def view_balance(self,account_no):
        self.cursor.execute("SELECT c.name, a.balance FROM accounts a JOIN customers c ON a.customer_id = c.customer_id WHERE a.account_no= ?",(account_no,))
        result=self.cursor.fetchall()
         
        return result

if __name__=="__main__":
    print("🏦🏦Welcome to bank")
    print("select an option :\n 1. create an account \n 2. view balance\n 3. view account details ")

    option=input("enetr the option:")
    bank=Banksystem()
    if option=="1":
        print("Please fill the following details")
        name=input("Enter your full name :")
        age=input("Enter your age: ")
        email=input("Enter your email :")
        phone=input("Enter your phone number: ")
        address=input("enter your address: ")
        acc_typ=input("Enter the account type (savings/current): ")
        deposit=float(input("Enter the deposit ammount: "))
        customer_id=bank.add_customer(name,age,email,phone,address)
        account_no=bank.open_account(customer_id,acc_typ,deposit)
        bank.view_account(account_no)
        print("Please remember your account number!!⚠️ ⚠️ ")
    if option=="2":
        account_no=input("Enter your account number: ")
        bal=bank.view_balance(account_no)
        print(bal)
        for row in bal:
            print("Account holder name: ",row[0],"\-")
            print("YOUR ACCOUNT BALANCE:",row[1])

    if option =="3":
        account_no=input("Enter your account number: ")
        bank.view_account(account_no)


        







     
        



