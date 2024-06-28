
import pygame
import random

pygame.init()
W, H = 750, 750

pencere = pygame.display.set_mode((W, H))

FPS = 30
saat = pygame.time.Clock()

# Sınıflar


class Oyun:
    def __init__(self, balikci, balik_grup):
        # Nesneler
        self.balikci = balikci
        self.balik_grup = balik_grup

        # Oyun degiskenleri
        self.sure = 0
        self.fps_degeri_sayma = 0
        self.bolum_no = 0

        # Baliklar ---> hedef
        balik1 = pygame.image.load("balik1.png")
        balik2 = pygame.image.load("balik2.png")
        balik3 = pygame.image.load("balik3.png")
        balik4 = pygame.image.load("balik4.png")
        self.balik_liste = [balik1, balik2, balik3, balik4]
        self.balik_liste_index_no = random.randint(0, 3)
        self.hedef_balik_goruntu = self.balik_liste[self.balik_liste_index_no]
        self.hedef_balik_konum = self.hedef_balik_goruntu.get_rect()
        self.hedef_balik_konum.top = 40  # üstten 40 bosluk
        self.hedef_balik_konum.centerx = W//2

        # Font
        self.oyun_fontu = pygame.font.Font("oyun_font.ttf", 40)
        # Oyun sarkisi ve ses efekti
        self.balik_tutma = pygame.mixer.Sound("yeme_efekt.wav")
        self.olme_sesi = pygame.mixer.Sound("olu.wav")
        pygame.mixer.music.load("sarki.wav")
        pygame.mixer.music.play(-1)  # hep bu calsin demek

        # Arka plan
        self.oyun_Arka_plan = pygame.image.load("arka_plan.jpg")
        self.oyun_bitti = pygame.image.load("oyun_sonu.jpg")

    def update(self):
        self.fps_degeri_sayma += 1
        if self.fps_degeri_sayma == FPS:
            self.sure += 1
            print(self.sure)
            self.fps_degeri_sayma = 0

        self.temas()

    def cizdir(self):

        metin1 = self.oyun_fontu.render("Süre: "+str(self.sure), True, (255, 255, 255), (0, 0, 170))
        metin1_konum = metin1.get_rect()
        metin1_konum.top = 30
        metin1_konum.left = 30

        metin2 = self.oyun_fontu.render("Can: "+str(self.balikci.can), True, (255, 255, 255), (0, 0, 170))
        metin2_konum = metin2.get_rect()
        metin2_konum.top = 30
        metin2_konum.right = W-50

        pencere.blit(self.oyun_Arka_plan, (0, 0))
        pencere.blit(metin1, metin1_konum)
        pencere.blit(metin2, metin2_konum)
        pencere.blit(self.hedef_balik_goruntu, self.hedef_balik_konum)

        # hedef balığı ve ekranın belirli kısmını dikdortgene alalım
        pygame.draw.rect(pencere, (255, 255, 255), (350, 30, 50, 50), 5)
        pygame.draw.rect(pencere, (255, 0, 255), (0, 100, 750, H - 150), 5)

    def temas(self):
        temas_oldu_mu = pygame.sprite.spritecollideany(self.balikci, self.balik_grup)
        if temas_oldu_mu:
            if temas_oldu_mu.tip == self.balik_liste_index_no:
                temas_oldu_mu.remove(self.balik_grup)  # temasli balik silindi
                self.balik_tutma.play()  # ses efekti
                if self.balik_grup:
                    self.hedef_yenile()  # yeni hedef
                else:
                    self.hedefle()

            else:  # yanlis balik tutuldu
                self.balikci.can -= 1
                self.olme_sesi.play()
                self.guvenli_Alan()

                if self.balikci.can <= 0:
                    self.durdur()

    def durdur(self):
        global durum
        pencere.blit(self.oyun_bitti, (0, 0))
        pygame.display.update()
        oyun_durdu = True
        while oyun_durdu:
            for etkinlik in pygame.event.get():
                if etkinlik.type == pygame.KEYDOWN:
                    if etkinlik.key == pygame.K_SPACE:
                        self.reset()
                        oyun_durdu = False

                if etkinlik.type == pygame.QUIT:  # gameoverda iken çarpıya tıklanınca kapatsın diye
                    oyun_durdu = False
                    durum = False

    def reset(self):
        self.balikci.can = 3
        self.bolum_no = 0
        self.hedefle()
        self.guvenli_Alan()

    def guvenli_Alan(self):
        self.balikci.rect.top = H - 40

    def hedef_yenile(self):
        # yeni hedef balik
        hedef_balik = random.choice(self.balik_grup.sprites())
        self.hedef_balik_goruntu = hedef_balik.image
        self.balik_liste_index_no = hedef_balik.tip

    def hedefle(self):  # balik kalmadiysa yeni bolume gec
        self.bolum_no += 1
        for balik in self.balik_grup:
            self.balik_grup.remove(balik)  # listeyi temizledi

        for x in range(self.bolum_no):
            self.balik_grup.add(Balik(random.randint(0, W-32), random.randint(105, H-150), self.balik_liste[0], 0))
            self.balik_grup.add(Balik(random.randint(0, W-32), random.randint(105, H-150), self.balik_liste[1], 1))
            self.balik_grup.add(Balik(random.randint(0, W-32), random.randint(105, H-150), self.balik_liste[2], 2))
            self.balik_grup.add(Balik(random.randint(0, W-32), random.randint(105, H-150), self.balik_liste[3], 3))


