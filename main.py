import n11 as N
import HepsiBurada as H
import Trendyol as T
import pandas as pd
arama=input('Aranacak (n11,HepsiBurada,Trendyol): ')
#######################################
n11=N.enOnBir(arama)
sayfa1=n11.Tara()
if type(sayfa1)==pd.DataFrame: 
    for sutun,satir in sayfa1.iterrows():
        satir["Puan"]=int(satir["Puan"][8:])*5/100
        satir["Oylanma"]=int(satir["Oylanma"].replace("(","").replace(")","").replace(",",""))
        satir["Fiyatı"]=float(((satir["Fiyatı"].split("\n")[0]).replace(".","")).replace(",","."))
        try:satir["Eski fiyat"]=float(((satir["Eski fiyat"].split(" ")[0]).replace(".","")).replace(",","."))
        except:satir["Eski fiyat"]=satir["Fiyatı"]
    sayfa1["İndirim"]=1-sayfa1["Fiyatı"]/sayfa1["Eski fiyat"]
    sayfa1["site"]="N11"
    sayfa1=sayfa1[["site","Adı","Puan","Oylanma","Eski fiyat","Fiyatı","İndirim","Link"]]
#######################################
hB=H.hepsiB(arama)
sayfa2=hB.Tara()
if type(sayfa2)==pd.DataFrame: 
    for sutun,satir in sayfa2.iterrows():
        satir["Oylanma"]=int(satir["Oylanma"].replace("(","").replace(")",""))
        satir["Puan"]=int(satir["Puan"].split(": ")[1].split("%")[0])*5/100
        satir["Fiyatı"]=float(((satir["Fiyatı"].split(" ")[0]).replace(".","")).replace(",","."))
        if  satir["Eski fiyat"]=="": satir["Eski fiyat"]=satir["Fiyatı"]
        else: satir["Eski fiyat"]=float(((satir["Eski fiyat"].split(" ")[0]).replace(".","")).replace(",","."))
        satir["Link"]=hB.adres+satir["Link"]
    sayfa2["İndirim"]=1-sayfa2["Fiyatı"]/sayfa2["Eski fiyat"] 
    sayfa2["site"]="HepsiBurada"
    sayfa2=sayfa2[["site","Adı","Puan","Oylanma","Eski fiyat","Fiyatı","İndirim","Link"]]
#######################################
tY=T.trendY(arama)
sayfa3=tY.Tara()
if type(sayfa3)==pd.DataFrame: 
    for sutun,satir in sayfa3.iterrows():
        satir["Oylanma"]=int(satir["Oylanma"].replace("(","").replace(")",""))
        if satir["Puan"]=="100": satir["Puan"]=5.00
        else: satir["Puan"]=float("4."+satir["Puan"])
        satir["Fiyatı"]=float(((satir["Fiyatı"].split(" ")[0]).replace(".","")).replace(",","."))
        if  satir["Eski fiyat"]=="": satir["Eski fiyat"]=satir["Fiyatı"]
        else: satir["Eski fiyat"]=float(((satir["Eski fiyat"].split(" ")[0]).replace(".","")).replace(",","."))
        satir["Link"]=str(tY.adres+satir["Link"])
    sayfa3["İndirim"]=1-sayfa3["Fiyatı"]/sayfa3["Eski fiyat"]
    sayfa3["Adı"]=sayfa3["Ürün"]#+"|"+sayfa3["Marka"]
    sayfa3["site"]="Trendyol"
    sayfa3=sayfa3[["site","Adı","Puan","Oylanma","Eski fiyat","Fiyatı","İndirim","Link"]]
######################################
    kitap=pd.concat([sayfa1,sayfa2,sayfa3])
    with pd.ExcelWriter(arama+'.xlsx') as writer:  
        kitap.to_excel(writer, sheet_name=arama,index=False) 
 