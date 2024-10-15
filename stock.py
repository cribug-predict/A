from AI_market_open.stock_all import predict
from custom_package import utils
import pandas as pd

def calculate(offset=0):
  utils.collection.delete_one(filter={"filename":"predict"})
  dflist=pd.read_csv("list.csv",dtype={"code":str})
  indexToDrop=[]
  dflist=dflist.drop(index=indexToDrop)
  in_sub="轨交设备"
  dflist=dflist.query("industry_sub!=@in_sub")
  dflist=pd.DataFrame(dflist,columns=["code","name","industry_sub"])
  dfempty=predict.pred_df(dflist,offset)
  dfempty=dfempty.dropna()
  dfempty=pd.DataFrame(dfempty,columns=["code","name","预低"])
  dfempty.to_csv("stock.csv",encoding="utf_8_sig",index=None)
calculate(0)