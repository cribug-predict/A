import akshare as ak
from custom_package import utils
import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt
import numpy as np
from multiprocessing import Process,shared_memory

ansys=utils.ansys()
y_lower=-5
y_toper=5

#offset unit seconed
x_offset=240
colorScale=0.3
baseelement=1-colorScale
base=(1.0,1.0,1.0)
count_toshow=30
# date=now.strftime("%Y%m%d")
sleeptime=1
totaltime=90*120 
totaltime=int(totaltime)
start=dt.datetime.now()
date=utils.getTradeDay()[0]
time0900:dt.datetime=dt.datetime.strptime(date+" 09:00:00" ,'%Y%m%d %H:%M:%S')
time0915:dt.datetime=dt.datetime.strptime(date+" 09:15:00" ,'%Y%m%d %H:%M:%S')
time0925=dt.datetime.strptime(date+" 09:25:00" ,'%Y%m%d %H:%M:%S')
time0926=dt.datetime.strptime(date+" 09:26:00" ,'%Y%m%d %H:%M:%S')
time0930=dt.datetime.strptime(date+" 09:30:00" ,'%Y%m%d %H:%M:%S')
time1130=dt.datetime.strptime(date+" 11:30:00" ,'%Y%m%d %H:%M:%S')
time1200=dt.datetime.strptime(date+" 12:00:00" ,'%Y%m%d %H:%M:%S')
time1300=dt.datetime.strptime(date+" 13:00:00" ,'%Y%m%d %H:%M:%S')
time1450=dt.datetime.strptime(date+" 14:50:00" ,'%Y%m%d %H:%M:%S')
time1500=dt.datetime.strptime(date+" 15:00:00" ,'%Y%m%d %H:%M:%S')
time1900=dt.datetime.strptime(date+" 19:00:00" ,'%Y%m%d %H:%M:%S')
plt.rcParams['font.family']='STSong'#修改了全局变量
plt.rcParams['font.size']=10
database = utils.database
collection = database["stockInfo"]

