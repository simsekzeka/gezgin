# gezgin
Ürün listesi şeklinde içerik bulunduran sitelerden veri çekmek için kullanılan web kazıma modülüdür.
### Harici requests, BeautifulSoup ve Pandas kütüphnalerinin kurulması gereklidir:
- pip install requests
- pip install bs4
- pip install pandas

### gezgin. py içerisinde 4 adet sınıf bulunur:
- **Gezgin:** Web sayfalarından html kodlarını çekmek için kullanılır. Bağlanılacak **adres**, istekle birlikte gönderilecek **header**, yanıt için beklenilecek maksimum **sure** ve istek gönderilen sayfada ** yonlendirme **  (301)  olması durumunda devam edilip edilmeyeceği parametrelerini alır. **HTML** metoduyla web sitesinden gelen cevabı BeautifulSoup ile html.parse edilmiş olarak göndürür. 
> #En basit kullanımı:
> 
> Sayfa=Gezgin("https://github.com/simsekzeka/gezgin")
> 
> sonuc=Sayfa.HTML() 

Varsayılan olarak  geçerli olan değerler
**header**> *'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0'* 

**sure**> sonsuz

**yonlendirme**> kapalı

Örneğin, cep telefonundan giriş yapmış gibi, yönlendirmeye açık  ve maksimum bekleme süresi 5 sn olan bir istek için şöyle bir tanımlama yapılabilir: 
> Sayfa=Gezgin("https://github.com/simsekzeka/gezgin",header="Mozilla/5.0 (Linux; Android 4.2.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36",sure=5,yonlendirme=True)
-   **Getir:** Html kodları arasında istenen kısmın alınmasını sağlar.  Parametre olarak Gezginden gelen html verisini ve veri içerisinden alınacak kısma ait kriterleri belirten **cekilecek** türündeki nesneyi alır. Geriye, str ve list olmak üzere iki farklı tür veri döndürebilir. Sayfa içerisinde parametrede girilen kriterlere sahip birden fazla içerik varsa sonucu liste olarak alınmak istenebilir yada tek bir içeriğe erişmek içi metin olarak alınabilir. Bu dönüşler için özel metodlar tanımlanmamıştır, __ iter __   ve   __ str __ ile dönüş sağlanır.
-Örneğin:
>adet=str(Getir(sonuc,parametre)) # string türündeki cevap **str**(Getir(...)) ile alınmıştır.
>
>uniteler=list(Getir(sonuc,parametre)) # list türündeki cevap **list**(Getir(...))  ile alınmıştır.
- **cekilecek:** Html kodları arasından çekilecek olan verinin kriterlerini oluşturan, metod içermeyen bir sınıftır. 
>parametre1=cekilecek("span","class","totalCount") #*span* tag'ine sahip, *class* attribute'unun değeri *totalCount* olan veri çekilir.
>parametre2=cekilecek("a","href") #a tag'inin href attribute'na ait değeri (linki) çeker.
>parametre3=cekilecek("a") #a tag'ine ait veri çekilir: <a ..(tag içerisindeki attribute ve değerlere bakmaksızın)..> burada yer alan **tüm** içerik çekilecektir. </a>
>
**Ayrac1, Ayrac2, sira ve Konteyner opsiyonel parametreler içerir.**

**Ayraçlar**, basit bir split işlemini gerçekleştirir. Örn. span tag'i içerisindeki title attribute'na ait çekilen değerin "....With:90%...." kısmındaki "90" değerine ulaşmak için: 
>parametre5=cekilecek("span","title",Ayrac1=("width:",1),Ayrac2=("%",0))

**sira**, aynı kritere sahip birden fazla sonuç varsa sira parametresinde verilen değer**inci** sonucu döndürür. Örn. çekilen sayfadaki 4. linki almak için 
>parametre4=cekilecek("a",sira=3)

**Konteyner**, html kodlarında benzer içerik bulunması durumunda belirli bir bölgeyi işleme almak için kullanılır.
>parametre5=cekilecek("a","href",Konteyner=parametre1) # sayfa içeriğinde çok fazla link bulunacağından, veri çekme işlemi sayfanın tamamında değil, Konteyner parametresi ile belirtilen çerçeve içerisinde gerçekleştirilecektir. 

Konteyner parametresi de yine **cekilecek** türünden bir nesnedir.
- **urunArama:** Yukarıda anlatılan sınıf ve metodları kullanarak **ürün listesi içeren sayfalardan** standart verilerin çekilerek işlenmesini sağlayan sınıftır.

# Ürün arama işlem basamakları
- **Nesne oluşturma**: parametre olarak anasayfa adresi verilir: 
- 
>aramaMotoru=urunArama("http://www.likitders.com")
>
- **Adres eklerinin tanımlanması**: Sitelerde gezerken URL'deki değişimi takip ederseniz belli bir formatı olduğunu anlarsınız. Ürün arama sitelerindeki standart format şu şekildedir: Adresten sonra gelen sorgu eki örn.'ara?q=' bunun ardından gelen ifade site içinde aranan anahtar kelimedir. Varsa kullanılan filitre ve/veya siralama ölçütü "puan=4-max&siralama=yorumsayisi" gibi. Son olarak da sayfaların ilerlemesini sağlayacak sayfa numarası eki "page=" gibi... Bu ekler önceden tespit edilip sınıfa ait metod olan adresEki'ne parametre olarak girilmelidir. Ve tabi **aranacak** anahtar kelime de...

>aramaMotoru.adresEki(aranacak="kitap",sorguEk='ara?q=',sayfaEk='sayfa=',filtreEk="puan=4-max&siralama=yorumsayisi")

-Ürün listelemeyle ilgili sayısal bir takım sınırlar bulunur: 1-Toplam ürün sayısı 2-Bir sayfada görüntülenen ürün sayısı 3-Toplam bulunan ürün sayısının çok fazla olması durumunda sayfaları ilerleterek ulaşılabilecek maksimum ürün sayısı (sınır).

1- Toplam ürün sayısını, sayfa içeriğinde bulunduğu konumdan almak için cekilecek nesnesi tanımlanmalıdır.

>toplamUrunSayisi=cekilecek("span","class","totalCount")

2-Sayfadaki ürün sayısını çekmek için her bir ürün verisinin içinde bulunduğu tag önceden tespit edilmelidir. 

>sayfadakiUrunler=cekilecek("div","class","p-card-wrppr")

3- Ürün üst sınırı varsa nesnenin maxUrun özelliğine değer olarak girilmelidir.

>aramaMotoru.maxUrun=1200

-**Anasayfa taraması**, sayfalar arası tarama işlemini başlatabilmek için bulunan ürünlerle ilgili sayısal bilgilerin alınıp sayfa hesabı yapılması gerekmektedir. Aynı zamanda bu aşamada taramanın başlayabilmesi için herşey yolunda mı sorgusu yapılmış olacaktır.

>sonuc=self.ty.anaSayfa(sayfadakiUrunler,toplamUrunSayisi)

Şayet dönen **sonuc** False ise işlem başarısız demektir.

-True değeri dönerse herşey yolunda demektir. Ürün bazında çekilecek (işin sonunda excel tablosuna aktarılacak) verilerin sütun başlıklarıyla birlikte tanımlanması gerekir.

-Ve artık **sayfalardaGez**meye başlayabiliriz!...

>listemiz=self.ty.sayfalardaGez(20) #sonuç list türünden veri olarak göndürülür.

Parametre olarak girilen 20 değeri, threading (eş zamanlı çalışacak iş parçacığı) sayısını ifade eder. Boş bırakılırsa taranacak sayfa kadar fazla threading oluşturulacaktır.
