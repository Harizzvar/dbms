import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="inventory_db"
)
cursor = conn.cursor()

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("600x400")
        
        # Labels and Entries
        self.product_label = tk.Label(root, text="Product Name")
        self.product_label.grid(row=0, column=0, padx=10, pady=10)
        self.product_entry = tk.Entry(root)
        self.product_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.quantity_label = tk.Label(root, text="Quantity")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.price_label = tk.Label(root, text="Price")
        self.price_label.grid(row=2, column=0, padx=10, pady=10)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Buttons
        self.add_button = tk.Button(root, text="Add Product", command=self.add_product)
        self.add_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.view_button = tk.Button(root, text="View Products", command=self.view_products)
        self.view_button.grid(row=3, column=1, padx=10, pady=10)
        
        self.sell_button = tk.Button(root, text="Sell Product", command=self.sell_product)
        self.sell_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.view_sales_button = tk.Button(root, text="View Sales", command=self.view_sales)
        self.view_sales_button.grid(row=4, column=1, padx=10, pady=10)

    def add_product(self):
        name = self.product_entry.get()
        quantity = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        
        cursor.execute("INSERT INTO Products (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        conn.commit()
        
        messagebox.showinfo("Success", "Product added successfully!")
        
        self.product_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def view_products(self):
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        
        view_window = tk.Toplevel(self.root)
        view_window.title("View Products")
        
        for index, product in enumerate(products):
            tk.Label(view_window, text=f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[2]}, Price: {product[3]}").grid(row=index, column=0, padx=10, pady=5)
    
    def sell_product(self):
        sell_window = tk.Toplevel(self.root)
        sell_window.title("Sell Product")
        
        tk.Label(sell_window, text="Product ID").grid(row=0, column=0, padx=10, pady=10)
        product_id_entry = tk.Entry(sell_window)
        product_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(sell_window, text="Customer Name").grid(row=1, column=0, padx=10, pady=10)
        customer_name_entry = tk.Entry(sell_window)
        customer_name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(sell_window, text="Quantity").grid(row=2, column=0, padx=10, pady=10)
        sell_quantity_entry = tk.Entry(sell_window)
        sell_quantity_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def process_sale():
            product_id = int(product_id_entry.get())
            customer_name = customer_name_entry.get()
            quantity = int(sell_quantity_entry.get())
            
            cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
            price = cursor.fetchone()[0]
            total_price = price * quantity
            
            cursor.execute("INSERT INTO Customers (name) VALUES (%s)", (customer_name,))
            conn.commit()
            
            customer_id = cursor.lastrowid
            
            cursor.execute("INSERT INTO Sales (product_id, customer_id, sale_date, quantity, total_price) VALUES (%s, %s, %s, %s, %s)", 
                           (product_id, customer_id, date.today(), quantity, total_price))
            conn.commit()
            
            cursor.execute("UPDATE Products SET quantity = quantity - %s WHERE product_id = %s", (quantity, product_id))
            conn.commit()
            
            messagebox.showinfo("Success", "Product sold successfully!")
            sell_window.destroy()
        
        tk.Button(sell_window, text="Sell", command=process_sale).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    def view_sales(self):
        cursor.execute("SELECT Sales.sale_id, Products.name, Customers.name, Sales.sale_date, Sales.quantity, Sales.total_price FROM Sales JOIN Products ON Sales.product_id = Products.product_id JOIN Customers ON Sales.customer_id = Customers.customer_id")
        sales = cursor.fetchall()
        
        view_sales_window = tk.Toplevel(self.root)
        view_sales_window.title("View Sales")
        
        for index, sale in enumerate(sales):
            tk.Label(view_sales_window, text=f"ID: {sale[0]}, Product: {sale[1]}, Customer: {sale[2]}, Date: {sale[3]}, Quantity: {sale[4]}, Total Price: {sale[5]}").grid(row=index, column=0, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

# Close the database connection
conn.close()
