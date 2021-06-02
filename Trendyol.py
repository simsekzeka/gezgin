import gezgin as gz
import pandas as pd
class trendY():
    def __init__(self,arama=None):
        self.adres="https://www.trendyol.com"
        self.ty=gz.urunArama(self.adres)#ana adres
        if not arama:
            arama=input(self.ty.adres+' sitesinde aranacak: ')#kullanıcıdan giriş al
        self.arama=arama
    
    def Tara(self):
        self.ty.adresEki(aranacak=self.arama,sorguEk='sr?q=',sayfaEk='pi=',filtreEk="pr=4&sst=MOST_RATED")#URL ek parçaları
        ### Tüm sayfaları tarıyabilmek için ilk sayfadan çekilecek bilgiler  ####
        sayfadakiUrunler=gz.cekilecek("div","class","p-card-wrppr")
        toplamUrunSayisi=[gz.cekilecek("div","class","dscrptn",('dscrptn">',1),(" sonuç",0)),
                        gz.cekilecek("div","class","dscrptn",('<!-- -->',1))]#ALTERNATİF içerik için bunu dene
        self.ty.maxUrun=4992#çok fazla sonuç bulsa da sitenin görüntülediği ürün sayısında sınır var.
        sonuc=self.ty.anaSayfa(sayfadakiUrunler,toplamUrunSayisi)
        if sonuc==False: return None
        ######## her bir ürüne ait çekilecek bilginin etiketi ve bulunduğu nokta ##################
        self.ty.sutunlar={"Marka":gz.cekilecek("span","class","prdct-desc-cntnr-ttl"),
                    "Ürün":gz.cekilecek("span","class","prdct-desc-cntnr-name hasRatings"),
                    "Puan":gz.cekilecek("div","class","star-w",("width:",1),("%",0),sira=4),
                    "Eski fiyat":gz.cekilecek("div","class","prc-box-orgnl"),
                    "Fiyatı":gz.cekilecek("div","class","prc-box-sllng"),
                    "Oylanma":gz.cekilecek("span","class","ratingCount"),#<span class="number-of-reviews">.....<> kısmını çeker
                    "Link":gz.cekilecek("a","href")}#Çekilecek olan verilerin excel tablosunda görüntüleneceği sütunlar
        listemiz=self.ty.sayfalardaGez(20)#tüm sayfalar taranarak liste elde edilir
        liste=pd.DataFrame(listemiz,columns=self.ty.sutunlar.keys())#listeyi, pandas'a sütun başlıklarıyla birlikte aktar       
        return liste

    def __str__(self) -> str:
        return self.arama


if __name__=="__main__":
    tY=trendY()
    arama=str(tY)
    sayfa1=tY.Tara()
    if type(sayfa1)==pd.DataFrame: 
        for sutun,satir in sayfa1.iterrows():
            satir["Oylanma"]=int(satir["Oylanma"].replace("(","").replace(")",""))
            if satir["Puan"]=="100": satir["Puan"]=5.00
            else: satir["Puan"]=float("4."+satir["Puan"])
            satir["Fiyatı"]=float(((satir["Fiyatı"].split(" ")[0]).replace(".","")).replace(",","."))
            if  satir["Eski fiyat"]=="": satir["Eski fiyat"]=satir["Fiyatı"]
            else: satir["Eski fiyat"]=float(((satir["Eski fiyat"].split(" ")[0]).replace(".","")).replace(",","."))
            satir["Link"]=tY.adres+ satir["Link"]
        sayfa1["İndirim"]=1-sayfa1["Fiyatı"]/sayfa1["Eski fiyat"] # (indirim %'si)
        sayfa1=sayfa1[["Marka","Ürün","Puan","Oylanma","Eski fiyat","Fiyatı","İndirim","Link"]]#sütun sıralamasını değiştirme
        sayfa1.to_excel(arama+"-ty.xlsx", sheet_name=arama,index=False) #index sütunu olmaksızın excel'e aktarma
        input()