class DataLists:
    def __init__(self,dfdata:pd.DataFrame,manual=False,row_count=1,col_count=1) -> None:
        self.xs_fixed=[]
        self.codes=[]
        self.count=dfdata.index.__len__()+5
        self.avgs:list[list]=[]
        self.savgs:list[list]=[]
        self.highs:list[list]=[]
        self.lows:list[list]=[]
        self.prices:list[list]=[]
        self.prices_value:list[list]=[]
        self.tradeMoney:list[list]=[]
        self.tradeVolume:list[list]=[]
        self.maxprice_open_close:list=[]
        self.minprice_open_close:list=[]
        self.beep_times:list=[]
        self.x=[]
        self.v=[]
        self.color:list[tuple]=[]
        self.basecolor:list[tuple]=[]
        self.price_lines=[]
        self.avg_lines=[]
        self.savg_lines=[]
        self.high_lines=[]
        self.low_lines=[]
        self.trade_lines=[]
        self.trade_today_lines=[]
        self.buy_lines=[]
        self.buy_alert=[]
        self.buy_alert1=[]
        self.alert=[]
        self.axes:list[plt.Axes]=[]
        self.stockconcepts:list[pd.DataFrame]=[]
        self.dflist_all=utils.read_list_all()
        self.dflist_all.set_index("code",inplace=True)
        dfindustry:pd.DataFrame=dfdata.copy()
        dfindustry=pd.DataFrame(dfindustry,columns=["industry"])
        dfindustry.set_index("industry",inplace=True)
        dfindustry["涨跌幅"]=0
        self.industry_am0=dfindustry["涨跌幅"]
        for index in dfdata.index:
            code=dfdata.loc[index,"code"]
            self.codes.append(code)
        axindex=-1
        if not manual:
            row_count,col_count=calRowCol(count_toshow)
        self.fig,rcs=plt.subplots(row_count,col_count)
        for row in rcs:
            if col_count==1 or row_count==1:
                row=[row]
            for ax in row:
                axindex+=1
                price_line,=ax.plot([],[],'black',linewidth=0.5)
                avg_line,=ax.plot([],[],'blue',linewidth=0.7)
                savg_line,=ax.plot([],[],'red',linewidth=0.5)
                low_line,=ax.plot([],[],'black',linewidth=1,)
                self.price_lines.append(price_line)
                self.avg_lines.append(avg_line)
                self.savg_lines.append(savg_line)
                self.low_lines.append(low_line)
                ax.set_xlim(-10,totaltime)
                ax.set_ylim(y_lower,y_toper)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.grid(True)
                self.axes.append(ax)
                if axindex<min(self.count,dfdata.index.__len__()):
                    opens_x=range(int(totaltime))
                    # x轴
                    opens_y=pd.Series(opens_x)*0
                    opens,=ax.plot(opens_x,opens_y,'black',linewidth=0.5)
                    # 最低
                    opens,=ax.plot(opens_x,opens_y,'black',linewidth=0.5)
                    # 最高
        for index in range(self.count):
            try:
              min_=dfdata.loc[index,"预低"]
              low_line=pd.Series(opens_x)*0+min_
              self.lows.append(low_line)
            except:
              pass
            self.avgs.append([])
            self.savgs.append([])
            self.prices.append([])
            self.prices_value.append([])
            self.tradeMoney.append([])
            self.tradeVolume.append([])
            self.v.append(0)
            self.beep_times.append(0)
            self.color.append(base)
            self.basecolor.append(base)
            try:
                code=dfdata.loc[index,"code"]
                mid_value=dfdata.loc[index,"中线"]
            except:
                mid_value=0
            if np.isnan(mid_value):
                buy_value=0
            else:
                buy_value=mid_value
            self.buy_lines.append(buy_value)
            self.buy_alert.append(False)
            self.buy_alert1.append(False)
            self.alert.append(False)
        try:
            self.customs=dfdata["custom"]
            self.holds=dfdata["hold"]
            for index in self.holds.index:
                hold=self.holds[index]
                if np.isnan(hold):
                    self.holds[index]=0
            self.zhuans=dfdata["zhuan"]
        except:
            pass
        self.allconcept=utils.read_allconcept_all()
        self.allconcept.set_index("name",inplace=True)
        allindustry=utils.read_allindustry()
        allindustry.set_index("name",inplace=True)
        try:
            df_money_yesterday=utils.read_yesterday_money()
            df_money_yesterday.set_index("code",inplace=True)
            for index in range(len(self.codes)):
                code=self.codes[index]
                self.savgs[index]=list(df_money_yesterday.loc[code,:]*abs(y_lower)+y_lower)
            time_diff=start-time0925
            s_offset=time_diff.seconds
            dayseconed=24*60*60
            if time_diff.seconds<-dayseconed*0.5:
                s_offset+=dayseconed
            if time_diff.seconds>dayseconed*0.5:
                s_offset-=dayseconed
            for t in df_money_yesterday.columns:
                t=int(t)
                if start<time1130:
                    value=t*60-s_offset
                else:
                    value=t*60-(start-time0925-dt.timedelta(minutes=90)).seconds
                value+=x_offset
                self.xs_fixed.append(value)
        except:
            pass
        # for name in allindustry.index:
        #     try:
        #       dfcon_industry=utils.read_con_industry(name)
        #       allindustry.loc[name,"count"]=dfcon_industry.index.__len__()
        #     except:
        #       allindustry.loc[name,"count"]=0
        # self.allindustry=allindustry
def calRowCol(count:int):
    sqrt=int(pow(count,0.5))
    row=int(sqrt)+1
    col=int(count/row+1)
    diff_col=int((row*col-count)/col)
    if diff_col>=1:
        row-=diff_col
    diff_row=int((row*col-count)/row)
    if diff_row>=1:
        col-=diff_row
    return row,col

def getMinute():
    now=dt.datetime.now()
    if now<time0925:
        minute=0
    else:
        minute=int((now-time0925).seconds/60)
        if minute>=126:
            minute-=90
    if minute>=245:
        minute=245
    return minute

def filterZTByConceptWhenOpen_zxj(dflist_zt:pd.DataFrame):
    dfallconcept=utils.read_allconcept()
    dfallindustry=utils.read_allindustry()
    dfallconcept=sum_to_allconcept(dfallconcept,dflist_zt,"concept")
    dfallindustry=sum_to_allconcept(dfallindustry,dflist_zt,"industry")
    return dfallconcept,dfallindustry

