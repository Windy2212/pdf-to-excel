from datetime import datetime
from django.shortcuts import render
import pdfplumber
import io
import os
import pandas as pd
from .forms import Upload
from datetime import datetime


def home_view(request):
    data = Upload()
    return render(request, 'home.html',{'data':data})

def pdf_view(request):
    if request.method == 'POST' and request.FILES['myfile']:
        pdfFileObj = io.BytesIO(request.FILES['myfile'].read())
        pdfFileObj1 = request.FILES['myfile'].read()
        my_dataframe = pd.DataFrame()
        with pdfplumber.open(pdfFileObj) as pdf:
            for page in pdf.pages:
                text = page.extract_text().splitlines()
                nameIdx, expirDateIdx, paymentIdx = -1, -1, -1
                print('vikram2')
                for idx, line in enumerate(text):
                    if "Shipment Reference :" in line:
                        expirDateIdx = idx
                    if "Waybill Number :" in line:
                        paymentIdx = idx
                    if "Invoice Number :" in line:
                        nameIdx = idx - 1

                Shipment = text[expirDateIdx] if expirDateIdx != -1 else ''
                WayBill = text[paymentIdx] if paymentIdx != -1 else ''
                Name = text[nameIdx] if nameIdx != -1 else ''
                order = Shipment.split('Shipment Reference : ')
                order_id = order[1]
                bill = WayBill.split('Waybill Number : ')
                ship = bill[1]
                customer = Name.split(', ')
                customer_name = customer[1]
                my_list = [order_id, ship, customer_name]
                my_list = pd.Series(my_list)
                my_dataframe = my_dataframe.append(my_list, ignore_index=True)
                my_dataframe = my_dataframe.rename(columns={'Shipment Reference': order_id, 'Waybill Number': ship, 'Name': customer_name})
                print(my_dataframe)
                date = datetime.now().strftime("%d - %m - %y")
                file_name = f'{str(date)}.xlsx'
                os.chdir('E:\pdf-file-save')
                # os.makedirs( date , exist_ok=True)
                my_dataframe.to_excel(file_name)
            return render(request,"upload.html")





