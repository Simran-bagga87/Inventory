import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import numpy as np
EXCEL_FILE = 'inventory.xlsx'
SHEET_NAME = 'Sheet1'


name_of_product = ['Atta ', 'Sugar ', 'Ghee ', 'Mah Dal', 'Chana Dal ', 'Chilka Dal', 'Hari Dal ', 'Mung Dal ', 'Masoor Dal ', 'Rise', 'Oil ', 'Tata Namak ', 'Chai Patti ', 'Rajma ', 'Kale chane ', 'Chole ', 'Garam Powder', 'Jeera Sabut', 'Dhaniya Powder', 'Jeera powder', 'Dhaniya Powder', 'Dhaniya Sabut', 'Haldi powder', 'Lal Mirch Powder', 'Lal Mirch Sabut', 'Deggi Mirch Powder ', 'Kasuri Methi ', 'Dal Makhani Powder', 'Shahi Paneer Powder', 'Rajma Powder', 'Chana Powder', 'Lobia ', 'Moth Dal ', 'Urad Dhuli Dal ', 'Seviyan ', 'Soya bean ', 'Suji ', 'Jaggery ', 'Besan ', 'Meda ', 'Daliya ', 'ROOHAFZA', 'Achar ', 'Amchoor powder ', 'Sabji powder ', 'Kitchan King Powder', 'Methi Dana ', 'Hari Elaichi ', 'Long ', 'Kali MIrch Sabut ', 'Kali Mirch Powder', 'Ajwain ', 'Fennel ', 'Baking Powder', 'Chaat POwder', 'Mix Powder', 'Elaichi ', 'Badam Giri ', 'Badam Chilka ', 'Kaju ', 'Kishmish ', 'Wheat ', 'Rai Sabut ', 'Rai Powder', 'Brown Sirka ', 'Kastard', 'coffe Powder', 'Kale Til', 'Honey', 'Nariyal oil ', 'Colour ', 'Bundi ', 'Poha ', 'Sabut Dana ', 'Mungfali Dana ']
pulses = ['Mah Dal', 'Chana Dal ', 'Chilka Dal', 'Hari Dal ', 'Mung Dal ', 'Masoor Dal ', 'Rajma ', 'Chole ', 'Kale chane ', 'Moth Dal ', 'Urad Dhuli Dal ', 'Lobia ', 'Kaale Til']
spices = [ 'Garam Powder', 'Dhaniya Powder', 'Jeera powder', 'Haldi powder', 'Lal Mirch Powder', 'Deggi Mirch Powder ', 'Dal Makhani Powder', 'Shahi Paneer Powder', 'Rajma Powder', 'Chana Powder', 'Amchoor powder ', 'Sabji powder ', 'Kitchan King Powder', 'Baking Powder', 'Chaat Powder', 'Mix Powder', 'Kali MIrch Sabut ', 'Jeera Sabut', 'Dhaniya Sabut', 'Lal Mirch Sabut', 'Rai Sabut']
oil = ['Oil ', 'Nariyal oil ', 'Fortune Oil ']
dry_fruits = ['Badam Giri ', 'Badam Chilka ', 'Kaju ', 'Kishmish ']
grains = ['Sabut Dana ', 'Mungfali Dana ', 'Methi Dana ']
gram_flour = ['Seviyan ', 'Soya bean ', 'Suji ', 'Jaggery ', 'Besan ', 'Meda ', 'Daliya ', 'Colour ', 'Bundi ', 'Poha' ]
Miscellaneous=[ 'Atta ', 'Sugar ', 'Ghee ', 'Rice', 'Tata Namak ', 'Chai Patti ', 'ROOHAFZA', 'Honey', 'coffe Powder', 'Elaichi ']





def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME,,dtype={"Mobile No": str})
        
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Pid","Supplier Type","Supplier Name","Email","Mobile No","Address","Product Name","Category","Price","Quantity","Unit","Expiry_date","Issued To","Issued Name","Issued Date","Issued Quantity","Issued Unit","Reciever Name","Receiver Contact","Receiver Email","Receiver Address"])