def sum_to_allconcept(dfallconcept,dflist_zt,name_type)->pd.DataFrame:
    dfallconcept=pd.DataFrame(dfallconcept,columns=["name"])
    dfallconcept.set_index("name",inplace=True)
    for index in dflist_zt.index:
        code=index
        dfconcept=pd.read_csv(utils.root+"stock"+name_type+"/"+code+".csv")
        if dfconcept.index.__len__()==0:
            continue
        dfconcept.set_index(name_type,inplace=True)
        dfconcept[code]=1
        dfallconcept=dfallconcept.join(dfconcept[code])
    for index in dfallconcept.index:
        dfallconcept.loc[index,"sum"]=dfallconcept.loc[index].sum()
    dfallconcept.sort_values("sum",ascending=False,inplace=True)
    dfallconcept=pd.DataFrame(dfallconcept,columns=["sum"])
    return dfallconcept

def filterFBByConcept(dflist_zt:pd.DataFrame,name_type_industry="industry",name_type_concept="concept"):
    dfallconcept=utils.read_allconcept()
    dfallindustry=utils.read_allindustry_sub()
    try:
        dfallindustry.drop(columns=["code"],inplace=True)
    except:
        pass
    dfallindustry=ratio_to_allconcept(dfallindustry,dflist_zt,name_type_industry)
    dfallconcept=ratio_to_allconcept(dfallconcept,dflist_zt,name_type_concept)
    return dfallconcept,dfallindustry
def threadFor_ratio_to_allconcept(total,id,dflist_zt:pd.DataFrame,dfallconcept:pd.DataFrame,name_type,sums:shared_memory.ShareableList):
    for index in dflist_zt.index:
        if index%total!=id:
            continue
        code=dflist_zt.loc[index,"code"]
        dfconcept=pd.read_csv(utils.root+"stock"+name_type+"/"+code+".csv")
        if dfconcept.index.__len__()==0:
            continue
        dfconcept.set_index(name_type,inplace=True)
        dfconcept[code]=1
        dfallconcept=dfallconcept.join(dfconcept[code])
    dfcount=dfallconcept["count"]
    dfallconcept.drop(columns=["count"],inplace=True)
    i=-1
    for index in dfallconcept.index:
        i+=1
        sum=dfallconcept.loc[index].sum()/dfcount[index]
        if np.isnan(sum):
            sum=0
        # dfallconcept.loc[index,"sum"]=int(sum*10)
        sums[i]=float(sum*10)

def ratio_to_allconcept(dfallconcept,dflist_zt:pd.DataFrame,name_type)->pd.DataFrame:
    dfallconcept=pd.DataFrame(dfallconcept,columns=["name","count"])
    dfallconcept.set_index("name",inplace=True)
    threads:list[Process]=[]
    total=12
    sum_sl=(dfallconcept["count"]*0.0).tolist()
    sums=[]
    for id in range(total):
        sums.append(shared_memory.ShareableList(sum_sl))
        thread=Process(target=threadFor_ratio_to_allconcept,args=(total,id,dflist_zt,dfallconcept,name_type,sums[id]))
        threads.append(thread)
    for thread in threads:
        thread.start()
    utils.threadSBlock(threads)
    j=-1
    for index in dfallconcept.index:
        j+=1
        sum=0
        for i in range(total):
            sum+=sums[i][j]
        if sum>9:
            sum=9
        dfallconcept.loc[index,"sum"]=int(sum)
    dfallconcept.sort_values("sum",ascending=False,inplace=True)
    dfallconcept=pd.DataFrame(dfallconcept,columns=["sum"])
    return dfallconcept


