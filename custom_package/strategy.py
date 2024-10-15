from custom_package import utils
import pandas as pd

def getDfResult(filter:callable,minimum:int=2)->pd.DataFrame:
    dflist=utils.read_list()
    dfpool1=filter(dflist)
    name=""
    dfcache=dfpool1.copy()
    indexToSave=[]
    for index in dfpool1.index:
        insub=dfpool1.loc[index,"industry_sub"]
        if insub!=name:
            indexToSave.append(index)
            name=insub
    dfpool1=pd.DataFrame(dfpool1,index=indexToSave)
    dfpool1=pd.DataFrame(dfpool1,columns=["industry_sub"])
    dfpool1["name"]=dfpool1["industry_sub"]
    dfpool1["code"]=dfpool1["name"]
    dfpool1=pd.DataFrame(dfpool1,columns=["code","name"])
    indexToDrop=[]
    sum=0
    for index in dfpool1.index:
        name=dfpool1.loc[index,"name"]
        dfslice=dfcache.query("industry_sub==@name")
        count=len(dfslice.index)
        sum+=count
        name+=str(count)
        dfpool1.loc[index,"name"]=name
        if count<minimum:
            indexToDrop.append(index)
    print(sum)
    dfpool1=dfpool1.drop(index=indexToDrop)
    indexToDrop=[]
    # for index in dfpool1.index:
    #     industry=dfpool1.loc[index,"code"]
    #     # df=utils.readFromMongodb(industry,"industry_sub_zt2")
    #     df=utils.readFromMongodb(industry,"industry_sub_zt2")
    #     if df is None:
    #         indexToDrop.append(index)
    dfpool1=dfpool1.drop(index=indexToDrop)
    return dfpool1

def down0(dflist:pd.DataFrame):
    dfpool=dflist
    # dfpool1=dflist.query("涨停次数_week>=1")
    dfpool=dfpool.query("连板次数>=2")
    dfpool1=dfpool.copy()
    indexToSave=[]
    for index in dfpool1.index:
        code=dfpool1.loc[index,'code']
        try:
            dfhist=utils.read_hist(code)
        except:
            print("no"+code)
            continue
        utils.reindex(dfhist)
        dfhist_count=len(dfhist.index)
        if dfhist_count<120:
            continue

        am=dfhist["涨跌幅"]
        open=dfhist['开盘']
        close=dfhist["收盘"]
        maxprice=dfhist["最高"]
        minprice=dfhist["最低"]
        am_max=(maxprice/close.shift(-1))*100-100
        am_min=(minprice/close.shift(-1))*100-100
        am_open=(open/close.shift(-1))*100-100
        close_=close.shift(-1)
        hsl=dfhist["换手率"]

        sub=close-open
        am_sub=(close/open-1)*100
        left=am_max-am_open
        right=am_max-am

        ma10=dfhist["ma10"]
        ma20=dfhist["ma20"]
        ma30=dfhist["ma30"]
        ma60=dfhist["ma60"]
        ma120=dfhist["ma120"]
        ma240=dfhist["ma240"]

        try:
            if utils.continueList([
                condition0(dfhist,0) or condition0(dfhist,1) or condition0(dfhist,2), 
                am[0]<0,
                close[0]<30,
                close[0]>3.3,
                close[0]/ma60[0]<1.15,
            ]):
                continue
        except:
            print(code)
            continue
        dfpool1.loc[index,'昨开']=open[0]
        dfpool1.loc[index,'昨收']=close[0]
        dfpool1.loc[index,'昨换']=hsl[0]
        indexToSave.append(index)

    dfpool1=pd.DataFrame(dfpool1,index=indexToSave)
    dfpool1=pd.DataFrame(dfpool1,columns=["code","name","industry_sub","连板次数"])
    return dfpool1


def zhongchun_yaogu(dflist:pd.DataFrame):
    dfpool=dflist
    dfpool=dfpool.query("连板次数>=4")
    dfpool1=dfpool.copy()
    indexToSave=[]
    for index in dfpool1.index:
        code=dfpool1.loc[index,'code']
        try:
            dfhist=utils.read_hist(code)
        except:
            print("no"+code)
            continue
        utils.reindex(dfhist)
        dfhist_count=len(dfhist.index)
        if dfhist_count<120:
            continue

        am=dfhist["涨跌幅"]
        open=dfhist['开盘']
        close=dfhist["收盘"]
        low=dfhist["最低"]
        hsl=dfhist["换手率"]
        # ma60=dfhist["ma60"]

        if utils.continueList([
            (open[0]/low[0]>1.04 and close[0]/low[0]>1.03) or condition0(dfhist,0) or condition0(dfhist,1) or condition0(dfhist,2) or am[1]>9.5 or am[2]>9.5 or am[3]>9.5,
            close[0]<40,
            close[0]>1.5,
            close[0]/ma60[0]<1.2,
        ]):
            continue
        dfpool1.loc[index,'昨开']=open[0]
        dfpool1.loc[index,'昨收']=close[0]
        dfpool1.loc[index,'昨换']=hsl[0]
        indexToSave.append(index)

    dfpool1=pd.DataFrame(dfpool1,index=indexToSave)
    dfpool1=pd.DataFrame(dfpool1,columns=["code","name","industry_sub","连板次数"])
    return dfpool1

