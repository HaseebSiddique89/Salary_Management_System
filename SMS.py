import datetime
from tkinter import *
import time
from tkinter import messagebox, simpledialog
import os
from py2neo import Graph


"""Setting up the geometry and the title"""
root = Tk()
root.title("Salary management system")
root.geometry('1350x650+0+0')
root.configure(bg = 'black')
"""set"""

# ================================== neo4j ==========================================

graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

# ============================================================================

def validate_input():
    if not Name.get() or not Address.get() or not Employer.get() or not Ninumber.get() or not hoursworked.get() or not hourlyrate.get():
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return False
    return True

def delete():
    result = simpledialog.askstring("Delete", "Enter CNIC")
    person = graph.run("""MATCH(n:PERSON {CNIC:$usrcnic}) delete n return n"""
                       , {'usrcnic':result})
    
    if len(person.data()) > 0:
        messagebox.showinfo('Confirmation','Successfully deleted!')
    else:
        messagebox.showerror('Error','No Record Found!')
    

def find():
    result = simpledialog.askstring("Search", "Enter CNIC")
    person = graph.run("""MATCH(n:PERSON {CNIC:$usrcnic}) return n.name, n.Address, n.Employer, n.Hourlyrate, n.Hoursworked, n.Netpay, n.CNIC, n.Overtime, n.Payable, n.Tax"""
                       , {'usrcnic':result})
    
    formatted_result = ""
    if person: 
        for record in person:
            formatted_result += "Name: {}\n".format(record['n.name'])
            formatted_result += "Address: {}\n".format(record['n.Address'])
            formatted_result += "Employer: {}\n".format(record['n.Employer'])
            formatted_result += "Hourly Rate: {}\n".format(record['n.Hourlyrate'])
            formatted_result += "Hours Worked: {}\n".format(record['n.Hoursworked'])
            formatted_result += "Net Pay: {}\n".format(record['n.Netpay'])
            formatted_result += "CNIC: {}\n".format(record['n.CNIC'])
            formatted_result += "Overtime: {}\n".format(record['n.Overtime'])
            formatted_result += "Payable: {}\n".format(record['n.Payable'])
            formatted_result += "Tax: {}\n\n".format(record['n.Tax'])

    if formatted_result:
        messagebox.showinfo("Saved Slip", str(formatted_result))
    
    else:
        messagebox.showerror("Error", 'No Record Found')


def database():
    if not validate_input():
        return

    dname = Name.get()
    dAddress = Address.get()
    dEmployer = Employer.get()
    dNinumber = Ninumber.get()
    dHoursworked = hoursworked.get()
    dHourlyrate = hourlyrate.get()
    dTax = tax.get()
    dOvertime = overtime.get()
    dNetpay = netpay.get()
    dPayable = payable.get()

    graph.run("""MERGE(n:PERSON {name:$usrname,Address:$usraddress,Employer:$usremployer,CNIC:$usrNinumber,Hoursworked:$usrhoursworked,Hourlyrate:$usrhourlyrate,Tax:$usrtax,Overtime:$usrovertime,Netpay:$usrnetpay,Payable:$usrpayable})"""
              , {'usrname':dname , 'usraddress':dAddress ,'usremployer':dEmployer,'usrNinumber':dNinumber,'usrhoursworked':dHoursworked,'usrhourlyrate':dHourlyrate,'usrtax':dTax,'usrovertime':dOvertime,'usrnetpay':dNetpay,'usrpayable':dPayable})


def wages():
    if not validate_input():
        return

    try:
        Hoursworkedinweek = float(hoursworked.get())
        wageperhour = float(hourlyrate.get())

        if Hoursworkedinweek <= 0 or wageperhour <= 0:
            messagebox.showerror("Error", "Invalid input. Please enter positive values.")
            return

        pay = wageperhour * Hoursworkedinweek
        paydue = "PKR " + str('%.2f' % pay)
        payable.set(paydue)

        taxa = pay * 0.2
        Taxable = "PKR " + str('%.2f' % taxa)
        tax.set(Taxable)

        netpaya = pay - taxa
        Netpays = "PKR " + str('%.2f' % netpaya)
        netpay.set(Netpays)

        if Hoursworkedinweek > 40:
            overtimehours = (Hoursworkedinweek - 40) * wageperhour * 1.5
            overtimeh = "PKR " + str('%.2f' % overtimehours)
            overtime.set(overtimeh)
        else:
            overtime.set("PKR 0.00")

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values.")


