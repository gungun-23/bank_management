import streamlit as st
import json
from pathlib import Path
import random
import string


# --------------------------
# Original Bank Class (fixed)
# --------------------------

class Bank():
    database = 'database.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            with open(database, "w") as fs:
                json.dump([], fs)
    except Exception as err:
        st.error(f"Error loading database: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id)

    # Methods rewritten to accept arguments instead of input()

    def createaccount(self, name, email, phone, pin):
        d = {
            "name": name,
            "email": email,
            "phone": phone,
            "pin": pin,
            "Account No.": Bank.__accountno(),
            "balance": 0
        }

        if len(str(pin)) != 4:
            return "PIN must be 4 digits", None
        if len(str(phone)) != 10:
            return "Phone number must be 10 digits", None

        Bank.data.append(d)
        Bank.__update()
        return "Account created successfully!", d["Account No."]

    def deposit_money(self, accno, pin, amount):
        user_data = [i for i in Bank.data if i["Account No."] == accno and i["pin"] == pin]
        if not user_data:
            return "User not found"

        if amount <= 0:
            return "Invalid amount"
        elif amount > 10000:
            return "Amount cannot exceed 10000"

        user_data[0]["balance"] += amount
        Bank.__update()
        return "Amount credited successfully!"

    def withdraw_money(self, accno, pin, amount):
        user_data = [i for i in Bank.data if i["Account No."] == accno and i["pin"] == pin]
        if not user_data:
            return "User not found"

        if amount <= 0:
            return "Invalid amount"
        elif amount > 10000:
            return "Amount cannot exceed 10000"

        if user_data[0]["balance"] < amount:
            return "Insufficient balance"

        user_data[0]["balance"] -= amount
        Bank.__update()
        return "Amount debited successfully!"

    def details(self, accno, pin):
        user_data = [i for i in Bank.data if i["Account No."] == accno and i["pin"] == pin]
        if not user_data:
            return None
        return user_data[0]

    def update_details(self, accno, pin, name, email, phone, newpin):
        user_data = [i for i in Bank.data if i['Account No.'] == accno and i["pin"] == pin]
        if not user_data:
            return "User not found"

        updated = user_data[0]

        if name: updated["name"] = name
        if email: updated["email"] = email
        if phone: updated["phone"] = phone
        if newpin: updated["pin"] = newpin

        Bank.__update()
        return "Details updated successfully!"

    def delete(self, accno, pin):
        user_data = [i for i in Bank.data if i['Account No.'] == accno and i["pin"] == pin]
        if not user_data:
            return "User not found"

        Bank.data.remove(user_data[0])
        Bank.__update()
        return "Account deleted successfully!"


# --------------------------
# STREAMLIT UI
# --------------------------

bank = Bank()
st.title("🏦 Simple Banking System (Streamlit Interface)")

menu = st.sidebar.selectbox(
    "Select Operation",
    ("Create Account", "Deposit Money", "Withdraw Money", "View Details", "Update Details", "Delete Account")
)

# 1. Create account
if menu == "Create Account":
    st.header("Create New Account")

    with st.form("create_form"):
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email")
        phone = st.text_input("Enter your phone number")
        pin = st.text_input("Set 4-digit PIN", type="password")
        submit = st.form_submit_button("Create Account")

    if submit:
        msg, accno = bank.createaccount(name, email, phone, pin)
        st.success(msg)
        if accno:
            st.info(f"Your new account number: **{accno}**")

# 2. Deposit Money
elif menu == "Deposit Money":
    st.header("Deposit Money")

    with st.form("deposit_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amt = st.number_input("Amount", min_value=1)
        submit = st.form_submit_button("Deposit")

    if submit:
        st.info(bank.deposit_money(acc, pin, amt))

# 3. Withdraw
elif menu == "Withdraw Money":
    st.header("Withdraw Money")

    with st.form("withdraw_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amt = st.number_input("Amount", min_value=1)
        submit = st.form_submit_button("Withdraw")

    if submit:
        st.info(bank.withdraw_money(acc, pin, amt))

# 4. View Details
elif menu == "View Details":
    st.header("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        data = bank.details(acc, pin)
        if data:
            st.json(data)
        else:
            st.error("User not found")

# 5. Update Details
elif menu == "Update Details":
    st.header("Update Account Information")

    with st.form("update_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        name = st.text_input("New Name (optional)")
        email = st.text_input("New Email (optional)")
        phone = st.text_input("New Phone (optional)")
        newpin = st.text_input("New PIN (optional)", type="password")
        submit = st.form_submit_button("Update")

    if submit:
        st.success(bank.update_details(acc, pin, name, email, phone, newpin))

# 6. Delete Account
elif menu == "Delete Account":
    st.header("Delete Your Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete Account"):
        st.warning(bank.delete(acc, pin))
