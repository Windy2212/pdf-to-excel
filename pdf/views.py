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
                nameIdx, add1Idx, add2Idx, add3Idx, ShipmentIdx, WaybillIdx, phoneIdx = -1, -1, -1, -1, -1, -1, -1
                print('vikram2')
                for idx, line in enumerate(text):
                    if "Shipment Reference :" in line:
                        ShipmentIdx = idx
                    if "Waybill Number : " in line:
                        WaybillIdx = idx
                    if "Invoice Number :" in line:
                        nameIdx = idx - 1
                    if "Receiver :" in line:
                        add1Idx = idx + 4
                    if "Receiver :" in line:
                        add2Idx = idx + 6
                    if "Receiver :" in line:
                        add3Idx = idx + 7
                    if "Tax ID :" in line:
                        phoneIdx = idx - 1
                        textIdx = idx - 2
                    if "Shipment Reference : " in line:
                        phoneIdx2 = idx + 1

                Shipment = text[ShipmentIdx] if ShipmentIdx != -1 else ''
                WayBill = text[WaybillIdx] if WaybillIdx != -1 else ''
                Name = text[nameIdx] if nameIdx != -1 else ''
                add1 = text[add1Idx] if add1Idx != -1 else ''
                add2 = text[add2Idx] if add2Idx != -1 else ''
                add3 = text[add3Idx] if add3Idx != -1 else ''
                phone1 = text[phoneIdx] if phoneIdx != -1 else ''
                phone2 = text[phoneIdx2] if phoneIdx2 != -1 else ''
                phone3 = text[textIdx] if textIdx != -1 else ''
                address = add1 + ", " + add2 + ", " + add3
                a = phone1
                b = phone2
                c = phone3
                phone_number = a if (a==b) else c
                order = Shipment.split('Shipment Reference : ')
                order_id = order[1]
                bill = WayBill.split('Waybill Number : ')
                ship = bill[1]
                customer = Name.split(', ')
                customer_name = customer[1]
                my_list = [order_id, ship, customer_name, address, phone_number]
                my_list = pd.Series(my_list)
                my_dataframe = my_dataframe.append(my_list, ignore_index=True)
                my_dataframe = my_dataframe.rename(columns={'Shipment Reference': order_id, 'Waybill Number': ship, 'Name': customer_name, 'Address': address, 'phone': phone_number})
                print(my_dataframe)
                date = datetime.now().strftime("%d-%m-%y")
                file_name = f'{str(date)}.xlsx'
                os.chdir('E:\pdf-file-save')
                # os.makedirs( date , exist_ok=True)
                my_dataframe.to_excel(file_name)
            return render(request,"upload.html")