def save_data(df):
    df["Mobile No"] = df["Mobile No"].astype(str)
    try:
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
    except FileNotFoundError:
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
        

st.header("Retail story inventory information")
option = st.radio("Select one option",["Purchase","Donate","Issue"])
data = load_data()


# FOR THE NAME ADDRESS AND EMAIL 
if option == "Purchase":
    contact = st.text_input("Enter Mobile No")
    
    pre_name = ""
    pre_email= ""
    pre_address = ""
   
        
    if contact:
        match = data["Mobile No"].astype(str).str.strip() == contact
        if match.any():
            matched_row = data[match].iloc[0]
            pre_name = matched_row["Supplier Name"]
            pre_email = matched_row["Email"]
            pre_address = matched_row["Address"]
            

        name = st.text_input("Enter Name", value=pre_name)
        email = st.text_input("Enter Email", value=pre_email)
        Address = st.text_area("Enter Address", value=pre_address)


    else:
        name = st.text_input("Enter Name")
        email = st.text_input("Enter email")
        Address = st.text_area("Enter Address")



# FOR THE PRODUCT NAME 
    # existing_products = data["Product Name"].dropna().unique().tolist()
    # existing_products.append("Other (Enter new)")

    # selected = st.selectbox("Select a product", existing_products)

    # if selected == "Other (Enter new)":
    #     Product_name = st.text_input("Enter new product name", key="new_product")
        
    # else:
    #     Product_name = selected



#FOR PRODUCT CATEGORY

    selections = ["Pulses", "Oil", "Spices", "Dry Fruit", "Grain", "Gram Flour", "Miscellaneous"]

    Category = st.selectbox("Select the category of Product", selections)

    category_map = {
        "Pulses": pulses,
        "Spices": spices,
        "Dry Fruit": dry_fruits,
        "Oil":oil,
        "Grain": grains,
        "Gram Flour": gram_flour,
        "Miscellaneous": Miscellaneous
    }

    if Category in category_map:
        options = category_map[Category] + ["Other (Enter new)"]
        product_choice = st.selectbox("Select Product", options)

        if product_choice == "Other (Enter new)":
            Product_name = st.text_input("Enter new product name", key="new_product")
        else:
            Product_name = product_choice
    else:
        Product_name = st.text_input("Enter new product name", key="new_product")
        category_map[Category].append(Product_name)


    Price = st.number_input("Enter price")
    Quantity = st.number_input("Enter Quantity")


#FOR PRODUCT UNIT
    selections_unit = ["Kg", "G", "Ltr", "Mltr", "Bottle"]
    selections_unit.append("Other (Enter new)")

    unit_series = data[data['Product Name'] == Product_name]["Unit"]

    if not unit_series.empty:
        default_option = unit_series.iloc[0]
        if default_option not in selections_unit:
            selections_unit.insert(0, default_option)
    else:
        default_option = selections_unit[0]

    selected_unit = st.radio("Select Unit", selections_unit, index=selections_unit.index(default_option))

    if selected_unit == "Other (Enter new)":
        Unit = st.text_input("Enter Unit", key="new_unit")
    else:
        Unit = selected_unit



    Expiry_date = st.date_input("Enter expiry Date")
    

    submit = st.button("Submit")
    
    
    
    if submit:
        if not name or not email or not Address:
            st.warning("Name, Email, and Address are required.")
        if not Product_name:
            st.warning("Enter product name first")
        st.success("Form submitted")
        pid = int(data["Pid"].max() + 1) if not data.empty else 1

        data_entry  = { "Pid":pid,
                        "Supplier Type":option,
                    "Supplier Name":name,
                    "Email":email,
                    "Mobile No":str(contact),
                    "Address":Address,
                    "Product Name":Product_name,
                    "Category":Category,
                    "Price":Price,
                    "Quantity":Quantity,
                    "Unit":Unit,
                    "Expiry_date":Expiry_date}
        
        new_entry = pd.DataFrame([data_entry])
        df = pd.concat([data,new_entry],ignore_index=True)
        
        save_data(df)
        st.write(oil)
        

        

