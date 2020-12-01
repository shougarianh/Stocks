import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
from companies import companies as cp


api_key = 'YOCWIOGGAB7SB5FV'
ts = TimeSeries(key=api_key,output_format='pandas')
writer = pd.ExcelWriter('companyData.xlsx')
for i in cp:
    # data, meta_data = ts.get_intraday(symbol=cp.get(i), interval='1min', outputsize='full')
    data, meta_data = ts.get_intraday(symbol=cp.get(i), interval="60min") # , outputsize='compact')
    data.to_excel(writer, sheet_name=cp.get(i))
# data, meta_data = ts.get_intraday(symbol='AAPl', interval='1min', outputsize='full')
writer.save()
