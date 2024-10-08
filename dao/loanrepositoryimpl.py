import sys
sys.path.append(r"C:\Users\nikhi\OneDrive\Pictures\Documents\loan_project_oops")

from exception.invalidloanexception import InvalidLoanException
from util import dbutil
import pyodbc
from dao.loanrepository import ILoanRepository
class LoanRepositoryImpl(ILoanRepository):
    def __init__(self):
        self.conn = dbutil.DBUtil.get_db_conn()

    def apply_loan(self, loan):
        try:
            print("Do you want to apply for the loan? (Yes/No):")
            choice = input()
            if choice.lower() == "yes":
                cursor = self.conn.cursor()
                if loan.loan_type=='HomeLoan':
                    cursor.execute("INSERT INTO Loan ( customer_id, principal_amount, interest_rate, loan_term_months, loan_type, loan_status,property_address,property_value) VALUES ( ?, ?, ?, ?, ?, ?,?,?)",
                               ( loan.customer_id, loan.principal_amount, loan.interest_rate, loan.loan_term_months, loan.loan_status,loan.property_address,loan.property_value))
                self.conn.commit()
                print("HomeLoan applied successfully!")
                if loan.loan_type=='CarLoan':
                    cursor.execute("INSERT INTO Loan ( customer_id, principal_amount, interest_rate, loan_term_months, loan_type, loan_status,car_model,car_value) VALUES ( ?, ?, ?, ?, ?, ?,?,?)",
                               ( loan.customer_id, loan.principal_amount, loan.interest_rate, loan.loan_term_months, loan.loan_type, loan.loan_status,loan.car_model,loan.car_value))
                self.conn.commit()
                print("CarLoan applied successfully!")
            else:
                print("Loan application cancelled.")
        except pyodbc.Error as ex:
            print(f"Error applying for the loan: {ex}")

    def calculate_interest(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT principal_amount, interest_rate, loan_term_months FROM Loan WHERE loan_id=?", (loan_id,))
            row = cursor.fetchone()
            if row:
                principal_amount, interest_rate, loan_term_months = row
                interest = (principal_amount * interest_rate * loan_term_months) / 12
                return interest
            else:
                raise InvalidLoanException("Loan not found.")
        except pyodbc.Error as ex:
            print(f"Error calculating interest: {ex}")

    def loan_status(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT credit_score FROM Customer WHERE customer_id=(SELECT customer_id FROM Loan WHERE loan_id=?)", (loan_id,))
            row = cursor.fetchone()
            if row:
                credit_score = row[0]
                if credit_score > 650:
                    cursor.execute("UPDATE Loan SET loan_status='Approved' WHERE loan_id=?", (loan_id,))
                    self.conn.commit()
                    print("Congratulations, Loan approved.")
                else:
                    cursor.execute("UPDATE Loan SET loan_status='Rejected' WHERE loan_id=?", (loan_id,))
                    self.conn.commit()
                    print("Sorry, Loan rejected due to low credit score.")
            else:
                raise InvalidLoanException("Loan not found.")
        except pyodbc.Error as ex:
            print(f"Error updating loan status: {ex}")

    def calculate_emi(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT principal_amount, interest_rate, loan_term_months FROM Loan WHERE loan_id=?", (loan_id,))
            row = cursor.fetchone()
            if row:
                principal_amount, interest_rate, loan_term_months = row
                principal_amount=float(principal_amount)
                interest_rate=float(interest_rate)
                R = interest_rate / 12 / 100
                N = loan_term_months
                emi = (principal_amount * R * (1+R)**N) / ((1+R)**N - 1)
                return emi
            else:
                raise InvalidLoanException("Loan not found.")
        except pyodbc.Error as ex:
            print(f"Error calculating EMI: {ex}")

    def loan_repayment(self, loan_id, amount):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT principal_amount, interest_rate, loan_term_months FROM Loan WHERE loan_id=?", (loan_id,))
            row = cursor.fetchone()
            if row:
                principal_amount, interest_rate, loan_term_months = row
                principal_amount=float(principal_amount)
                interest_rate=float(interest_rate)
                R = interest_rate / 12 / 100
                N = loan_term_months
                emi = (principal_amount * R * (1 + R) ** N) / ((1 + R) ** N - 1)
                no_of_emi = amount / float(emi)

                if amount < emi:
                    print("Amount is less than one EMI. Payment rejected.")
                else:
                    cursor.execute("UPDATE Loan SET NoOfEMI=NoOfEMI+? WHERE loan_id=?", (int(no_of_emi), loan_id))
                    self.conn.commit()
                    print(f"{int(no_of_emi)} EMI(s) paid successfully.")
            else:
                raise InvalidLoanException("Loan not found.")
        except pyodbc.Error as ex:
            print(f"Error processing loan repayment: {ex}")

    def get_all_loan(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Loan")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"Loan ID: {row[0]}, Customer ID: {row[1]}, Principal Amount: {row[2]}, Interest Rate: {row[3]}, Loan Term: {row[4]}, Loan Type: {row[5]}, Loan Status: {row[6]}")
            else:
                print("No loans found.")
        except pyodbc.Error as ex:
            print(f"Error fetching loans: {ex}")

    def get_loan_by_id(self, loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Loan WHERE loan_id=?", (loan_id,))
            row = cursor.fetchone()
            if row:
                print(f"Loan ID: {row[0]}, Customer ID: {row[1]}, Principal Amount: {row[2]}, Interest Rate: {row[3]}, Loan Term: {row[4]}, Loan Type: {row[5]}, Loan Status: {row[6]}")
            else:
                raise InvalidLoanException("Loan not found.")
        except pyodbc.Error as ex:
            print(f"Error fetching loan: {ex}")

    def customer_details(self,loan_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT customer_id, name, phone_number,email, address from Customer WHERE customer_id=?", (loan_id,))
            row = cursor.fetchall()
            if row:
                print(f"{row[0]}")
            else:
                raise InvalidLoanException("Customer Not found")
        except pyodbc.Error as ex:
            print(f"Error fetching Customer:{ex}")
    

    def updateloancount(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT customer_id, name, phone_number from Customer")
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return -1
            
        except pyodbc.Error as ex:
            print("Error")