def exit():
    qexit = messagebox.askyesno("Salary management system", "Do you want to exit?")
    if qexit > 0:
        root.destroy()
    return

def Reset():
    Name.set("")
    Address.set("")
    Employer.set("")
    Ninumber.set("")
    hoursworked.set("")
    hourlyrate.set("")
    tax.set("")
    overtime.set("")
    netpay.set("")
    payable.set("")
    txtsalary.delete("1.0",END)
    return
    
def info():
    if not validate_input():
        return

    txtsalary.insert(END,"\t\tSalary\n\n")
    txtsalary.insert(END,"Name: \t\t" + Name.get() + "\n\n")
    txtsalary.insert(END,"Address: \t\t" + Address.get() + "\n\n")
    txtsalary.insert(END,"Employer: \t\t" + Employer.get() + "\n\n")
    txtsalary.insert(END,"Ninumber: \t\t" + Ninumber.get() + "\n\n")
    txtsalary.insert(END,"Hours Worked: \t\t" + hoursworked.get() + "\n\n")
    txtsalary.insert(END,"NET PAY\t\t" + netpay.get() + "\n\n")
    txtsalary.insert(END,"Hourly Rate\t\t" + hourlyrate.get() +"\n\n")
    txtsalary.insert(END,"Tax Payable: \t\t" + tax.get() + "\n\n")
    txtsalary.insert(END,"Payable \t\t" + payable.get() + "\n\n")
    return

# =============================================================================================

Name = StringVar()
Address = StringVar()
Employer = StringVar()
Ninumber = StringVar()
hoursworked = StringVar()
hourlyrate = StringVar()
tax = StringVar()
overtime = StringVar()
netpay = StringVar()
dateoforder = StringVar()
timeoforder = StringVar()
payable = StringVar()

Topframe = Frame(root, width = 1350, height = 50, bd = 0, bg = 'black',relief ="raise")
Topframe.pack(side = TOP)

frameone = Frame(root, width = 600, height = 600, bd = 0, bg = 'black', relief = "raise")
frameone.pack(side = LEFT)

frametwo = Frame(root, width = 300, height = 700, bd = 0, bg = 'black', relief = "raise")
frametwo.pack(side = RIGHT)

fla = Frame(frameone,width = 600, height = 200, bd = 0, bg = 'black',relief = "raise")
fla.pack(side = TOP)

gap_frame = Frame(frameone, width = 600, height = 40, bd=0, bg = 'black', relief="raise")
gap_frame.pack()

flb = Frame(frameone,width = 600, height = 300, bd = 0, bg = 'black',relief = "raise")
flb.pack(side = BOTTOM)

lblinfo = Label(Topframe, font =('arial', 60, 'italic','bold'), bg = "lightblue",fg = "white", text = "       Salary Management System        ", bd = 10)
lblinfo.grid(row = 0, column = 0)

lblmin = Label(Topframe, font = ('arial' , 15, 'italic'), bg = 'black', fg = 'white', text = "Take Control of Your Payroll with Confidence")
lblmin.grid(row = 1,column = 0)


dateoforder.set(time.strftime("%d/%m/%Y"))

