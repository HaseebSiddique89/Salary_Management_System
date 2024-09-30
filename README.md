# Basic Salary Management System
This project is a GUI-based salary management system built using Tkinter for the front-end and Neo4j as the back-end database to store employee details and payroll data. The system allows users to calculate wages, manage employee data, and generate payslips.

## Introduction
The Salary Management System is designed to handle employee records, calculate wages, manage payroll details, and store data securely using Neo4j, a graph database. The system includes various functionalities such as adding, searching, and deleting employee data, as well as generating a payslip for the employee.

## Features
- Add Employee Records: Add employee details including name, address, employer, CNIC number, hours worked, hourly rate, tax, and overtime.
- Calculate Wages: Compute employee wages based on the number of hours worked, hourly rate, tax payable, and overtime.
- Payslip Generation: Generate a formatted payslip that displays the employee's name, CNIC number, and net pay.
- Employee Search: Search for an employee using their CNIC and view their salary details.
- Employee Deletion: Delete an employee's record from the Neo4j database by providing their CNIC.
- Neo4j Database Integration: Store and manage employee records and payroll data in Neo4j, a graph database.
- Error Handling: Display error messages for invalid inputs and handle missing employee records gracefully.

## Neo4j Integration
The system uses Neo4j, a graph-based database, to store employee records. Employee data is modeled as nodes in the database, and fields such as name, CNIC, hours worked, and net pay are properties of these nodes. Key Neo4j functionalities include:

- Creating Employee Nodes: Adds a new employee record to the Neo4j database when a user enters employee details.
- Searching for Employees: Queries the database for an employee's details using their CNIC.
- Deleting Employee Records: Deletes an employee node from the database based on the CNIC.
- The system connects to a local instance of Neo4j using py2neo.

## GUI Components
The user interface is built using Tkinter, a Python library for creating GUI applications. The key components are:

- Text Input Fields: Input fields for employee name, address, employer, CNIC, hours worked, and hourly rate.

- Buttons:
   - Salary: Calculates and displays the employee's wages.
   - Reset: Clears all input fields.
   - View Payslip: Displays the formatted payslip.
   - Save Slip: Saves the employee details and payroll data to Neo4j.
   - Search: Finds and displays an employee's details using their CNIC.
   - Delete: Deletes an employee's record.
   - Exit: Closes the application.
   - Output Area: Displays the payslip in a text box.

## Functionality
### 1. Wage Calculation
Input Validation: Ensures all required fields (Name, Address, Employer, CNIC, etc.) are filled in before proceeding.
Pay Calculation: Calculates the total pay by multiplying the hours worked by the hourly rate. It also computes taxes and overtime if applicable.
Display Wages: Shows net pay, tax payable, and overtime in read-only fields.
### 2. Employee Management
Add Employee to Database: Adds the employee’s details to the Neo4j database using a MERGE query.
Search Employee: Finds and displays an employee’s details using their CNIC by running a Neo4j MATCH query.
Delete Employee: Deletes an employee record from the Neo4j database by running a MATCH and DELETE query based on the CNIC number.
### 3. Payslip Generation
Formats and displays employee data in the form of a payslip using Tkinter’s Text widget.
Data shown includes name, CNIC, net pay, tax, and hours worked.
### 4. Error Handling
Alerts the user if required fields are missing or if invalid inputs are provided (e.g., non-numeric values for hours worked).
Displays appropriate error messages if no employee is found during search or deletion.

## How to Run
### Prerequisites
- Python 3.x
- Neo4j installed and running on localhost (bolt://localhost:7687)
- py2neo library installed (pip install py2neo)
- Tkinter (typically included with Python installations)





