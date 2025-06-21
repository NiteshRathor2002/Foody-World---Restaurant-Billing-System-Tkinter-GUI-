from tkinter import*
from tkinter import ttk 
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from tkinter import messagebox
import random, os
from datetime import datetime

window=Tk()
window.title("Welcome to the Foody World")
window.config(bg="lightblue")
Height=400
Width=400
full_width = 1560
sys_width=window.winfo_screenwidth()
sys_height=window.winfo_screenheight()
window.geometry(f"{sys_width}x{sys_height}")
lab=Label(window,text="Foody World",font=("Arial Rounded",20,"bold"),bg="skyblue",fg="black",pady=10,relief="groove",bd=6)
lab.pack(fill="x")

#-------Logic Part of the Program-------------------#
#----------------varibales-------------------------#
Customer_n=StringVar()
customer_co=StringVar()
Product_name=StringVar()
Product_price=StringVar()
Product_Quantiy=StringVar()
#-------------add item to the order box---------------#
def add_item_to_order():
    name = Product_name.get()
    price = Product_price.get()
    quantity = Product_Quantiy.get()

    if not name or not price or not quantity:
        messagebox.showwarning("Input Error", "Please fill all the item fields.")
        return

    try:
        qty = int(quantity)
        rate = float(price)
        total = qty * rate
    except ValueError:
        messagebox.showerror("Input Error", "Price and Quantity must be numbers.")
        return

    # ✅ DO NOT DELETE ANYTHING HERE
    Order_listbox.insert("", "end", values=(name, qty, f"{total:.2f}"))

    update_total_price()

    Product_name.set("")
    Product_price.set("")
    Product_Quantiy.set("")    
#------------------remove item---------------#
def remove_item():
    selected=Order_listbox.selection()#get selected items
    if selected:
     for item in selected:
        Order_listbox.delete(item)
     update_total_price()
    else:
        messagebox.showinfo("No Selection", "Please select an item to remove.")
def update_total_price():
    total = 0
    for child in Order_listbox.get_children():
        item = Order_listbox.item(child)["values"]
        if len(item) >= 3:
            try:
                total += float(item[2])
            except:
                pass
    total_price_entry.delete(0, END)
    total_price_entry.insert(0, f"{total:.2f}")
#------------------update qunatity-------------#
def update_quantity():
    selected = Order_listbox.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an item from the order list to update.")
        return

    try:
        new_qty = int(Product_Quantiy.get())
        unit_price = float(Product_price.get())
        name = Product_name.get()
        total = new_qty * unit_price
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid quantity and price.")
        return

    # Update selected item
    Order_listbox.item(selected[0], values=(name, new_qty, f"{total:.2f}"))

    update_total_price()

    # Clear entry fields after updating
    Product_name.set("")
    Product_price.set("")
    Product_Quantiy.set("")
    #----------------------clear orderbox---------------#
def clear_item():
    Order_listbox.delete(*Order_listbox.get_children())
    total_price_entry.delete(0, END)

    # Optional: reset product/customer fields
    Product_name.set("")
    Product_price.set("")
    Product_Quantiy.set("")
    #------------------show item accoring to type-----------#
def show():
    select_food_type=Select_menu.get()
    tree.delete(*tree.get_children())
    for item,price,category in menu_items:
        if select_food_type==category:
            tree.insert("", END, values=(item, f"₹{price}"))
def showall():
     tree.delete(*tree.get_children())
     for item,price,category in menu_items:
        tree.insert("", END, values=(item, f"₹{price}"))
        #----------------print bill--------------------#
def print_bill():
    if not Customer_n.get():
        messagebox.showwarning("Missing Info", "Please enter customer name before printing the bill.")
        return

    items = Order_listbox.get_children()
    if not items:
        messagebox.showwarning("Empty Order", "No items to bill.")
        return

    bill_number = random.randint(1000, 9999)
    bill_date = datetime.now().strftime("%Y-%m-%d")
    customer_name = Customer_n.get()

    # Save to Desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, f"bill_{bill_number}.pdf")

    # PDF setup
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50  # Start near top

    def center_text(text, y, size=14, font="Helvetica-Bold"):
        c.setFont(font, size)
        text_width = c.stringWidth(text, font, size)
        c.drawString((width - text_width) / 2, y, text)

    # --- Header Section ---
    center_text("Welcome To The Foody World", y, 16)
    y -= 25
    center_text(f"Date: {bill_date}    |    Bill No: {bill_number}", y, 12, "Helvetica")
    y -= 25
    center_text(f"Customer Name: {customer_name}", y, 12, "Helvetica")
    y -= 20
    c.line(50, y, width - 50, y)
    y -= 20

    # --- Table Header ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "Item")
    c.drawString(350, y, "Qty")
    c.drawString(500, y, "Price")
    y -= 15
    c.line(50, y, width - 50, y)
    y -= 20

    # --- Item Rows ---
    c.setFont("Helvetica", 11)
    total = 0
    for item in items:
        values = Order_listbox.item(item, "values")
        item_name, qty, price = values[0], values[1], values[2]
        total += float(price)

        # Trim item name if too long
        if len(item_name) > 35:
            item_name = item_name[:32] + "..."

        c.drawString(60, y, item_name)
        c.drawRightString(370, y, str(qty))
        c.drawRightString(520, y, f"₹{float(price):.2f}")
        y -= 20

        if y < 100:  # Add new page if space is low
            c.showPage()
            y = height - 50

    # --- Total ---
    c.line(50, y, width - 50, y)
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(520, y, f"Total: ₹{total:.2f}")
    y -= 40

    # --- Footer ---
    center_text("Thank you for visiting Foody World!", y, 12)

    c.save()

    # Open the PDF
    try:
        os.startfile(file_path)  # For preview
        # os.startfile(file_path, "print")  # For direct printing
    except Exception as e:
        messagebox.showerror("Error", f"Could not open/print PDF:\n{e}")
    else:
        messagebox.showinfo("Bill Created", f"Bill saved on Desktop:\n{file_path}")
