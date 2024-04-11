"""
The flask application package.
"""
from datetime import datetime
from msilib.schema import SelfReg
import smtplib
from typing import Self
from flask import Flask, render_template, request, redirect, url_for
from config import EMAIL_SENDER, SMTP_SERVER, SMTP_PORT  # Import configuration variables
app = Flask(__name__)

import Proactive_Inventory____Supply_Chain_Integration__PISCI_.views

class Supplier:
    def __init__(self, supplier_id, name, contact_info):
        self.id = supplier_id
        self.name = name
        self.contact_info = contact_info

class Stock:
    def __init__(self, item_id, name, max_inventory, on_hand, supplier):
        self.id = item_id
        self.name = name
        self.total_capacity = max_inventory
        self.current_level = on_hand
        self.supplier = supplier
        self.reorder_threshold = int(input("Enter reorder threshold for " + self.name + ": "))

    @property
    def reorder_point(self):
        # Derived property: Calculate reorder point based on some logic
        return self.current_level < self.reorder_threshold

class OrderRequest:
    def __init__(self, request_id, item, quantity, status="pending"):
        self.id = request_id
        self.item = item
        self.quantity = quantity
        self.status = status
        self.created_at = datetime.now()

class InventoryMonitor:
    def get_inventory_data(self):
        # Fetch inventory data from a database or other source
        pass

    def check_reorder_point(self, item):
        return item.current_level < item.reorder_point

    def generate_order_request(self, item):
        return OrderRequest(request_id=None, item=item, quantity=item.total_capacity - item.current_level)

class OrderManagementSystem:
    def submit_order_request(self):
        # Logic to submit the order request to the supply chain system
        self.sender = EMAIL_SENDER
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        
    def submit_order_request(self, request):
        # Existing order submssion logic
        self.send_order_notification(request)
     
    def send_order_notification(self, request):
     message = f"An order has been placed for item {request.item.name}
    ({request.quantity} units). Order ID: {request.id}"
     with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
      server.starttls()
      # Assuming password is stored securely elsewhere 
      server.login(self.sender, "your_password")
      server.sendmail(SelfReg.sender, request.item.supplier.contact_info, message)


# Request for user to import inventory database
@app.route("/import-inventory")
def import_inventory():
    if request.method == "POST":
        uploaded_file = request.files["inventory_file"]
        if uploaded_file.filename.lower().endswith(('.csv', '.json')):
            # Validate and parse file contents
            inventory_data = parse_inventory_data(uploaded_file)
            # Populate database with inventory data
            populate_database(inventory_data)
            return redirect(url_for("success_message"))  # Redirect to success page
        else:
            return "Invalid file format!"
    else:
        return render_template("import_form.html")  # Display import form        

# Example usage
if __name__ == "__main__":
    supplier1 = Supplier(supplier_id=1, name="Supplier A", contact_info="supplierA@example.com")
    item1 = Stock(item_id=101, name="Widget", total_capacity=200, current_level=100, supplier=supplier1)

    monitor = InventoryMonitor()
    if monitor.check_reorder_point(item1):
        order_request = monitor.generate_order_request(item1)
        order_system = OrderManagementSystem()
        order_system.submit_order_request(order_request)
    else:
        print(f"{item1.name} inventory is sufficient.")