# pygame.sprite.Sprite, Pygame'in sprite (hareketli oyun nesnesi) sistemi için
# sağladığı bir sınıftır. Sprite sistemi, oyun nesnelerinin kolayca yönetilmesini,
# gruplandırılmasını ve işlenmesini sağlar.

class Balik(pygame.sprite.Sprite):
    def __init__(self, x, y, resim, tip):
        super().__init__()
        self.image = resim
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.tip = tip
        self.hiz = random.randint(1, 8)
        # balik kenara çarparsa ters yonden devam etsin
        self.yonx = random.choice([-1, 1])  # ikisinden birini secer
        self.yony = random.choice([-1, 1])

    def update(self):  # *args, **kwargs):
        self.rect.x += self.hiz * self.yonx
        self.rect.y += self.hiz * self.yony

        if self.rect.left <= 0 or self.rect.right >= W:
            self.yonx *= -1
        if self.rect.top <= 100 or self.rect.bottom >= H-50:
            self.yony *= -1


class Balikci(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("balikci.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.can = 3
        self.hiz = 10

    def update(self):
        self.hareket()

    def hareket(self):
        tus = pygame.key.get_pressed()
        if tus[pygame.K_LEFT]:
            self.rect.x -= self.hiz
        elif tus[pygame.K_RIGHT]:
            self.rect.x += self.hiz
        elif tus[pygame.K_UP]:
            self.rect.y -= self.hiz
        elif tus[pygame.K_DOWN]:
            self.rect.y += self.hiz


# Ana Karakter Grup İslemleri
balikci_grup = pygame.sprite.Group()
balikci = Balikci(W//2, H//2)
balikci_grup.add(balikci)

# Balik Grup
# balik1 = pygame.image.load("balik1.png")
balik_grup = pygame.sprite.Group()
# balik = Balik(random.randint(0,W-32), random.randint(0,H-32),balik1,0)
# balik_grup.add(balik)

# balik2 = pygame.image.load("balik2.png")
# balik = Balik(random.randint(0,W-32), random.randint(0,H-32),balik2,0)
# balik_grup.add(balik)

# Oyun sınıfı
oyun = Oyun(balikci, balik_grup)
oyun.hedefle()


# Oyun dongusu
durum = True
while durum:
    for etkinlik in pygame.event.get():  # var mi klavyede hareketlilik
        if etkinlik.type == pygame.QUIT:
            durum = False

    pencere.fill((0, 0, 0))  # her hareketten sonra safyayı siyaha boya ki düz cigi olmasin

    # Oyun mekanigi
    oyun.update()
    oyun.cizdir()

    # balikci cizdirme ve guncelleme
    balikci_grup.update()  # balik_grup içinde bulunan tüm sprite'ların update fonksiyonlarını çağırır.
    # balik_grup içindeki her Balik nesnesi, bu fonksiyon ile hareket eder ve durumu güncellenir.
    balikci_grup.draw(pencere)  # balikci_grup içindeki tüm sprite'ları pencere yüzeyine çizer.

    # Balik Test
    balik_grup.update()
    balik_grup.draw(pencere)

    pygame.display.update()  # ekrandaki tüm çizimlerin güncellenmesini sağlar.
    saat.tick(FPS)

pygame.quit()
