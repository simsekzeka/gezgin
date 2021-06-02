# gezgin
Alışveriş sitesi formundaki web sitelerinden veri kazıma modülüdür.
### Harici requests, BeautifulSoup ve Pandas kütüphnalerinin kurulması gereklidir:
- pip install requests
- pip install bs4
- pip install pandas

### gezgin. py içerisinde 4 adet sınıf bulunur:
- **Gezgin:** Web sayfalarından html kodlarını çekmek için kullanılır. Bağlanılacak **adres**, istekle birlikte gönderilecek **header**, yanıt için beklenilecek maksimum **sure** ve istek gönderilen sayfada ** yonlendirme **  (301)  olması durumunda devam edilip edilmeyeceği parametrelerini alır. **HTML** metoduyla web sitesinden gelen cevabı BeautifulSoup ile html.parse edilmiş olarak göndürür. 
> #En basit kullanımı:
> Sayfa=Gezgin("https://github.com/simsekzeka/gezgin")
> sonuc=Sayfa.HTML() 

Varsayılan olarak  geçerli olan değerler
**header**> *'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0'* 
**sure**> sonsuz
**yonlendirme**> kapalı
Örneğin, cep telefonundan giriş yapmış gibi, yönlendirmeye açık  ve maksimum bekleme süresi 5 sn olan bir istek için şöyle bir tanımlama yapılabilir: 
> Sayfa=Gezgin("https://github.com/simsekzeka/gezgin",header="Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",sure=5,yonlendirme=True)
-   **Getir:** Html kodları arasında istenen kısmın alınmasını sağlar.  Parametre olarak Gezginden gelen html verisini ve veri içerisinden alınacak kısmı belirten **cekilecek** türündeki nesneyi alır. Geriye, str ve list olmak üzere iki farklı tür veri döndürür. Bu dönüşler için özel metodlar tanımlanmamıştır, __ iter __   ve   __ str __ ile dönüş sağlanır.
-Örneğin:
>adet=str(Getir(sonuc,parametre)) # string türündeki cevap **str**(Getir(...)) ile alınmıştır.
>uniteler=list(Getir(sonuc,parametre)) # list türündeki cevap **list**(Getir(...))  ile alınmıştır.
- **cekilecek:**Çekilecek verinin yapısını oluşturan, metod içermeyen sınıftır. 
>parametre=cekilecek("span","class","totalCount") #*span* tag'ine sahip, *class* attribute'unun değeri *totalCount* olan veri çekilecek
- **urunArama:**
