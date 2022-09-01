# import necessaary libs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd 

# connection params 
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

# read from sheet
sh = client.open("CopyBest")

# worsheet_list = sh.worksheets()

objective_worksheet = sh.worksheet('Objective')
Control_worksheet = sh.worksheet('Control')
SKUSales_worksheet = sh.worksheet('SKU Sales')
SKUMarketing_worksheet = sh.worksheet('SKU Marketing')
output_worksheet = sh.worksheet('Output Template')

#output
# data[1:], columns=data[0]

skuSales_df = pd.DataFrame(SKUSales_worksheet.get_all_values()[1:], columns=SKUSales_worksheet.get_all_values()[0])
skuMarketing_df = pd.DataFrame(SKUMarketing_worksheet.get_all_values()[1:], columns=SKUMarketing_worksheet.get_all_values()[0])
outputWorksheet_df = pd.DataFrame(output_worksheet.get_all_values()[1:], columns=output_worksheet.get_all_values()[0])
# print(skuSales_df, skuMarketing_df)
print(outputWorksheet_df)


# skuSales_df.to_csv('data.csv')
# result = pd.merge(skuSales_df, skuMarketing_df, how="left", on=["SKU_ID"])
# print(result)


