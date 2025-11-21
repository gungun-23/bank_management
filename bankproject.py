from pathlib import Path
import json
import random
import string
class Bank():
    database = 'database.json'
    data = []
    
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("sorry we are facing some issues:- ")
            
    except Exception as err:
        print(f"An error occured as {err} ")
    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data))
    
    @staticmethod
    def __accountno():
        alpha=random.choices(string.ascii_letters,k=5)
        digits=random.choices(string.digits,k=4)
        id=alpha +digits
        random.shuffle(id)
        return "".join(id)
    
    
    def createaccount(self):
        d = {
            "name":input("please tell your name:- "),
            "email":input("please tell your mail:- "),
            "phone":input("pleaase tell your phone number:- "),
            "pin":input("please enter your pin(4 Digit):- "),
            "Account No.":Bank.__accountno(),
            "balance":0
            }
        
        if len(str(d['pin'])) != 4:
            print("please review your pin")
            
        elif len(str(d["phone"])) != 10:
            print("please enter a valid phone number")
            
        else:
            Bank.data.append(d)
            Bank.__update()
            print("account created")
        
    def deposit_money(self):
        accno=input("tell your accout number: ")
        pin=input("tell your pin: ")
        user_data=[i for i in Bank.data if i["Account No."]==accno and i["pin"]==pin]
        if not  user_data:
            print("user not found")
        else:
            amount=int(input("enetr amount to be deposited="))
            if amount<=0:
                print("invalid amount")
            elif amount>10000:
                print("greater than 10000")
            else:
                user_data[0]["balance"]+=amount
                Bank.__update()
                print("amount credited")
        
    def withdraw_money(self):
        accNo = input("Enter your account no.")
        pin = input("Enter your pin: ")
        user_data = [i for i in Bank.data if i['Account No.']==accNo and i["pin"]==pin]  
        if not user_data:
            print("user not found")
        else:
            amount = int(input("Enter amount to be withdraw: "))
            if amount <= 0:
                print("Invalid amount")
            elif amount > 10000:
                print("Greater than 10000")
            else:
                if user_data[0]['balance'] < amount:
                    print("Insufficent Balance")
                else:
                    user_data[0]['balance'] -=amount
                    Bank.__update()
                    print("Amount Debited")
                    
    def details(self):
        accNo = input("Enter your account no.")
        pin = input("Enter your pin: ")
        user_data = [i for i in Bank.data if i['Account No.']==accNo and i["pin"]==pin]  
        if not user_data:
            print("user not found")
        else:
            for i in user_data[0]:
                print(i,user_data[0][i])

    def update_details(self):
        accNo = input("Enter your account no.")
        pin = input("Enter your pin: ")
        user_data = [i for i in Bank.data if i['Account No.']==accNo and i["pin"]==pin]  
        if not user_data:
            print("User not found")
        
        else:
            print("You cannot change account number!")
            print("Now update your details and skip it if you dont want to")
            new_data={
                'name':input("Enter your new name: "),
                'email':input("Enter your new email:"),
                'phone':input("Enter your new phone no.:"),
                'pin':input("Enter your new pin:")
            }

            new_data["Account No."]=user_data[0]["Account No."]
            new_data["balance"]=user_data[0]["balance"]
            #Handle the skipped values:

            for i in new_data:
                if new_data[i]=="":
                    new_data[i]=user_data[0][i]

            #We have to update new data to database:

            for i in user_data[0]:
                if user_data[0][i]==new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i]=int(new_data[i])

                    else:
                        user_data[0][i]=new_data[i]
            Bank.__update  
            print("Details updated!")



    def Delete(self):
        accnumber = input("please tell your account number ")
        pin = input("please tell your pin as well ")
        user_data = [i for i in Bank.data if i['Account No.']==accnumber and i["pin"]==pin]  
        if not user_data:
            print("User not found")
        else:
            for i in Bank.data:
               if i['Account No.'] == accnumber and i['pin'] == pin:
                    Bank.data.remove(i)
                    print("account deleted successfully ")
                    Bank.__update()

            
        
        
                    
                

user = Bank()
print("press 1 for creating an account")
print("press 2 to deposit money")
print("press 3 to withdraw money")
print("press 4 for details")
print("press 5 for updating tha details")
print("press 6 for deleting tha account")

check = int(input("tell your choice:- "))

if check == 1:
    user.createaccount()
if check==2:
    user.deposit_money()
if check==3:
    user.withdraw_money()
if check==4:
    user.details()
if check==5:
    user.update_details()
if check==6:
    user.Delete()