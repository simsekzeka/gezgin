import threading
import requests
from bs4 import BeautifulSoup,element
from urllib.parse import quote
import datetime as dt

class Gezgin(object):

    def __init__(self,adres,header='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',sure=0,yonlendirme=False):
        self.Adres=adres
        self.sure=sure
        self.yonlendirme=yonlendirme
        self.Baslik = {
            'User-Agent': header,
            'Host': adres.split("/")[2],
            'Referer': adres.split("/")[0]+"//"+adres.split("/")[2]
        }    

    def HTML(self):
        try:
            if self.sure:
                yanit = requests.get(self.Adres, headers=self.Baslik,allow_redirects=self.yonlendirme,timeout=self.sure)
            else:
                yanit = requests.get(self.Adres, headers=self.Baslik,allow_redirects=self.yonlendirme)
            if yanit.status_code==200:
                cevap=BeautifulSoup(yanit.text, 'html.parser')
                return cevap
            else:
                return yanit.status_code
        except:
            print(self.Adres,"adresinden veri çekilemedi.")
            return False
        
class Getir(object):
    def __init__(self,Html,Par):
        self.veri=Html
        if not type(Par)==list: Par=[Par]
        self.parametre=Par

    def Metin(self,veri,Parametre):
        i=-1
        cevap=None
        for par in Parametre:
            i+=1
            if par.Konteyner:
                if not type(par.Konteyner)==list: par.Konteyner=[par.Konteyner]
                veri=self.Metin(veri,par.Konteyner)
            try:
                if par.sira>0:
                    cevap=str(list(Getir(veri,[par]))[par.sira])
                elif not par.Val=="": 
                    cevap=veri.find(par.Tag,{par.Atr:par.Val})
                elif  not par.Atr=="": 
                    cevap=veri.find(par.Tag)[par.Atr]
                else: 
                    cevap=veri.find(par.Tag)
                if not cevap==None:break   
            except:
                pass
        if type(cevap)==list:
            cevap=" ".join(cevap)
        try:
            (bolen,kacinci)=Parametre[i].Ayrac1
            if not bolen==0:
                #if type(cevap)==element.Tag: cevap=cevap.get_text()
                cevap=str(cevap).split(bolen)[kacinci]     
        except:
            print("Ayrac1 (",bolen,kacinci,") bölümleme hatası")
        try:
            (bolen,kacinci)=Parametre[i].Ayrac2
            if not bolen==0:
                #if type(cevap)==element.Tag: cevap=cevap.get_text()
                cevap=str(cevap).split(bolen)[kacinci]
        except:
            print("Ayrac2 (",bolen,kacinci,") bölümleme hatası")
        return cevap 

    def __str__(self):
        cevap=self.Metin(self.veri,self.parametre)
        if type(cevap)==element.Tag: cevap=cevap.get_text()
        if cevap==None: return ""
        else: return cevap.strip()

    def Liste(self,veri,Parametre):
        cevap=[]
        for par in Parametre:
            if par.Konteyner:
                if not type(par.Konteyner)==list: par.Konteyner=[par.Konteyner]
                veri=self.Metin(self.veri,par.Konteyner)
                if not veri:continue
            try:
                if not par.Val=="": 
                    cevap=veri.find_all(par.Tag,attrs={par.Atr:par.Val})
                else: cevap=veri.find_all(par.Tag)
                if not cevap==None:break   
            except:
                pass
        return iter(cevap)  
        
    def __iter__(self):
        return self.Liste(self.veri,self.parametre)

class cekilecek(object):
    def __init__(self,tag,atr="",val="",ayrac1=(0,0),ayrac2=(0,0),sira=0,Konteyner=False):
        self.Tag=tag
        self.Atr=atr
        self.Val=val
        self.Ayrac1=ayrac1
        self.Ayrac2=ayrac2
        self.toplamUrun=0
        self.sayfaAdedi=0
        self.sira=sira
        self.Konteyner=Konteyner