def zhongchun1(dflist:pd.DataFrame):
    dfpool1=dflist
    indexToSave=[]
    for index in dfpool1.index:
        code=dfpool1.loc[index,'code']
        try:
            dfhist=utils.read_hist(code)
        except:
            print("no"+code)
            continue
        utils.reindex(dfhist)
        dfhist_count=len(dfhist.index)
        if dfhist_count<120:
            continue

        am=dfhist["涨跌幅"]
        open=dfhist['开盘']
        close=dfhist["收盘"]
        low=dfhist["最低"]
        high=dfhist["最高"]
        hsl=dfhist["换手率"]
        # ma60=dfhist["ma60"]
        try:
            if utils.continueList([
                (open[0]/low[0]>1.04 and close[0]/low[0]>1.03) or condition1(dfhist,0) or condition1(dfhist,1) or condition1(dfhist,2) or am[1]>9.5 or am[2]>9.5 or am[3]>9.5,
                # close[0]/ma60[0]<2,
            ]):
                continue
        except:
            print(code)
            continue
        dfpool1.loc[index,'昨开']=open[0]
        dfpool1.loc[index,'昨收']=close[0]
        dfpool1.loc[index,'昨换']=hsl[0]
        indexToSave.append(index)
    dfpool1=pd.DataFrame(dfpool1,index=indexToSave)
    dfpool1=pd.DataFrame(dfpool1,columns=["code","name","industry_sub","连板次数"])
    return dfpool1

def zhongchun2(dflist:pd.DataFrame):
    dfpool1=dflist
    dfpool1=dfpool1.query("连板次数>=2").copy()
    indexToSave=[]
    for index in dfpool1.index:
        code=dfpool1.loc[index,'code']
        try:
            dfhist=utils.read_hist(code)
        except:
            print("no"+code)
            continue
        utils.reindex(dfhist)
        dfhist_count=len(dfhist.index)
        if dfhist_count<120:
            continue

        am=dfhist["涨跌幅"]
        open=dfhist['开盘']
        close=dfhist["收盘"]
        low=dfhist["最低"]
        hsl=dfhist["换手率"]
        # ma60=dfhist["ma60"]
        try:
            if utils.continueList([
                (close[1]/low[0]>1.04 and close[0]/low[0]>1.03) or condition0(dfhist,0) or condition0(dfhist,1) or condition0(dfhist,2) or condition0(dfhist,3) or am[1]>9.5 or am[2]>9.5 or am[3]>9.5,
                # close[0]/ma60[0]<2,
                close[0]<open[0],
                close[0]>2.2
            ]):
                continue
        except:
            print(code)
            continue
        dfpool1.loc[index,'昨开']=open[0]
        dfpool1.loc[index,'昨收']=close[0]
        dfpool1.loc[index,'昨换']=hsl[0]
        indexToSave.append(index)
    dfpool1=pd.DataFrame(dfpool1,index=indexToSave)
    # dfpool1=pd.DataFrame(dfpool1,columns=["code","name","industry_sub","连板次数"])
    return dfpool1

def zhongchun_big(dflist:pd.DataFrame):
    dfpool1=dflist
    dfpool1=dfpool1.query("连板次数>=2").copy()
    indexToSave=[]
    for index in dfpool1.index:
        code=dfpool1.loc[index,'code']
        try:
            dfhist=utils.read_hist(code)
        except:
            print("no"+code)
            continue
        utils.reindex(dfhist)
        dfhist_count=len(dfhist.index)
        if dfhist_count<120:
            continue

        am=dfhist["涨跌幅"]
        open=dfhist['开盘']
        close=dfhist["收盘"]
        low=dfhist["最低"]
        hsl=dfhist["换手率"]
        ma60=dfhist["ma60"]
        ma120=dfhist["ma120"]
        diff=(close-ma60).copy()
        
        try:
            if utils.continueList([
                (close[1]/low[0]>1.04 and close[0]/low[0]>1.03) or condition0(dfhist,0) or condition0(dfhist,1) or condition0(dfhist,2) or condition0(dfhist,3) or condition0(dfhist,4) or am[1]>9.5 or am[2]>9.5 or am[3]>9.5,
                close[0]/ma60[0]<1.2,
                # close[0]<open[0],
                close[0]>2.2,
                diff.iloc[:40].max()>0,
                (ma60-ma120).iloc[:80].max()<0,
                ma60[0]<ma120[0]
            ]):
                continue
        except:
            print(code)
            continue
        dfpool1.loc[index,'昨开']=open[0]
        dfpool1.loc[index,'昨收']=close[0]
        dfpool1.loc[index,'昨换']=hsl[0]
        indexToSave.append(index)
    dfpool1=pd.DataFrame(dfpool1,index=indexToSave)
    # dfpool1=pd.DataFrame(dfpool1,columns=["code","name","industry_sub","连板次数"])
    return dfpool1



def condition0(dfhist:pd.DataFrame,dayIndex:int):
    am=dfhist["涨跌幅"]
    open=dfhist['开盘']
    close=dfhist["收盘"]
    maxprice=dfhist["最高"]
    am_max=(maxprice/close.shift(-1))*100-100
    am_open=(open/close.shift(-1))*100-100
    left=am_max-am_open
    right=am_max-am

    up=dfhist["up"][dayIndex]
    return (up>=3.5 or left[dayIndex]>5) and right[dayIndex]>up/3

def condition1(dfhist:pd.DataFrame,dayIndex:int):
    open=dfhist['开盘']
    close=dfhist["收盘"]
    maxprice=dfhist["最高"]
    am_max=(maxprice/close.shift(-1))*100-100
    am_open=(open/close.shift(-1))*100-100

    left=am_max-am_open

    up=dfhist["up"]
    return (up[dayIndex]>=3.5 or left[dayIndex]>4.5)