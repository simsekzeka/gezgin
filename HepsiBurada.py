import gezgin as gz
import pandas as pd
class hepsiB():
    def __init__(self,arama=None):
        self.adres="https://www.hepsiburada.com"
        self.hb=gz.urunArama(self.adres)#ana adres
        if not arama:
            arama=input(self.hb.adres+' sitesinde aranacak: ')#kullanıcıdan giriş al
        self.arama=arama
    
    def Tara(self):
        self.hb.adresEki(aranacak=self.arama,sorguEk='ara?q=',sayfaEk='sayfa=',filtreEk="puan=4-max&siralama=yorumsayisi")#ek parçaları
        ### Tüm sayfaları tarıyabilmek için ilk sayfadan çekilecek bilgiler  ####
        sayfadakiUrunler=gz.cekilecek("li","data-index","1")#herbir ürünün içinde bulunduğu konteynera ait: tag,attribute, value
        toplamUrunSayisi=[gz.cekilecek("span","class","totalCount"),
                            gz.cekilecek("strong","class","result-count tolkien")]#birinde yoksa diğerine bakar (liste kullanıyoruz)
        self.hb.maxUrun=1200
        sonuc=self.hb.anaSayfa(sayfadakiUrunler,toplamUrunSayisi)
        if sonuc==False: return None
        ############ her bir ürüne ait çekilecek bilginin etiketi ve bulunduğu nokta ##################
        self.hb.sutunlar={"Adı":gz.cekilecek("h3","title"),# <h3 title="....."> kısmını çeker
                    "Eski fiyat":gz.cekilecek("del"),# <del>.....<> kısmını çeker
                    "Fiyatı":gz.cekilecek("a","data-price"),
                    "Puan":gz.cekilecek("span","style",Konteyner=gz.cekilecek("span","class","ratings")),
                    "Oylanma":gz.cekilecek("span","class","number-of-reviews"),#<span class="number-of-reviews">.....<> kısmını çeker
                    "Link":gz.cekilecek("a","href")}#Çekilecek olan verilerin excel tablosunda görüntüleneceği sütunlar
        listemiz=self.hb.sayfalardaGez()#tüm sayfalar taranarak liste elde edilir
        liste=pd.DataFrame(listemiz,columns=self.hb.sutunlar.keys())#pandas kütüphanesi ile verileri kolayca işleyip excele atabiliriz       
        return liste
    
    def __str__(self) -> str:
        return self.arama
        
if __name__=="__main__":
    hB=hepsiB()
    arama=str(hB)
    sayfa1=hB.Tara()
    if type(sayfa1)==pd.DataFrame: 
        for sutun,satir in sayfa1.iterrows():
            satir["Oylanma"]=int(satir["Oylanma"].replace("(","").replace(")",""))
            satir["Puan"]=int(satir["Puan"].split(": ")[1].split("%")[0])*5/100
            satir["Fiyatı"]=float(((satir["Fiyatı"].split(" ")[0]).replace(".","")).replace(",","."))
            if  satir["Eski fiyat"]=="": satir["Eski fiyat"]=satir["Fiyatı"]
            else: satir["Eski fiyat"]=float(((satir["Eski fiyat"].split(" ")[0]).replace(".","")).replace(",","."))
            satir["Link"]=hB.adres+satir["Link"]
        sayfa1["İndirim"]=1-sayfa1["Fiyatı"]/sayfa1["Eski fiyat"] 
        sayfa1=sayfa1[["Adı","Puan","Oylanma","Eski fiyat","Fiyatı","İndirim","Link"]]
        sayfa1.to_excel(arama+"-hb.xlsx", sheet_name=arama,index=False) 
        input()