def tag_fb_create_file(df:pd.DataFrame,ls:DataLists,dfinfo:pd.DataFrame,name_type_indstry="industry",name_type_concept="concept"):
    dfinfo_=dfinfo.copy()
    dflist_all=pd.DataFrame(ls.dflist_all,columns=["昨低","昨高"])
    dfinfo_=dfinfo_.join(dflist_all)
    dffb=dfinfo_.query("最高>昨高 or 最低>昨低")
    dffb["code"]=dffb.index
    dffb=pd.DataFrame(dffb,columns=["code"])
    dffb.index=range(dffb.index.__len__())
    now=dt.datetime.now()
    time0=now
    dfallconcept,dfallindustry=filterFBByConcept(dffb,name_type_indstry,name_type_concept)
    dfallconcept.to_csv("dfallconcept.csv",encoding="utf_8_sig")
    dfallindustry.to_csv("dfallindustry.csv",encoding="utf_8_sig")
    for index in df.index:
        name_industry=df.loc[index,name_type_indstry]
        i0=dfallindustry.loc[name_industry,"sum"]
        df.loc[index,"industry_zt"]=i0
        dfconcepts:pd.DataFrame=ls.stockconcepts[index].copy()
        dfconcepts=dfallconcept.join(dfconcepts["selected"])
        dfconcepts=dfconcepts.query("selected==1")
        c0=0
        c1=0
        if dfconcepts.index.__len__()>=2:
            c0=dfconcepts.iloc[0]["sum"]
            c1=dfconcepts.iloc[1]["sum"]
            c0=c0
            c1=c1
        elif dfconcepts.index.__len__()>=1:
            c0=dfconcepts.iloc[0]["sum"]
            c1=0

        df.loc[index,"concept_zt0"]=c0
        df.loc[index,"concept_zt1"]=c1
        df.loc[index,"sum_zt"]=i0+c0+c1
    df["industry_zt"]=df["industry_zt"].astype(np.float16)
    df["concept_zt0"]=df["concept_zt0"].astype(np.float16)
    df["concept_zt1"]=df["concept_zt1"].astype(np.float16)
    df=pd.DataFrame(df,columns=["industry_zt","concept_zt0","concept_zt1","sum_zt"])
    df.to_csv("dfpool.csv",index=None,encoding="utf_8_sig")

def tag_zt(df:pd.DataFrame,ls:DataLists,dfinfo:pd.DataFrame):
    dfinfo_=dfinfo.copy()
    dfinfo_.query("涨跌幅>9.5",inplace=True)
    dfinfo_["codeint"]=dfinfo_.index.astype(np.int32)
    dfinfo0=dfinfo_.query("codeint<300000")
    dfinfo1=dfinfo_.query("codeint>=300000 and codeint<600000")
    dfinfo2=dfinfo_.query("codeint>=600000 and codeint<680000")
    dfinfo3=dfinfo_.query("codeint>=680000")
    dfinfo_10=pd.concat([dfinfo0,dfinfo2])
    dfinfo_20=pd.concat([dfinfo1,dfinfo3])
    dfinfo_10=dfinfo_10.query("涨跌幅>9.5")
    dfinfo_20=dfinfo_20.query("涨跌幅>19")
    dffb=pd.concat([dfinfo_10,dfinfo_20])
    dffb=pd.DataFrame(dffb,columns=["code"])
    dffb.index=range(dffb.index.__len__())

    dfamount_stockpool=pd.DataFrame(df,columns=["成交额"])
    dfamount_stockpool=dfamount_stockpool.rename(columns={"成交额":"amount"})
    while(1):
        try:
            dffb.to_csv("dffb.csv",index=None,encoding="utf_8_sig")
            dfamount_stockpool.to_csv("amount_stockpool.csv",index=None,encoding="utf_8_sig")
            break
        except:
            continue
    while(1):
        try:
            dfpool_fb=pd.read_csv("dfpool.csv",index_col="code",dtype={"code":str})
            break
        except:
            continue
    if dfpool_fb.index[0]==df.loc[0,"code"] and dfpool_fb.index.__len__()==df.index.__len__():
        df=df.set_index("code")
        df=df.join(dfpool_fb)
        df["code"]=df.index
        df.index=range(df.index.__len__())
    else:
        df["industry_zt"]=0
        df["concept_zt0"]=0
        df["concept_zt1"]=0
        df["sum_zt"]=0
        df["amount_ratio"]=1
    return df

def tag_fb(df:pd.DataFrame,ls:DataLists,dfinfo:pd.DataFrame):
    dfinfo_=dfinfo.copy()
    dflist_all=pd.DataFrame(ls.dflist_all,columns=["昨低","昨高"])
    dfinfo_=dfinfo_.join(dflist_all)
    dffb=dfinfo_.query("最高>昨高")
    dffb=dffb.query("最低>昨低")
    dffb=pd.DataFrame(dffb,columns=["code"])
    dffb.index=range(dffb.index.__len__())
    dfzt=dfinfo_.query("涨跌幅>9")
    dfzt=pd.DataFrame(dfzt,columns=["code"])
    dfzt.index=range(dfzt.index.__len__())

    dfamount_stockpool=pd.DataFrame(df,columns=["成交额"])
    dfamount_stockpool=dfamount_stockpool.rename(columns={"成交额":"amount"})
    while(1):
        try:
            dffb.to_csv("dffb.csv",index=None,encoding="utf_8_sig")
            dfzt.to_csv("dfzt.csv",index=None,encoding="utf_8_sig")
            dfamount_stockpool.to_csv("amount_stockpool.csv",index=None,encoding="utf_8_sig")
            break
        except:
            continue
    while(1):
        try:
            dfpool_fb=pd.read_csv("dfpool.csv",index_col="code",dtype={"code":str})
            break
        except:
            continue
    if dfpool_fb.index[0]==df.loc[0,"code"] and dfpool_fb.index.__len__()==df.index.__len__():
        df=df.set_index("code")
        df=df.join(dfpool_fb)
        df["code"]=df.index
        df.index=range(df.index.__len__())
    else:
        df["industry_zt"]=0
        df["concept_zt0"]=0
        df["concept_zt1"]=0
        df["sum_zt"]=0
        df["amount_ratio"]=1
    return df

