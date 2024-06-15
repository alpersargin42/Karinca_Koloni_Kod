'''
Alper SARGIN - 201312030 - Sezgisel Kodlama Ödevi
'''

import numpy as np

class KarincaKoloni:
    #Karınca koloni sınıfının yapıcı methodu-->(constructor)
    def __init__(self, mesafeler, karinca_sayisi, en_iyiler, iterasyon_sayisi, buharlasma, alfa=1, beta=1):
        self.mesafeler = mesafeler
        self.feromon = np.ones(self.mesafeler.shape) / len(mesafeler) # Feromon izlerini saklar. Başlangıçta tüm kenarlar üzerindeki feromon miktarını eşit olarak ayarlar (1 birim). Feromon matrisi, mesafeler matrisinin boyutlarıyla aynı şekle sahiptir ve her hücresinde başlangıç feromon miktarını içerir.
        self.tum_indisler = range(len(mesafeler))
        self.karinca_sayisi = karinca_sayisi
        self.en_iyiler = en_iyiler
        self.iterasyon_sayisi = iterasyon_sayisi
        self.buharlasma = buharlasma
        self.alfa = alfa
        self.beta = beta
    #Karınca Koloni Algoritmasını çalıştıran ana fonksiyondur. Bu fonksiyon, belirli bir iterasyon sayısı boyunca algoritmayı yürütür ve sonunda en kısa yolu bulur. 
    def calistir(self):
        en_kisa_yol = None
        tum_zamanlarin_en_kisa_yolu = ("gecici", np.inf)#Tüm iterasyonlar boyunca bulunan en kısa yolu ve bu yolun mesafesini saklar. Başlangıçta mesafe np.inf olarak ayarlanır, böylece ilk bulunan yol bu değerden daha kısa olacaktır.
        for i in range(self.iterasyon_sayisi): #iterasyon sayısı kadar iterasyon gerçekleştirir.
            tum_yollar = self.tum_yollari_olustur() # tum_yollari_olustur fonksiyonu çağrılarak, tüm karıncaların oluşturduğu yollar ve bu yolların mesafeleri hesaplanır.
            self.feromon_yay(tum_yollar, self.en_iyiler, en_kisa_yol=en_kisa_yol)#feromon_yay fonksiyonu çağrılarak, en iyi yolların üzerinden geçen karıncaların bıraktığı feromonlar güncellenir. Bu feromonlar, gelecekteki iterasyonlarda karar verme sürecini etkiler.
            en_kisa_yol = min(tum_yollar, key=lambda x: x[1]) #içindeki en kısa mesafeli yol bulunur ve en_kisa_yol değişkenine atanır.
            '''
            key=lambda x: x[1]: min fonksiyonuna verilen bu key parametresi, her bir elemanı karşılaştırırken hangi değeri kullanacağını belirtir. Burada, x her bir tuple'dır ve x[1] o yolun mesafesidir. 
            '''
            if en_kisa_yol[1] < tum_zamanlarin_en_kisa_yolu[1]:
                tum_zamanlarin_en_kisa_yolu = en_kisa_yol #Eğer bu iterasyonda bulunan en kısa yol, şimdiye kadar bulunan en kısa yoldan daha kısa ise, tum_zamanlarin_en_kisa_yolu bu yeni yolla güncellenir.
            self.feromon *= self.buharlasma #Feromon izleri, buharlama katsayısı ile çarpılarak zamanla azalır. Bu işlem, eski yolların etkisini azaltır ve yeni yolların keşfedilmesine olanak tanır.
        return tum_zamanlarin_en_kisa_yolu

    #feromon_yay fonksiyonu, belirli sayıda en iyi yolu kullanarak feromon izlerini günceller. Bu fonksiyon, karınca koloni algoritmasında önemli bir adımdır çünkü feromonlar, karıncaların sonraki iterasyonlarda hangi yolları tercih edeceğini etkiler. Feromon izleri artırılarak, daha iyi (daha kısa) yolların daha fazla tercih edilmesi sağlanır.
    def feromon_yay(self, tum_yollar, en_iyiler, en_kisa_yol):
        sirali_yollar = sorted(tum_yollar, key=lambda x: x[1]) #tum_yollar listesindeki yolları, mesafelerine göre artan şekilde sıralar. key=lambda x: x[1] ifadesi, her bir yolun mesafesini sıralama kriteri olarak kullanır. Sonuçta, sirali_yollar listesi mesafeye göre sıralanmış yolları içerir.
        for yol, mesafe in sirali_yollar[:en_iyiler]:
            for hareket in yol:
                self.feromon[hareket] += 1.0 / self.mesafeler[hareket]
        '''
        sirali_yollar[:en_iyiler] ifadesi, sıralanmış yollar listesinin en iyi en_iyiler sayıda olan kısmını alır.
        İç içe döngüde, yol üzerindeki her bir hareket (kenar) için:
        self.feromon[hareket] += 1.0 / self.mesafeler[hareket]: Bu ifade, feromon miktarını günceller. Feromonun artırılma miktarı, mesafenin tersiyle orantılıdır. Böylece, daha kısa mesafeler daha fazla feromon alır.
        '''

    #Bu fonksiyon, verilen bir yolun (düğümler arasındaki hareketlerin) toplam mesafesini hesaplar. Yol, bir dizi düğüm çiftinden oluşur ve her çift, iki düğüm arasındaki mesafeyi temsil eder.
    def yol_mesafesini_hesapla(self, yol):
        toplam_mesafe = 0 #Bu değişken, yol üzerindeki tüm hareketlerin mesafelerinin toplamını saklamak için kullanılır. Default = 0
        for eleman in yol:
            toplam_mesafe += self.mesafeler[eleman]
        '''
        self.mesafeler[eleman]: self.mesafeler matrisi, düğümler arasındaki mesafeleri içerir. eleman (bir düğüm çifti), bu matristeki bir indeksi temsil eder ve bu indekse karşılık gelen mesafe alınır.
        toplam_mesafe += self.mesafeler[eleman]: Bu mesafe, toplam_mesafe değişkenine eklenir.
        '''
        return toplam_mesafe

    #tum_yollari_olustur fonksiyonu, belirli sayıda karınca için yollar oluşturur ve bu yolların toplam mesafelerini hesaplar. Sonuçta, her bir yol ve o yolun toplam mesafesini içeren bir liste döndürür.
    def tum_yollari_olustur(self):
        tum_yollar = []
        for i in range(self.karinca_sayisi):
            yol = self.yol_olustur(0) #yol_olustur fonksiyonunu çağırarak başlangıç düğümünden (0) bir yol oluşturur. yol_olustur fonksiyonu, bir karıncanın izleyeceği düğümler arası yolu belirler.
            tum_yollar.append((yol, self.yol_mesafesini_hesapla(yol))) # oluşturulan yol ve bu yolun toplam mesafesi bir tuple olarak tum_yollar listesine eklenir.

            #self.yol_mesafesini_hesapla(yol): yol_mesafesini_hesapla fonksiyonu çağrılarak, oluşturulan yolun toplam mesafesi hesaplanır.
        return tum_yollar

    def yol_olustur(self, baslangic):
        yol = []
        ziyaret_edilenler = set() 
        ziyaret_edilenler.add(baslangic)
        onceki = baslangic
        '''
        ziyaret_edilenler: Karıncanın ziyaret ettiği düğümleri tutan bir küme. Başlangıç düğümü kümesine eklenir.
        onceki: Karıncanın şu anda bulunduğu düğüm. Başlangıçta bu düğüm, başlangıç düğümüdür.
        '''
        for i in range(len(self.mesafeler) - 1): #Tüm düğümleri ziyaret etmek için döngü. len(self.mesafeler) - 1 ifadesi, başlangıç düğümüne dönmeden önce tüm diğer düğümleri ziyaret etmeyi sağlar.
            hareket = self.hareket_sec(self.feromon[onceki], self.mesafeler[onceki], ziyaret_edilenler) #Mevcut düğümden bir sonraki düğüme olan hareket belirlenir. Bu fonksiyon, feromon seviyeleri ve mesafeleri dikkate alarak karıncanın hangi düğüme gideceğini belirler.
            yol.append((onceki, hareket)) #Mevcut düğümden (onceki) seçilen düğüme (hareket) olan hareket, yol listesine eklenir.
            onceki = hareket #Seçilen düğüm, bir sonraki adım için mevcut düğüm olur.
            ziyaret_edilenler.add(hareket) # Seçilen düğüm, ziyaret edilenler kümesine eklenir.
        yol.append((onceki, baslangic))  # Döngü tamamlandığında, karınca başlangıç düğümüne geri döner. Bu hareket de yol listesine eklenir.
        return yol

    #Bu fonksiyon, karıncanın mevcut düğümden bir sonraki düğüme hareketini seçer. Seçim süreci, feromon izleri ve mesafeler kullanılarak yapılır ve karıncanın daha önce ziyaret etmediği düğümler dikkate alınır.
    def hareket_sec(self, feromon, mesafe, ziyaret_edilenler):
        feromon = np.copy(feromon) #Feromon matrisinin kopyasını oluşturur. Bu, orijinal feromon matrisini değiştirmemek için yapılır.
        feromon[list(ziyaret_edilenler)] = 0 #Ziyaret edilen düğümler için feromon değerlerini sıfırlar. Böylece karınca, zaten ziyaret ettiği düğümlere geri dönmez.

        satir = feromon ** self.alfa * ((1.0 / mesafe) ** self.beta) #Feromon değerleri alfa kuvvetine yükseltilir. Bu, feromonun etkisini kontrol eder.Mesafelerin tersleri beta kuvvetine yükseltilir. Bu, mesafenin etkisini kontrol eder.

        norm_satir = satir / satir.sum() #Hareket olasılıklarını normalleştirir. Böylece olasılıkların toplamı 1 olur ve geçerli bir olasılık dağılımı elde edilir.
        hareket = np_choice(self.tum_indisler, 1, p=norm_satir)[0] #Normalleştirilmiş olasılık dağılımına göre bir sonraki düğümü olasılıksal olarak seçer.
        return hareket  #Seçilen düğüm (bir sonraki hareket) döndürülür.

