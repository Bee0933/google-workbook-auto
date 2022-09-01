import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class workbook:
      def __init__(self) -> None:
            # connection parameters
            scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
            
            # google cloud platform API credentials
            creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
            
            # create API client
            client = gspread.authorize(creds)
            
            # copen the work book
            self.sh = client.open("CopyBest")
            
            # create session instances of worksheets 
            self.skusales_worksheet = self.sh.worksheet('SKU Sales')
            self.skuMarketing_worksheet = self.sh.worksheet('SKU Marketing')

      # function to merge and update output worksheet based on key ID's and merge type
      def merge_sheets(self, how : str , id : str):

            # containers
            skid=[]
            sales=[]
            grosmargin=[]
            spend1=[]
            spend2=[]

            # convert worsheet to pandas dataframe to process
            skuSales_df = pd.DataFrame(self.skusales_worksheet.get_all_values()[1:], columns=self.skusales_worksheet.get_all_values()[0])
            skuMarketing_df = pd.DataFrame(self.skuMarketing_worksheet.get_all_values()[1:], columns=self.skuMarketing_worksheet.get_all_values()[0])

            # apply data preprocessing
            result_df = pd.merge(skuSales_df, skuMarketing_df, how=how, on=[id])
            df = result_df.drop(['Order ID'], axis=1)
            df.to_csv('result.csv')
            df=pd.read_csv('result.csv')
            
            # sumup and count 
            sku_ids = list(df.SKU_ID.unique())
            for id in sku_ids:
                  skuvalues = df[df.SKU_ID == id]
                  sales_sumup = skuvalues['Sales'].sum()
                  gross_margin_count = len(skuvalues['Gross Margin'].dropna())
                  spend1_sumup = skuvalues['Spend 1'].sum()
                  spend2_count = len(skuvalues['Spend 1'].dropna())

                  skid.append(id)
                  sales.append(sales_sumup)
                  grosmargin.append(gross_margin_count)
                  spend1.append(spend1_sumup)
                  spend2.append(spend2_count)

            # define output frame
            result = pd.DataFrame({ 
                  "SKU_ID":skid, 
                  'Sales': sales, 
                  "Gross Margin":grosmargin,
                  "Spend 1": spend1,
                  "Spend 2" : spend2
            })

            try:
                  # create output worksheet with required content
                  output_worksheet = self.sh.add_worksheet(title="Output", rows=result.shape[0], cols=result.shape[1])
            except:
                  # if worksheet already exists
                  output_worksheet = self.sh.worksheet('Output')
            
            # ingest worksheet data to workbook
            output_worksheet.update([result.columns.values.tolist()] + result.values.tolist())

            return result
            
      #  merge left function
      def merge_left(self):
            result_df = self.merge_sheets(how='left',id="SKU_ID")
            print(result_df)
      
      #  merge left function
      def merge_right(self):     
            result_df = self.merge_sheets(how='right',id="SKU_ID")
            print(result_df)
      
      # merge inner/intersection function
      def merge_inner(self):
            result_df = self.merge_sheets(how='inner',id="SKU_ID")
            print(result_df)

      # merge outer/union function
      def merge_outer(self):
            result_df = self.merge_sheets(how='outer',id="SKU_ID")
            print(result_df)
            

            
wb = workbook()
wb.merge_left()
# wb.merge_right()
# wb.merge_inner()
# wb.merge_outer()