elif option =="Donate":
    contact = st.text_input("Enter Mobile No")
   
    pre_name = ""
    pre_email= ""
    pre_address = ""
   
        
    if contact:
        match = data["Mobile No"].astype(str).str.strip() == contact
        if match.any():
            matched_row = data[match].iloc[0]
            pre_name = matched_row["Supplier Name"]
            pre_email = matched_row["Email"]
            pre_address = matched_row["Address"]
            

        name = st.text_input("Enter Name", value=pre_name)
        email = st.text_input("Enter Email", value=pre_email)
        Address = st.text_area("Enter Address", value=pre_address)


    else:
        name = st.text_input("Enter Name")
        email = st.text_input("Enter email")
        Address = st.text_area("Enter Address")
    selections = ["Pulses", "Oil", "Spices", "Dry Fruit", "Grain", "Gram Flour", "Miscellaneous"]

    Category = st.selectbox("Select the category of Product", selections)

    category_map = {
        "Pulses": pulses,
        "Spices": spices,
        "Dry Fruit": dry_fruits,
        "Oil": oil,
        "Grain": grains,
        "Gram Flour": gram_flour,
        "Miscellaneous": Miscellaneous
    }

    if Category in category_map:
        options = category_map[Category] + ["Other (Enter new)"]
        product_choice = st.selectbox("Select Product", options)

        if product_choice == "Other (Enter new)":
            Product_name = st.text_input("Enter new product name", key="donate_new_product")
        else:
            Product_name = product_choice
    else:
        Product_name = st.text_input("Enter new product name", key="donate_new_product")
        category_map[Category].append(Product_name)

    Quantity = st.number_input("Enter Quantity")
    Unit = st.selectbox("Select Unit", ["Kg", "G", "Ltr", "Mltr", "Bottle", "Other"])
    if Unit == "Other":
        Unit = st.text_input("Enter custom Unit", key="donate_custom_unit")
    Expiry_date= st.date_input("enter the expiry date")
    submit = st.button("Submit Donation")

    if submit:
        if not name or not email or not Address:
            st.warning("Name, Email, and Address are required.")
        elif not Product_name:
            st.warning("Product name is required.")
        else:
            st.success("Donation form submitted")
            pid = int(data["Pid"].max() + 1) if not data.empty else 1

            donation_entry = {
                "Pid": pid,
                "Supplier Type": option,
                "Supplier Name": name,
                "Email": email,
                "Mobile No": str(contact),
                "Address": Address,
                "Product Name": Product_name,
                "Category": Category,
                "Price": 0, 
                "Quantity": Quantity,
                "Unit": Unit,
                "Expiry_date": Expiry_date,  
            }

            new_donation = pd.DataFrame([donation_entry])
            df = pd.concat([data, new_donation], ignore_index=True)

            save_data(df)

    

        
        
elif option=="Issue":
    Issued_to = st.text_input("Enter issuing to")
    issuer_name = st.text_input("Enter issuer name")
    issue_date = st.date_input("Enter issuing date")
    Issued_Qty = st.number_input("Enter issuing Quantity")
    Unit = st.number_input("Enter Units")
    Receiver_Name = st.text_input("Enter Receiver name")
    Receiver_Contact = st.text_input("Enter contact detail")
    Receiver_Email = st.text_input("Enter issuer email")
    Receiver_Address = st.text_input("Enter Receiver Address")

    
    submit = st.button("Submit")   
    if submit:
        

        pid = int(data["Pid"].max() + 1) if not data.empty else 1
            

        data_entry  = { "Pid":pid,
                        "Supplier Type":option,
                       "Issued To":Issued_to,
                       "Issued Name":issuer_name,
                       "Issued Date":issue_date,
                       "Issued Quantity":Issued_Qty,
                       "Issued Unit":Unit,
                       "Reciever Name":Receiver_Name,
                       "Receiver Contact":Receiver_Contact,
                       "Receiver Email":Receiver_Email,
                       "Receiver Address":Receiver_Address}
                        
        
        new_entry = pd.DataFrame([data_entry])
        df = pd.concat([data,new_entry],ignore_index=True)

        save_data(df)
       
        
        st.success("Form submitted")