lblName = Label(fla, text = "Name",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblName.grid(row = 0, column = 0)

lbladdress = Label(fla, text = "Address",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lbladdress.grid(row = 0, column = 2)

lblEmployer = Label(fla, text = "Employer",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblEmployer.grid(row = 1, column = 0)

lblNinumber = Label(fla, text = "CNIC Number",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblNinumber.grid(row = 1, column = 2)

lblhoursworked = Label(fla, text = "Hours Worked",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblhoursworked.grid(row = 2, column = 0)

lblhourlyrate = Label(fla, text = "Hourly Rate",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblhourlyrate.grid(row = 2, column = 2)

lbltax = Label(fla, text = "Tax payable",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lbltax.grid(row = 3, column = 0)

lblovertime = Label(fla, text = "Extra Bonus",fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblovertime.grid(row = 3, column = 2)

lblgrosspay = Label(fla, text = "Grosspay", fg = "white", bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblgrosspay.grid(row = 4, column = 0)

lblNetpay = Label(fla, text = "Net Pay", fg = "white",  bg = 'black', font = ('arial',16,'italic','bold'),bd = 20)
lblNetpay.grid(row = 4, column = 2)




etxtname = Entry(fla, textvariable = Name, font = ('arial',16,'italic','bold'),bd = 10,width = 22, justify = 'left')
etxtname.grid(row = 0, column = 1)

etxtadd = Entry(fla, textvariable = Address, font = ('arial',16,'italic','bold'),bd = 10,width = 22, justify = 'left')
etxtadd.grid(row = 0, column = 3)

etxtemployer = Entry(fla, textvariable = Employer, font = ('arial',16,'italic','bold'),bd = 10,width = 22, justify = 'left')
etxtemployer.grid(row = 1, column = 1)

etxtnumber = Entry(fla, textvariable = Ninumber, font = ('arial',16,'italic','bold'),bd = 10,width = 22, justify = 'left')
etxtnumber.grid(row = 1, column = 3)

etxthoursw = Entry(fla, textvariable = hoursworked, font = ('arial',16,'italic','bold'),bd = 10,width = 22, justify = 'left')
etxthoursw.grid(row = 2, column = 1)

etxthourlyr = Entry(fla, textvariable = hourlyrate, font = ('arial',16,'italic','bold'),bd = 10,width = 22, justify = 'left')
etxthourlyr.grid(row = 2, column = 3)



etxttax = Entry(fla, textvariable = tax, font = ('arial',16,'italic','bold'),bd = 4,width = 22, justify = 'left',state='readonly')
etxttax.grid(row = 3, column = 1)
etxttax.configure(readonlybackground='black', fg='white')

etxtovertime = Entry(fla, textvariable = overtime, font = ('arial',16,'italic','bold'),bd = 4,width = 22, justify = 'left',state='readonly')
etxtovertime.grid(row = 3, column = 3)
etxtovertime.configure(readonlybackground='black', fg='white')

etxtnetpay = Entry(fla, textvariable = netpay, font = ('arial',16,'italic','bold'),bd = 4,width = 22, justify = 'left',state='readonly')
etxtnetpay.grid(row = 4, column = 3)
etxtnetpay.configure(readonlybackground='black', fg='white')

etxtpayable = Entry(fla, textvariable = payable, font = ('arial',16,'italic','bold'),bd = 4,width = 22, justify = 'left',state='readonly')
etxtpayable.grid(row = 4, column = 1)
etxtpayable.configure(readonlybackground='black', fg='white')


lblsalary = Label(frametwo,textvariable = dateoforder, bg = 'black', fg = 'white' ,font = ('arial',21,'italic','bold')).grid(row = 0, column = 0)
txtsalary = Text(frametwo, height = 22, width = 40, bd = 16, bg = 'black', fg = 'white', font=('arial',12,'italic','bold'))
txtsalary.grid(row = 1, column = 0)



btnsalary = Button(flb,text = 'Salary', padx = 16, pady = 16, bd =8, fg = "black",bg = "lightblue", font = ('arial',8,'italic','bold'), width = 7, height = 0, command = wages).grid(row = 2, column = 0)

btnreset = Button(flb,text = 'Reset', padx = 16, pady = 16, bd =8, fg = "black",bg = "lightblue", font = ('arial',8,'italic','bold'), width = 7, height = 0, command = Reset).grid(row = 2, column = 1)

btnpayslip = Button(flb,text = 'View Payslip', padx = 16, pady = 16, bd =8, fg = "black",bg = 'lightblue', font = ('arial',8,'italic','bold'), width = 7, height = 0, command = info).grid(row = 2, column = 2)

btnexit = Button(flb,text = 'Save Slip', padx = 16, pady = 16, bd =8, fg = "black",bg = "lightblue", font = ('arial',8,'italic','bold'), width = 7, height = 0, command = database).grid(row = 2, column = 3)

btnexit = Button(flb,text = 'Search', padx = 16, pady = 16, bd =8, fg = "black",bg = "lightblue", font = ('arial',8,'italic','bold'), width = 7, height = 0, command = find).grid(row = 2, column = 4)

btnexit = Button(flb,text = 'delete', padx = 16, pady = 16, bd =8, fg = "black",bg = "lightblue", font = ('arial',8,'italic','bold'), width = 7, height = 0, command = delete).grid(row = 2, column = 5)

btnexit = Button(flb,text = 'Exit', padx = 16, pady = 16, bd =8, fg = "black",bg = 'lightblue', font = ('arial',8,'italic','bold'), width = 7, height = 0, command = exit).grid(row = 2, column = 6)

root.mainloop()