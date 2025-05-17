import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import numpy as np
EXCEL_FILE = 'inventory.xlsx'
SHEET_NAME = 'Sheet1'

    


def load_data():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Pid","Supplier Type","Supplier Name","Email","Mobile No","Address","Product Name","Category","Price","Quantity","Unit","Expiry_date",])


def save_data(df):
    try:
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
    except FileNotFoundError:
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
        

st.header("Retail story inventory information")
option = st.radio("Select one option",["Sell","Donate"])
data = load_data()


# FOR THE NAME ADDRESS AND EMAIL 
if option == "Sell":
    contact = st.text_input("Enter Mobile No")
    data["Mobile No"] = data["Mobile No"].apply(lambda x: str(int(float(x))) if pd.notnull(x) else "")
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
    selections =["Aata","Pulses","Oil","Spices","Dry Fruit","Grain","Gram Flour","Miscellaneous"]
    Category = st.selectbox("Select the category of Product",selections)
    if Category in data['Category'].values:
        product_series = data[data['Category']==Category]["Product Name"]
        products_list = list(product_series.unique())
        products_list.append("Other (Enter new)")
        selected= st.selectbox("select Product",products_list)
         
        if selected == "Other (Enter new)":
            Product_name = st.text_input("Enter new product name", key="new_product")
        else:
            Product_name = selected
    else:
        Product_name = st.text_input("Enter new product name", key="new_product")
        

        
       


    
    

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
                    "Mobile No":contact,
                    "Address":Address,
                    "Product Name":Product_name,
                    "Category":Category,
                    "Price":Price,
                    "Quantity":Quantity,
                    "Unit":Unit,
                    "Expiry_date":Expiry_date}
        
        new_entry = pd.DataFrame([data_entry])
        df = pd.concat([data,new_entry],ignore_index=True)
        st.write(data)
        st.write(new_entry)
        save_data(df)
        
        

        

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

    

# FOR THE PRODUCT NAME 
    existing_products = data["Product Name"].dropna().unique().tolist()
    existing_products.append("Other (Enter new)")

    selected = st.selectbox("Select a product", existing_products)

    if selected == "Other (Enter new)":
        Product_name = st.text_input("Enter new product name", key="new_product")
        
    else:
        Product_name = selected


#FOR PRODUCT CATEGORY
    selections =["Aata","Pulses","Oil","Spices","Dry Fruit","Grain","Gram Flour","Miscellaneous"]
    category_series = data[data['Product Name']==Product_name]["Category"]
    if category_series.empty== False:
        default_option = category_series.iloc[0]
        Category = st.radio("Select Category",selections,index=selections.index(default_option))
    else:
        Category = st.radio("Select Category",selections)

 
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
    Quantity = st.number_input("Enter Quantity")
    Unit = st.selectbox("Enter Units",["Kg","Bottle"])
    Expiry_date = st.date_input("Enter expiry Date")
    
    submit = st.button("Submit")
    clear =st.button("Clear")
    if submit:
        if not Product_name:
            st.warning("Enter product name first")

        pid = int(data["Pid"].max() + 1) if not data.empty else 1
            

        data_entry  = { "Pid":pid,
                        "Supplier Type":option,
                    "Supplier Name":name,
                    "Email":email,
                    "Mobile No":contact,
                    "Address":Address,
                    "Product Name":Product_name,
                    "Category":Category,
                    "Price":np.nan,
                    "Quantity":Quantity,
                    "Unit":Unit,
                    "Expiry_date":Expiry_date}
        
        new_entry = pd.DataFrame([data_entry])
        df = pd.concat([data,new_entry],ignore_index=True)
        st.write(data)
        st.write(new_entry)
        save_data(df)
        
        st.success("Form submitted")

        
        
        