from pandas.core.frame import DataFrame
import gezgin as gz
import pandas as pd
class enOnBir():
    def __init__(self,arama=None):
        self.adres="https://www.n11.com/"
        self.n11=gz.urunArama(self.adres)#ana adres
        if not arama:
            arama=input(self.n11.adres+' sitesinde aranacak: ')#kullanıcıdan giriş al
        self.arama=arama

    def Tara(self):
        self.n11.adresEki(aranacak=self.arama,sorguEk='arama?q=',sayfaEk='pg=',filtreEk="srt=REVIEWS&utpn=4")#ek parçaları
        ### Tüm sayfaları tarıyabilmek için ilk sayfadan çekilecek bilgiler  ####
        self.n11.maxUrun=1400
        konteyner=gz.cekilecek("div","id","view")
        toplamUrunSayisi=gz.cekilecek("div","class","resultText",("<strong>",1),("</strong>",0))
        sayfadakiUrunler=gz.cekilecek("li","class","column",Konteyner=konteyner)#herbir ürünün içinde bulunduğu konteynera ait: tag,attribute, value
        sonuc=self.n11.anaSayfa(sayfadakiUrunler,toplamUrunSayisi)
        if sonuc==False: return None
        ############ her bir ürüne ait çekilecek bilginin etiketi ve bulunduğu nokta ##################
        self.n11.sutunlar={"Adı":gz.cekilecek("h3","class","productName"),# <h3 title="....."> kısmını çeker
                    "Puan":gz.cekilecek("span","class",Konteyner=gz.cekilecek("div","class","ratingCont")),#konteyner: sayfanın tamamında değil belirtilen etiket içinde aramayı gerçekleştirir.
                    "Eski fiyat":gz.cekilecek("del"),# <del>.....<> kısmını çeker
                    "Fiyatı":gz.cekilecek("ins",ayrac1=("<span",0),ayrac2=("<ins>",1)),#ayrac parametresi split uygulayarak gereksiz kısmları temizler
                    "Oylanma":gz.cekilecek("span","class","ratingText"),#<span class="number-of-reviews">.....<> kısmını çeker
                    "Link":gz.cekilecek("a","href")}#Çekilecek olan verilerin excel tablosunda görüntüleneceği sütunlar
        listemiz=self.n11.sayfalardaGez()#tüm sayfalar taranarak liste elde edilir
        liste=pd.DataFrame(listemiz,columns=self.n11.sutunlar.keys())#pandas kütüphanesi ile verileri kolayca işleyip excele atabiliriz    
        return liste

    def __str__(self):
        return self.arama

if __name__=="__main__":
    n11=enOnBir()
    arama=str(n11)
    sayfa1=n11.Tara()
    if type(sayfa1)==pd.DataFrame: 
        for sutun,satir in sayfa1.iterrows():
            satir["Puan"]=int(satir["Puan"][8:])*5/100
            satir["Oylanma"]=int(satir["Oylanma"].replace("(","").replace(")","").replace(",",""))
            satir["Fiyatı"]=float(((satir["Fiyatı"].split("\n")[0]).replace(".","")).replace(",","."))
            try:satir["Eski fiyat"]=float(((satir["Eski fiyat"].split(" ")[0]).replace(".","")).replace(",","."))
            except:satir["Eski fiyat"]=satir["Fiyatı"]
        sayfa1["İnd.%"]=1-sayfa1["Fiyatı"]/sayfa1["Eski fiyat"]
        sayfa1=sayfa1[["Adı","Puan","Oylanma","Eski fiyat","Fiyatı","İnd.%","Link"]]#sütun sıralamasını değiştirme
        sayfa1.to_excel(arama+"-n11.xlsx", sheet_name=arama,index=False) #index sütunu olmaksızın excel'e aktarma