class urunArama(object):
    def __init__(self,adres):
        self.Konteyner=False
        self.maxUrun=999999999
        self.adres=adres
        self.tumListe=[]
        self.sutunlar={}
        self.DUR=False
        
    def adresEki(self,aranacak,sorguEk='ara?q=',sayfaEk='sayfa=',filtreEk="puan=4-max&siralama=yorumsayisi"):
        arama=quote(aranacak)
        self.sorguEk=sorguEk+arama
        self.filtreEk=filtreEk
        self.sayfaEk=sayfaEk
        #self.Konteyner=""

    def anaSayfa(self,Unite,Total):
        Sayfa=Gezgin(self.adres+"/"+self.sorguEk+"&"+self.filtreEk)
        print(Sayfa.Adres)
        sonuc=Sayfa.HTML()
        #try:
        adet=str(Getir(sonuc,Total)).strip()
        if adet=="" or adet.isnumeric()==False:
            print("Ürün yok!")
            return False
        self.toplamUrun= int(adet.replace("'","").replace(".","").replace(",","").replace("+",""))
        print("Toplam", self.toplamUrun,"adet ürün bulundu.")
        if self.toplamUrun>self.maxUrun: 
            print("Fakat taranabilecek üst sınır:",self.maxUrun)
            self.toplamUrun=self.maxUrun
        Sayfa=Gezgin(self.adres+"/"+self.sorguEk+"&"+self.filtreEk)
        sonuc=Sayfa.HTML()
        sayfadakiUrun=len(list(Getir(sonuc,Unite)))
        if sayfadakiUrun<1:
            print("Aranan kritere göre ürün bulunamadı!")
            return False
        if self.toplamUrun%sayfadakiUrun>1:
            sayfaAdedi=self.toplamUrun//sayfadakiUrun+1
        else: sayfaAdedi=self.toplamUrun//sayfadakiUrun
        print("Her bir sayfada (maksimum)",sayfadakiUrun, "ürün olmak üzere, toplam ", sayfaAdedi,"sayfada taranacak.")
        self.sayfaAdedi=sayfaAdedi
        self.unite=Unite
        return True
        
    def sayfalardaGez(self,thr=999):
        if thr>self.sayfaAdedi: thr=self.sayfaAdedi
        print("İş parçacığı (threading ) sayısı=",thr)
        self.tumListe.clear
        thrA=[]
        i=0
        n1=dt.datetime.now()#işlem süresini hesaplatmak için kronometreyi başlattık
        for sayfa in range(1,self.sayfaAdedi+1):
            i+=1
            if self.DUR: break
            url=self.adres+"/"+self.sorguEk+"&"+self.filtreEk+"&"+self.sayfaEk+str(sayfa)
            ta=threading.Thread(target=self.cekAl, args = (url,))
            thrA.append(ta)
            ta.start()
            if i%thr==0:
                for tek in thrA:
                    tek.join()
                    thrA=[]
        for tek in thrA:
            tek.join()    
        n2=dt.datetime.now()#işlem bitiş süresini hesaplamak için kronometreyi durdur
        print(len(self.tumListe),"adet ürünün için çekme işlemi",(n2-n1).seconds,"saniyede tamamlandı.")
        return self.tumListe
        
    def cekAl(self,url):
        Sayfa=Gezgin(url)
        sonuc=Sayfa.HTML()
        if sonuc==429 or sonuc==301:
            if sonuc==429: print("site tarafından ip bloke edildi.")
            self.DUR=True
            return
        sayfadakiUrunler=list(Getir(sonuc,self.unite))
        for urun in sayfadakiUrunler:
            satir=[]
            for etiket,parametre in self.sutunlar.items():
                try:
                    ekle=str(Getir(urun,parametre))
                    satir.append(ekle)
                except:
                    satir.append("")#çekilemeyen veri
            self.tumListe.append(satir)
        
if __name__=="__main__":
    pass