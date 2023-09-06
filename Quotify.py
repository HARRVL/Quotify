from fpdf import FPDF
from datetime import datetime, timedelta

class PDF(FPDF):
    def header(self):
    # Add the company logo
     self.image('king.png', 5, 8, 33)  # Adjust the values to fit the logo.

    # Move below the logo to set the title
     self.set_xy(10, 8 + 33 - 15)  # Position below the logo (logo's height + 5 units for spacing)
     self.set_font('Times', 'B', 16)
     self.cell(0, 10, 'Kings Solar', 0, 1, 'L')
    
    # Set the address below the company name
     self.set_font('Times', '', 12)
     self.cell(0, 10, 'Cataño, Puerto Rico', 0, 1, 'L')

    # Center and set the "Invoice/Quote" text
     self.ln(10)  # Spacing before the text
     self.set_font('Times', 'B', 20)
     self.cell(0, 20, "Invoice/Quote", 0, 1, 'C') 


    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_invoice(business, client, items, date, expiry_date):
    pdf = PDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Client details on the right side
    pdf.set_font('Times', '', 12)
    pdf.set_xy(145, 10)
    pdf.cell(0, 10, f"Name: {client['name']}", 0, 2)
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, f"Phone: {client['phone']}", 0, 2)
    
    if 'email' in client and client['email']:
        pdf.cell(0, 10, f"Email: {client['email']}", 0, 2)

    # Dates
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, f"Date: {date.strftime('%Y-%m-%d')}", 0, 2)
    pdf.cell(0, 10, f"Expiry Date: {expiry_date.strftime('%Y-%m-%d')}", 0, 2)

    pdf.ln(20)  # Add a 20-unit space

    # Table headers
    col_widths = [70, 30, 30, 50]
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(col_widths[0], 10, "Item Description", 1, 0, 'C', 1)
    pdf.cell(col_widths[1], 10, "Quantity", 1, 0, 'C', 1)
    pdf.cell(col_widths[2], 10, "Price", 1, 0, 'C', 1)
    pdf.cell(col_widths[3], 10, "Sub-Total", 1, 1, 'C', 1)

    # Items in table and calculating total
    total = 0 

    for item in items:
        sub_total = item['price'] * item['quantity']  # Calculate the sub_total here
        total += sub_total  # Add sub_total to the total for each item

        pdf.cell(col_widths[0], 10, item['description'], 1)
        pdf.cell(col_widths[1], 10, str(item['quantity']), 1, 0, 'C')
        pdf.cell(col_widths[2], 10, f"${item['price']:.2f}", 1, 0, 'R')
        pdf.cell(col_widths[3], 10, f"${sub_total:.2f}", 1, 1, 'R')

    # Total outside table
    pdf.set_font('Times', 'B', 12)
    pdf.cell(col_widths[0] + col_widths[1] + col_widths[2], 10, "Total", 0, 0, 'R')
    pdf.cell(col_widths[3], 10, f"${total:.2f}", 1, 1, 'R')

    # Additional Text
    pdf.ln(10) # add some space
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, "Cotización preparada por: Héctor Reyes", 0, 1)
    pdf.multi_cell(0, 10, "Esta es una cotización de los productos mencionados, sujeta a las condiciones que se detallan a continuación: Todas las ventas son finales, el pago se debe al momento de la recepción.")
    
    pdf.ln(5)  
    pdf.cell(0, 10, "Firma del cliente: ____________________________________________________", 0, 1)
    
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Ofrecemos una garantía extendida de 10 años honrada por nosotros localmente aquí en Puerto Rico.")
    
    # Save
    cleaned_client_name = client['name'].replace(" ", "_")
    filename = f"Kings Solar {cleaned_client_name}.pdf"
    pdf.output(filename)

    print(f"Invoice saved as {filename}")

def main():
    business = {
        'name': 'Kings Solar',
        'address': 'Cataño, Puerto Rico'
    }

    client_name = input("Enter client name: ")
    client_phone = input("Enter client phone: ")
    client_email = input("Enter client email (press Enter to skip): ")

    client = {
        'name': client_name,
        'phone': client_phone,
    }
    if client_email:
        client['email'] = client_email

    date_input = input("Enter date (YYYY-MM-DD): ")
    date = datetime.strptime(date_input, "%Y-%m-%d")
    expiry_date = date + timedelta(days=15)

    items = []
    while True:
        item_desc = input("Enter item description (or 'done' to finish): ")
        if item_desc.lower() == 'done':
            break
        item_price = float(input("Enter item price: "))
        item_quantity = int(input("Enter item quantity: "))
        items.append({
            'description': item_desc,
            'price': item_price,
            'quantity': item_quantity
        })

    generate_invoice(business, client, items, date, expiry_date)

if __name__ == "__main__":
    main()