def np_choice(a, size, p):
    return np.random.choice(a, size, p=p)  #np_choice fonksiyonu, np.random.choice fonksiyonuna benzer şekilde çalışır, ancak p parametresi ile belirtilen olasılık dağılımını dikkate alır. Bu dağılıma göre, örnekler çekilir ve dönüş değeri olarak verilir.

if __name__ == "__main__":
    mesafeler = np.array([[np.inf, 2, 2, 5, 7],
                          [2, np.inf, 4, 8, 2],
                          [2, 4, np.inf, 1, 3],
                          [5, 8, 1, np.inf, 2],
                          [7, 2, 3, 2, np.inf]])

    karinca_koloni = KarincaKoloni(mesafeler, 3, 1, 100, 0.95, alfa=1, beta=2)
    '''
    mesafeler: Çözüm alanındaki noktalar arasındaki mesafeleri içeren mesafe matrisi.
    karinca_sayisi: Karınca kolonisindeki karınca sayısı.
    en_iyiler: Her iterasyonda en iyi yolu seçmek için kullanılacak karıncaların sayısı.
    iterasyon_sayisi: Algoritmanın çalışacağı iterasyon sayısı.
    buharlasma: Feromonların buharlaşma oranı.
    alfa: Feromon etkisinin gücünü belirleyen parametre.
    beta: Mesafe etkisinin gücünü belirleyen parametre.
    '''

    en_kisa_yol = karinca_koloni.calistir()
    print("En kısa yol: {}".format(en_kisa_yol))
