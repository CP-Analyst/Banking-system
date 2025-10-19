import random
from datetime import datetime
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="MONEYBANK"
)
mycursor = mydb.cursor()

a1 = 1
while(a1 == 1):
    print("\n************************WELCOME TO MONEYBANK************************")
    print("1. NEW ACCOUNT")
    print("2. TRANSACTION")
    print("3. LOAN_ELIGIBILITY")
    print("4. EXIT")
    a = int(input("\nCHOOSE OPTION:-"))

    # --- Fetch existing accounts ---
    mycursor.execute("SELECT ACC_NO FROM ACCOUNT_OPENING")
    acc_no = mycursor.fetchall()
    List = [row[0] for row in acc_no]

    # --- Generate unique account number ---
    while True:
        y = random.randint(10000, 99999)
        if y not in List:
            break

    if a == 1:  # NEW ACCOUNT
        print("ACCOUNT NUMBER:-", y)
        c1 = input("NAME :-")
        c2 = int(input("AGE:-"))
        G = int(input("GENDER- 1.MALE    2.FEMALE :-"))
        c3 = "MALE" if G == 1 else "FEMALE"
        c4 = input("ENTER YOUR CITY :-")

        # Account Type Selection
        print("ACCOUNT TYPE OPTIONS:")
        print("1. SERVICE")
        print("2. CURRENT")
        print("3. SAVING")
        while True:
            acc_type_choice = input("CHOOSE ACCOUNT TYPE (1/2/3) :- ")
            if acc_type_choice == "1":
                c5 = "SERVICE"
                break
            elif acc_type_choice == "2":
                c5 = "CURRENT"
                break
            elif acc_type_choice == "3":
                c5 = "SAVING"
                break
            else:
                print("Invalid choice! Choose 1, 2 or 3.")

        while True:
            c6 = input("Enter your 10-digit mobile number: ")
            if c6.isdigit() and len(c6) == 10:
                break
            else:
                print("Invalid input! Please enter exactly 10 digits.")
        date_input = input("Opening Date (YYYY-MM-DD): ")
        c7 = datetime.strptime(date_input, "%Y-%m-%d").date()
        c8 = int(input("ENTER YOUR OPENING BALANCE :-"))

        insert = "INSERT INTO ACCOUNT_OPENING(ACC_NO,NAME,AGE,GENDER,CITY,TYPE,CONT,DATE,BALANCE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        d = (y,c1,c2,c3,c4,c5,c6,c7,c8)
        mycursor.execute(insert, d)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    # --- Exit Option ---
    if a == 4:
        print("Thank you for visiting MONEYBANK!")
        break

    # --- Transaction Menu ---
    if a == 2:
        # Fetch transaction IDs
        mycursor.execute("SELECT TRANS_ID FROM TRANSACTION")
        ID = mycursor.fetchall()
        L2 = [row[0] for row in ID]

        while True:
            c1 = int(input("ACCOUNT NO :-"))
            if c1 in List:
                break
            else:
                print("Account number not found! Enter a valid account number.")

        # Generate unique transaction ID
        while True:
            y1 = random.randint(1, 999)
            if y1 not in L2:
                break
        print("TRANSACTION ID:-", y1)

        # Transaction type menu
        print("TRANSACTION TYPE:")
        print("1. CREDIT")
        print("2. DEBIT")
        print("3. BALANCE CHECK")
        while True:
            c2_input = input("Choose type (1/2/3) :- ")
            if c2_input in ["1","2","3"]:
                break
            print("Invalid choice!")

        if c2_input == "1":
            c2 = "CREDIT"
            c3 = int(input("TRANSACTION AMOUNT :-"))
        elif c2_input == "2":
            c2 = "DEBIT"
            # Get last balance
            mycursor.execute("SELECT UPDATED_BAL FROM TRANSACTION WHERE ACC_NO=%s ORDER BY TRANS_TIMESTAMP DESC LIMIT 1",(c1,))
            l = mycursor.fetchone()
            if l:
                r = l[0]
            else:
                mycursor.execute("SELECT BALANCE FROM ACCOUNT_OPENING WHERE ACC_NO=%s",(c1,))
                r = mycursor.fetchone()[0]
            # Insufficient balance check
            while True:
                c3 = int(input("TRANSACTION AMOUNT :-"))
                if c3 > r:
                    print("INSUFFICIENT BALANCE! Last balance:", r)
                    continue
                break
        else:
            c2 = "BAL_CHECK"
            c3 = 0

        print("TRANSACTION MODE OPTIONS:")
        print("1. CASH")
        print("2. UPI")
        print("3. NETBANKING")
        print("4. CHEQUE")
        print("5. NA")
        while True:
            mode_choice = input("Choose mode (1/2/3/4/5) :- ")
            if mode_choice == "1":
                c5 = "CASH"
                break
            elif mode_choice == "2":
                c5 = "UPI"
                break
            elif mode_choice == "3":
                c5 = "NETBANKING"
                break
            elif mode_choice == "4":
                c5 = "CHEQUE"
                break
            elif mode_choice == "5":
                c5 = "NA"
                break
            else:
                print("Invalid choice! Choose 1,2,3,4 or 5")

        # Get last balance
        mycursor.execute("SELECT UPDATED_BAL FROM TRANSACTION WHERE ACC_NO=%s ORDER BY TRANS_TIMESTAMP DESC LIMIT 1",(c1,))
        l = mycursor.fetchone()
        if l:
            r = l[0]
        else:
            mycursor.execute("SELECT BALANCE FROM ACCOUNT_OPENING WHERE ACC_NO=%s",(c1,))
            r = mycursor.fetchone()[0]
        print("LAST BALANCE:-", r)

        if c2 == "CREDIT":
            cc = r + c3
        elif c2 == "DEBIT":
            cc = r - c3
        else:
            cc = r

        if c2 != "BAL_CHECK":
            insert = "INSERT INTO TRANSACTION(TRANS_ID,ACC_NO,TRANS_TYPE,AMOUNT,MODE,UPDATED_BAL) VALUES (%s,%s,%s,%s,%s,%s)"
            d = (y1,c1,c2,c3,c5,cc)
            mycursor.execute(insert, d)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        print("CURRENT BALANCE:-", cc)

    # --- Loan Eligibility ---
    if a == 3:
        while True:
            c1 = int(input("ACCOUNT NO :-"))
            if c1 in List:
                break
            else:
                print("Account number not found! Enter a valid account number.")

        mycursor.execute("SELECT NAME, AGE, CITY, TYPE FROM ACCOUNT_OPENING WHERE ACC_NO=%s",(c1,))
        result = mycursor.fetchone()

        if result:
            name, age, city, acc_type = result
            print("\n--- CUSTOMER DETAILS ---")
            print("NAME:", name)
            print("AGE:", age)
            print("CITY:", city)
            print("ACCOUNT TYPE:", acc_type)

            mycursor.execute("SELECT TRANS_TYPE,AMOUNT FROM TRANSACTION WHERE ACC_NO=%s",(c1,))
            trans = mycursor.fetchall()

            total_credit = sum(t[1] for t in trans if t[0] == "CREDIT")
            total_debit = sum(t[1] for t in trans if t[0] == "DEBIT")

            if total_credit + total_debit == 0:
                print("\nNo transaction data available.")
                credit_ratio = 0
            else:
                credit_ratio = (total_credit / (total_credit + total_debit)) * 100

            if credit_ratio >= 90:
                cibil = 850; eligible = "YES"; loan_percent = 70
            elif credit_ratio >= 80:
                cibil = 800; eligible = "YES"; loan_percent = 60
            elif credit_ratio >= 70:
                cibil = 750; eligible = "YES"; loan_percent = 50
            elif credit_ratio >= 60:
                cibil = 700; eligible = "YES"; loan_percent = 30
            else:
                cibil = 650; eligible = "NO"; loan_percent = 0

            print("\n--- FINANCIAL SUMMARY ---")
            print("Total Credit:", total_credit)
            print("Total Debit:", total_debit)
            print("Credit Ratio:", round(credit_ratio,2), "%")
            print("CIBIL SCORE:", cibil)
            print("Loan Eligible:", eligible)
            print("Loan Limit (% of Avg Monthly Credit):", loan_percent, "%")
            if eligible == "YES":
                avg_monthly_credit = total_credit / 12
                estimated_loan = (avg_monthly_credit * loan_percent)/100
                print("Estimated Loan Amount: ₹", round(estimated_loan,2))

    # --- Repeat Prompt ---
    a1 = int(input("AGAIN(1.YES, 2.NO):-"))
