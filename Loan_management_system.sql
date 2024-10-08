use Loan_management_system;
CREATE TABLE Customer (
    customer_id INT IDENTITY(1,1) PRIMARY KEY ,
    name VARCHAR(50),
    email VARCHAR(60),
    phone_number VARCHAR(15),
    address VARCHAR(150),
    credit_score INT
);
CREATE TABLE Loan (
    loan_id INT IDENTITY(101,1) PRIMARY KEY ,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) on DELETE CASCADE,
    principal_amount Decimal(10, 2),
    interest_rate INT,
    loan_term_months INT,
    loan_type VARCHAR(20),
    loan_status VARCHAR(20)    
);


INSERT INTO Customer (name, email , phone_number, address, credit_score) VALUES
	('Nikhil', 'nikhil@gmail.com', '+91 8458393088', '123 Happy St, Hyderabad', 830),
	('Rajashekar', 'raj@gmail.com', '+91 6974581165', '456 Park Avenue, Bengaluru', 850),
	('Jayakumar', 'jayak@gmail.com', '+91 7035024126', '789 Diamond Road, Pondicherry', 900),
	('Meghana', 'megana@gmail.com', '+91 9443342088', '11 Olive Garden, Chennai', 850),
	('Vishal', 'vishal@gmail.com', '+91 9975325173', '23 Sam Street, Chittoor', 750),
	('Rahul', 'rahul@gmail.com', '+91 8769362439', '57 Park Street, Chennai', 880),
	('Ajay', 'ajay@gmail.com', '+91 7095392498', '800 Hyung Avenue, Vijayawada', 790),
	('Kumar', 'kumar@gmail.com', '+91 8723402109', '345 Platinum Lane, Delhi', 900),
	('Mahesh', 'mahesh@gmail.com', '+91 7953488348', '6 V Avenue, Vizag', 650),
	('Jayanth', 'jayanth@gmail.com', '+91 8799383759', '12 Ghost Street, Mumbai', 580);

INSERT INTO Loan (customer_id, principal_amount, interest_rate, loan_term_months, loan_type, loan_status) VALUES
	(7, 500000, 8, 36, 'CarLoan', 'Approved'),
	(1, 1000000, 7, 60, 'HomeLoan', 'Pending'),
	(5, 300000, 9, 24, 'CarLoan', 'Approved'),
	(6, 800000, 6, 48, 'HomeLoan', 'Approved'),
	(4, 700000, 8, 36, 'CarLoan', 'Approved'),
	(3, 1200000, 7, 60, 'HomeLoan', 'Pending'),
	(2, 400000, 9, 24, 'CarLoan', 'Approved'),
	(9, 900000, 6, 48, 'HomeLoan', 'Pending'),
	(8, 600000, 8, 36, 'CarLoan', 'Pending'),
	(10, 1100000, 7, 60, 'HomeLoan', 'Pending');

alter table Loan add property_value int null,property_address varchar(255) null,car_value int null,car_model varchar(255)null;
alter table Loan add no_emi int null;

select * from Customer;
select * from Loan
ALTER TABLE Loan ADD NoOfEMI INT DEFAULT 0;