#----------cancel order----------------#
def cancel():
    Order_listbox.delete(*Order_listbox.get_children())
    update_total_price()
#-----------------customer Details-------------#
lab2=LabelFrame(window,text="Customer Details",font=("Arial Rounded",18,"bold"),bg="lightblue",fg="black",pady=10,labelanchor="nw",padx=10,bd=6,relief="groove")
lab2.place(y=60,height=80,width=full_width )
customer_name=Label(lab2, text="Name", font=("Arial", 14), bg="lightblue").grid(row=0, column=0, padx=10)
entry_name = Entry(lab2, font=("Arial", 14), width=20,relief="sunken",textvariable=Customer_n)
entry_name.grid(row=0, column=1, padx=10)
customer_contact=Label(lab2,text="Contact_no",font=("Arial", 14),bg="lightblue").grid(row=0,column=2,padx=10)
entry_contact=Entry(lab2,font=("Arial", 14), width=20,relief="sunken").grid(row=0,column=3,padx=10)

#------------------Left Menu Section---------------------#
menu_items = [
    # Tea & Coffee
    ("Masala Chai", 30, "Tea & Coffee"),
    ("Ginger Tea", 35, "Tea & Coffee"),
    ("Green Tea", 40, "Tea & Coffee"),
    ("Coffee Mocachino", 51, "Tea & Coffee"),
    ("Coffee Americano (Black)", 55, "Tea & Coffee"),
    ("Coffee Espresso", 60, "Tea & Coffee"),
    ("Coffee Cappuccino", 51, "Tea & Coffee"),
    ("Espresso (Black)", 55, "Tea & Coffee"),

    # Beverages
    ("Ice Tea (Lemon)", 51, "Beverages"),
    ("Cold-Coffee (Frappe)", 70, "Beverages"),
    ("Cola / Orange / Lemon", 55, "Beverages"),
    ("Diet Pepsi", 55, "Beverages"),
    ("Fresh Lime Soda", 60, "Beverages"),
    ("Mineral Water", 55, "Beverages"),
    ("Mango Shake", 75, "Beverages"),
    ("Strawberry Smoothie", 90, "Beverages"),

    # Snacks
    ("Veg Sandwich", 50, "Snacks"),
    ("Grilled Cheese Sandwich", 65, "Snacks"),
    ("French Fries", 60, "Snacks"),
    ("Samosa", 20, "Snacks"),
    ("Veg Burger", 70, "Snacks"),
    ("Paneer Roll", 80, "Snacks"),
    ("Spring Rolls", 85, "Snacks"),
    ("Veg Pizza (Small)", 120, "Snacks")
]
style=ttk.Style()
style.configure("TButton", foreground="black", background="darkblue", font=("Arial rounded", 10))
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
style.configure("Treeview", font=("Arial", 11))

Left_outer_frame = Frame(window, bg="white", width=781, height=700, bd=4, relief="raised")
Left_outer_frame.place(x=0, y=139)

# Inner green LabelFrame inside white border
Left_menu = LabelFrame(Left_outer_frame, text="Menu", font=("Arial Rounded", 18, "bold"),labelanchor="n", width=770, height=633,bg="lightgreen", fg="black", bd=0)
Left_menu.place(x=0, y=3)

# Combobox and buttons
ttk.Label(Left_menu, text="Select Type", font=("Arial Rounded", 14, "bold"), background="lightgreen").place(x=20, y=10)
Select_menu = ttk.Combobox(Left_menu, values=["Tea & Coffee", "Beverages", "Snacks"], state="readonly", width=15, font=("Arial Rounded", 12))
Select_menu.place(x=140, y=10)
Select_menu.set("Tea & Coffee")

show = ttk.Button(Left_menu, text="Show", width=10, cursor="hand2",command=show)
show.place(x=370, y=10)
showall = ttk.Button(Left_menu, text="Show All", width=10, cursor="hand2",command=showall)
showall.place(x=470, y=10)