def processDfdata(dfdata:pd.DataFrame,dflist_all:pd.DataFrame):
    # dfinfo=utils.readFromMongodb("info")
    dfdata=dfdata.set_index("code")
    dfinfo=utils.readFromRedis("info")
    dfinfo=pd.DataFrame(dfinfo,columns=['code',"name",'最低','最高','avg','最新价','涨跌幅',"成交额","成交量","相对成交额","今开"])
    dfinfo.index=dfinfo["code"]
    dfinfo_=pd.DataFrame(dfinfo,index=dfdata.index)
    dfinfo_.index=range(len(dfinfo_))
    # dfpool2=dfdata.copy()
    # dfpool2.index=dfpool2["code"]
    # dfpool2=dfpool2.join(dfinfo,on="code")
    # dfpool2.index=range(len(dfpool2.index))
    # dfinfo=dfinfo.fillna(0)
    return dfinfo_,dfinfo,1

def totalseconds():
    now=dt.datetime.now()
    if now<time0915:
        return 0
    if now>time1130 and now<time1300:
        now=time1130
    totalseconds=(now-time0915).total_seconds()
    if now>=time1300:
        totalseconds-=5400
    return int(totalseconds)

def spot():
    filename=utils.server+"获取info/info.csv"
    dfinfo=pd.read_csv(filename,dtype={"code":str})
    dfinfo.set_index("code",inplace=True)
    return dfinfo

def totalseconds_float():
    now=dt.datetime.now()
    if now<time0915:
        return 0
    if now>time1130 and now<time1300:
        now=time1130
    totalseconds=(now-time0915).total_seconds()
    if now>time1300:
        totalseconds-=5400
    return totalseconds

def clamp(v,max):
    if max!=0:
        v/=max
    else:
        v=0
    v=utils.clamp(v,0,1)
    return v

def update_data(dfpool2:pd.DataFrame,ls:DataLists):
    now=dt.datetime.now()
    for index in dfpool2.index:
        row=dfpool2.loc[index,:]
        code=dfpool2.loc[index,'code']
        am=dfpool2.loc[index,'涨跌幅']
        newprice=dfpool2.loc[index,'最新价']
        start_price=newprice/(1+am/100)
        avg_price=dfpool2.loc[index,'avg']
        if avg_price==None:
            avg_price=newprice
        am_avg=(avg_price/start_price-1)*100
        if now>=time0930:
            try:
                ls.tradeMoney[index].append(dfpool2.loc[index,'成交额'])
                ls.tradeVolume[index].append(dfpool2.loc[index,'成交量'])
            except:
                pass
        startIndex_savg=0
        am_savg=am_avg
        window=5
        if ls.tradeMoney[0].__len__()>=window:
            startIndex_savg=-window
        if now>=time0930 and ls.tradeVolume[index][-1]!=ls.tradeVolume[index][startIndex_savg]:
            am_savg=0.01*(ls.tradeMoney[index][-1]-ls.tradeMoney[index][startIndex_savg])/(ls.tradeVolume[index][-1]-ls.tradeVolume[index][startIndex_savg])
            am_savg=(am_savg/start_price-1)*100
        else:
            pass
        ls.prices[index].append(float(am))
        ls.prices_value[index].append(float(newprice))
        try:
            ls.avgs[index].append(float(row["相对成交额"]*(-y_lower)+y_lower))
        except:
            ls.avgs[index].append(y_lower)
        dfpool2.loc[index,'am_avg']=am_avg
def awake(now:dt.datetime):
    if now<time0915 or (now>time0925 and now<time0930) or (now>time1130 and now<time1300) or (now>time1500):
        return False
    return True