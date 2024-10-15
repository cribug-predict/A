import pandas as pd
import numpy as np
from tkinter import ttk
from tkinter import *
from datetime import datetime
from custom_package import utils
from functools import partial
import mplfinance as mpf
from matplotlib import pyplot as plt
import time
import datetime as dt
import pyttsx3

root=utils.root
engine:pyttsx3.Engine = pyttsx3.init()
engine.setProperty('rate', 400)
length=0
dfhists=[]
mins=[]
maxs=[]
zts=[]
end_date:dt.datetime=utils.getNextTradeday(dt_type=True)[0]
end_date=end_date.date()
start_date=end_date-dt.timedelta(days=360)
fig=None
ax1=None
ax2=None
list_=[0,True,True,5,0]
fileName="stock"
def select_read(dflist:pd.DataFrame,hour=6):
    # dflist=dflist.loc[::-1]
    dflist=utils.reindex(dflist)
    utils.to_stock(dflist,"stock1")
    index=-1
    old=pd.DataFrame([])
    if utils.isExistAndNew("stock.csv",hour,slow=True):
        old=pd.read_csv("stock.csv")
        utils.formatDataframeCode(old)
        for index in dflist.index:
            code=dflist.loc[index,"code"]
            if code==old["code"].iloc[-1]:
                break
    dflist=dflist.iloc[index+1:]
    utils.reindex(dflist)
    return dflist,old

def deselect_read(dflist=pd.DataFrame([])):
    if dflist.index.__len__()==0:
        dflist=pd.read_csv("stock.csv",dtype={"code":str})
    # utils.formatDataframeCode(dflist)
    # dflist=dflist.loc[::-1]
    dflist=utils.reindex(dflist)
    utils.to_stock(dflist,"stock1")
    old=pd.DataFrame([])
    return dflist,old

def speak(name:str):
    pyttsx3.speak(name)

def reset(list_:list):
    list_[0]=0
    list_[1]=True
def pause(list_:list):
    list_[2]=not list_[2]

def setDiff(list_:list,entry0:ttk.Entry):
    try:
        list_[3]=int(entry0.get())
    except:
        list_[3]=1
def view(list_:list,length,direction=1):
    list_[0]=utils.clamp(list_[0]+list_[3]*direction,0,length-1)
    list_[1]=True

def view0(list_:list,length):
    list_[0]=utils.clamp(list_[0]+1,0,length-1)
    list_[1]=True

def mouseWheel(e:Event,list_:list,length:int):
    delta=-int(e.delta/120)
    list_[0]=utils.clamp(list_[0]+delta,0,length-1)
    list_[1]=True
    
def add_select(list_:list[int],dflist:pd.DataFrame,codeList:list,nameList:list,length):
    index=list_[0]
    code=dflist.loc[index,"code"]
    name=dflist.loc[index,"name"]
    # try:
    #     code=utils.formatCodeint(int(code))
    # except:
    #     pass
    print(name)
    cl=codeList.__len__()
    if cl==0 or code!=codeList[cl-1]:
        codeList.append(code)
        nameList.append(name)
        dftosave=pd.DataFrame([])
        codeSeries=pd.Series(codeList,dtype=str)
        nameSeries=pd.Series(nameList,dtype=str)
        dftosave["code"]=codeSeries
        dftosave["name"]=nameSeries
        # dftosave["industry"]=industrySeries
        dftosave.to_csv(fileName+".csv",index=None,encoding="utf_8_sig")
        time=datetime.now()
        time=datetime.strftime(time,"%Y%m%d")
        # dftosave.to_csv("record/"+time+".csv",index=None,encoding="utf_8_sig")
    view0(list_,length)

def add_deselect(list_:list[int],dflist:pd.DataFrame,codeList:list,nameList:list,length):
    index=list_[0]
    code=dflist.loc[index,"code"]
    cl=codeList.__len__()
    if cl==0 or code!=codeList[cl-1]:
        codeList.append(index)
        dftosave=dflist.drop(index=codeList)
        dftosave.to_csv(fileName+".csv",index=None,encoding="utf_8_sig")
    view0(list_,length)

def add_pause(list_:list[int],dflist:pd.DataFrame,codeList:list,nameList:list,industryList:list,length):
    pause(list_)

def gui(old:pd.DataFrame,mode="select"):
    dflist=list_[4]
    if mode=="select":
        add=add_select
    elif mode=="deselect":
        add=add_deselect
    elif mode=="pause":
        add=add_pause
    begintime=datetime.now()
    root = Tk()
    root.wm_attributes("-topmost", 1)
    frm = ttk.Frame(root, padding=10)
    frm.place(x=100,y=0)
    frm.grid()
    codeList=[]
    nameList=[]
    industryList=[]
    global length
    if old.index.__len__()>0:
        codeList=old["code"].tolist()
        nameList=old["name"].tolist()
        # industryList=old["industry"].tolist()

    ttk.Button(frm, text="Reset", command=partial(reset,list_)).grid(column=0, row=0)
    ttk.Button(frm, text="Pause", command=partial(pause,list_)).grid(column=0, row=1)
    entry0=ttk.Entry(frm,text="diff",width=10)
    entry0.grid(column=0, row=3)
    ttk.Button(frm, text="SetDiff", command=partial(setDiff,list_,entry0)).grid(column=0, row=2)
    btnext=ttk.Button(frm, text="Next", command=partial(view,list_,length))
    btnext.grid(column=1, row=0)
    btview=ttk.Button(frm, text="View")
    btview.bind_all('<MouseWheel>',lambda e:mouseWheel(e,list_,length))
    btclick=ttk.Button(frm, text="Next")
    btclick.bind_all('<Button-1>',lambda e:view0(list_,length))

    btlast=ttk.Button(frm, text="Last", command=partial(view,list_,length,-1))
    btlast.grid(column=1, row=1)
    btadd=ttk.Button(frm, text="Add", command=partial(add,list_,dflist,codeList,nameList,length))
    btadd.bind_all('<Button-3>',lambda e:add(list_,dflist,codeList,nameList,length))
    root.mainloop()