# Treeview menu list
tree = ttk.Treeview(Left_menu, columns=("Name", "Price"), show="headings", height=30)
tree.place(x=0, y=55, width=770, height=547)

tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.column("Name", width=300)
tree.column("Price", width=100, anchor="center")

scrollbar = Scrollbar(Left_menu, orient=VERTICAL, command=tree.yview)
scrollbar.place(x=752, y=56,height=544 )
tree.configure(yscrollcommand=scrollbar.set)
def on_menu_item_select(event):
    #Read the selected item
    selected = tree.selection()
    if selected:
        #Get the item's values (name & price),this return a values in tuples ("Coffe",40)
        values = tree.item(selected, "values")
        #Delete the old values form the  product name entry
        item_entry.delete(0, END)
        #insert the values of product name
        item_entry.insert(0, values[0])
        #Delete the old values from the price entry
        
        Rate_entry.delete(0, END)
        #insert the values of price and delete rate symbol 
        Rate_entry.insert(0, values[1].replace("₹", ""))  # remove ₹ symbol

#Detect which item is clicked in the Treeview        
tree.bind("<<TreeviewSelect>>", on_menu_item_select)

#-------Right menu------#

outer_frame = Frame(window, bg="white", width=760,height=240,bd=4,relief="raised")
outer_frame.place(x=781, y=141)

# Inner green item frame (simulating border inside white)

item_label = LabelFrame(
    outer_frame,
    text="Item",
    labelanchor="n",
    font=("Arial Rounded", 18, "bold"),
    fg="black",
    width=738,
    height=230,
    bd=0,
    bg="lightgreen",
)

item_label.place(x=0,y=1)
item_name=ttk.Label(item_label,text="Product Name",font=("Arial Rounded",14,"bold"),background="lightgreen").place(x=20,y=10)
item_entry = Entry(item_label, font=("Arial", 14), width=20,relief="groove",textvariable=Product_name)
item_entry.place(x=180,y=10)

Rate_name=ttk.Label(item_label,text=" Product Price",font=("Arial Rounded",14,"bold"),background="lightgreen").place(x=450,y=10)
Rate_entry = Entry(item_label, font=("Arial", 14), width=10,relief="groove",textvariable=Product_price)
Rate_entry.place(x=600,y=10)

Quantity_name=ttk.Label(item_label,text="Quantity",font=("Arial Rounded",14,"bold"),background="lightgreen").place(x=20,y=50)
Quantity_entry = Entry(item_label, font=("Arial", 14), width=10,relief="groove",textvariable=Product_Quantiy)
Quantity_entry.place(x=180,y=50)

addbtn=ttk.Button(item_label,text="Add Item",cursor="hand2",command=add_item_to_order).place(x=20,y=140)
removebtn=ttk.Button(item_label,text="Remove Item",cursor="hand2",command=remove_item).place(x=140,y=140)
Updatebtn=ttk.Button(item_label,text=" Update Quantity",cursor="hand2",command=update_quantity).place(x=260,y=140)
Clearbtn=ttk.Button(item_label,text="Clear",cursor="hand2",command=clear_item).place(x=390,y=140)

Second_outer_frame=Frame(window,bg="white", width=760,height=403,bd=4,relief="raised")
Second_outer_frame.place(x=781,y=382)
Order_label = LabelFrame(
Second_outer_frame,
    text="Your Order",
    labelanchor="n",
    font=("Arial Rounded", 18, "bold"),
    fg="black",
    width=738,
    height=390,
    bd=0,
    bg="lightgreen"
)

Order_label.place(x=0,y=3)

#-----Order Listbox-----------#

Order_listbox=ttk.Treeview(Second_outer_frame,columns=("Name","Quantity","Price"),show="headings",height=20)
Order_listbox.place(y=50,height=260,width=736)
Order_listbox.heading("Name",text="Name")
Order_listbox.heading("Quantity",text="Quantity")
Order_listbox.heading("Price",text="Price")

Order_listbox.column("Name",width=300,anchor="center")
Order_listbox.column("Quantity",width=40,anchor="center")
Order_listbox.column("Price",width=40,anchor="center")

final_step = LabelFrame(Second_outer_frame, width=736, height=82, bg="lightgreen")
final_step.place(x=0, y=310)
total_price = Label(final_step, text="Total Price", fg="black", bg="lightgreen", font=("arial rounded", 14, "bold"))
total_price.place(x=10, y=10)
total_price_entry = Entry(final_step, width=20, relief="groove", font=("arial round", 14, "bold"))
total_price_entry.place(x=150, y=10)
billbtn = ttk.Button(final_step, text="Bill", cursor="hand2",command=print_bill)
billbtn.place(x=400, y=10)
Cancel = ttk.Button(final_step, text="Cancel Order", cursor="hand2",command=cancel)
Cancel.place(x=500, y=10)
window.mainloop()