# def prepareData(code:str,length=280,datafolder="../emdata/data/"):
#     dfhist=pd.read_csv(datafolder+code+".csv")
#     dfhist=dfhist.loc[:length]
#     dfhist=dfhist.rename(columns={"日期":"Date","开盘":"Open","收盘":"Close","最高":"High","最低":"Low","成交量":"Volume"})
#     dfhist=pd.DataFrame(dfhist,columns=["Date","Open","Close","High","Low","Volume"])
#     dfhist.index=pd.DatetimeIndex(dfhist["Date"])
#     dfhist=dfhist.reindex(index=dfhist.index[::-1])
#     return dfhist

def mpf_prepareData(code:str,count=260)->pd.DataFrame:
    today=utils.getTradeDay(dot="-")[0]
    # dfhist=pd.read_csv(root+"data/"+code+".csv")
    dfhist=pd.read_csv(root+"data/"+code+".csv")
    # try:
    #     a=int(code)
    # except:
    #     if dfhist.loc[0,"日期"]!=today:
    #         dfhist=pd.read_csv(root+"newdata/"+code+".csv")
    dfhist=dfhist.reindex(index=dfhist.index[::-1])
    for index in dfhist.index:
        if not np.isnan(dfhist.loc[index,"开盘"]):
            break
    dfhist=dfhist.iloc[-min(count,index):]
    dfhist=dfhist.rename(columns={"日期":"Date","开盘":"Open","收盘":"Close","最高":"High","最低":"Low","成交量":"Volume"})
    dfhist=pd.DataFrame(dfhist,columns=["Date","Open","Close","High","Low","Volume"])
    dfhist.index=pd.DatetimeIndex(dfhist["Date"])
    return dfhist

def mpf_initial():
    plt.rcParams['font.size']=10
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 解决mplfinance绘制输出中文乱码
    mc = mpf.make_marketcolors(up='white',down='black',volume="inherit",edge="black")
    s = mpf.make_mpf_style(marketcolors=mc,rc={'font.family': 'SimHei'})
    return s

s=mpf_initial()
def animate(a):
    dflist=list_[4]
    global length,dfhists,s,start_date,end_date,fig,ax1,ax2,zts
    fig.canvas.draw()
    plt.pause(0.001)
    while(not list_[1]):
        if not list_[2]:
            time.sleep(0.3)
            view0(list_,dflist.index.__len__())
        pass
    index=list_[0]
    print(dflist.loc[list_[0],"name"])
    list_[1]=False
    code=dflist.loc[index,"code"]
    industry=dflist.loc[index,"industry_sub"]
    dfhist=dfhists[index]
    name=dflist.loc[index,"name"]
    ax1.clear()
    ax2.clear()
    mav=(60,120,240)
    if dfhist.index.__len__()<240:
        mav=(60,120)
    mpf.plot(dfhist,type="candle",mav=mav,ax=ax1,volume=ax2,
        xlim=(start_date,end_date),
        ylim=(mins[index],maxs[index]),
        axtitle=str(index)+"/"+str(length)+"\n"+industry+"\n"+code+" "+name+"_"+zts[index],style=s)
    
def createlistsFromDflist(dflist:pd.DataFrame,daycount=300):
    global length,s,fig,ax1,ax2,mins,maxs,zts
    list_[4]=dflist
    length=dflist.__len__()
    dflist_=utils.read_list()
    dflist_.index=dflist_["code"]
    for index in dflist.index:
        print(index)
        code=dflist.loc[index,"code"]
        dfhist=mpf_prepareData(code,daycount)
        dfhists.append(dfhist)
        try:
            industry=dflist_.loc[code,"industry_sub"]
        except:
            try:
                industry=dflist_.loc[code,"industry"]
            except:
                industry=""
        dflist.loc[index,"industry_sub"]=industry
        try:
            zts.append(str(int(dflist_.loc[code,"涨停次数"])))
        except:
            zts.append("")
        temp=dfhist
        ratio=3
        min_=temp["Low"].min()
        max_=temp["High"].max()
        mins.append(min_)
        maxs.append(max_)
    fig, axes = mpf.plot(dfhists[0],style=s,returnfig=True,volume=True,
                         figsize=(4,3),panel_ratios=(2,1))
    ax1 = axes[0]
    ax2 = axes[2]
    plt.subplots_adjust(left=0,right=1,bottom=0.03,top=1,hspace=0.22,wspace=0.02)