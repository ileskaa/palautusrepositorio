class JoukkoMetodi:
    def __init__(self, joukko1, joukko2):
        self.lista1, self.lista2 = (joukko.to_int_list() for joukko in [joukko1, joukko2])

    def aja(self, avainsana):
        int_joukko = IntJoukko()

        if avainsana == "leikkaus":
            for i in range(0, len(self.lista1)):
                for j in range(0, len(self.lista2)):
                    if self.lista1[i] == self.lista2[j]:
                        int_joukko.lisaa(self.lista2[j])
        elif avainsana == "yhdiste":
            for lista in [self.lista1, self.lista2]:
                for indeksi in range(0, len(lista)):
                    alkio = lista[indeksi]
                    int_joukko.lisaa(alkio)
        elif avainsana == "erotus":
            for indeksi in range(0, len(self.lista1)):
                alkio = self.lista1[indeksi]
                int_joukko.lisaa(alkio)
            for indeksi in range(0, len(self.lista2)):
                alkio = self.lista2[indeksi]
                int_joukko.poista(alkio)

        return int_joukko


OLETUSKAPASITEETTI = 5
OLETUSKASVATUS = 5


class IntJoukko:
    # tämä metodi on ainoa tapa luoda listoja
    def _luo_lista(self, koko):
        return [0] * koko

    def __init__(self, kapasiteetti=None, kasvatuskoko=None):
        if kapasiteetti is None:
            self.kapasiteetti = OLETUSKAPASITEETTI
        elif isinstance(kapasiteetti, int) or kapasiteetti < 0:
            self.kapasiteetti = kapasiteetti
        else:
            raise Exception("Kapasiteetin tulee olla kokonaisluku")

        if kasvatuskoko is None:
            self.kasvatuskoko = OLETUSKASVATUS
        elif isinstance(kasvatuskoko, int) or kasvatuskoko < 0:
            self.kasvatuskoko = kasvatuskoko
        else:
            raise Exception("kasvatuskoon tulee olla kokonaisluku")

        self.lukujono = self._luo_lista(self.kapasiteetti)

        self.alkioiden_lkm = 0

    def kuuluu(self, luku):
        for alkio in self.lukujono:
            if luku == alkio:
                return True
        return False

    def lisaa_jonon_peraan(self, luku):
        self.lukujono[self.alkioiden_lkm] = luku
        self.alkioiden_lkm = self.alkioiden_lkm + 1

        jono_taynna = self.alkioiden_lkm % len(self.lukujono) == 0
        if jono_taynna:
            vanha_jono = self._luo_lista(self.alkioiden_lkm)
            self.kopioi_lista(self.lukujono, vanha_jono)
            self.lukujono = self._luo_lista(self.alkioiden_lkm + self.kasvatuskoko)
            self.kopioi_lista(vanha_jono, self.lukujono)

    def lisaa(self, luku):
        if not self.kuuluu(luku):
            self.lisaa_jonon_peraan(luku)

    def poista_alkio_listasta(self, poistettava_alkio):
        for alkion_indeksi in range(0, self.alkioiden_lkm):
            alkio = self.lukujono[alkion_indeksi]
            if poistettava_alkio == alkio:
                self.lukujono[alkion_indeksi] = 0
                return alkion_indeksi
        EI_MAARITELTY = -1
        return EI_MAARITELTY

    def siirra_seuraavat_alkiot_vasemmalle(self, poistetun_alkion_indeksi):
        viimeisen_alkion_indeksi = self.alkioiden_lkm - 1
        for j in range(poistetun_alkion_indeksi, viimeisen_alkion_indeksi):
            self.lukujono[j] = self.lukujono[j + 1]

        self.alkioiden_lkm = self.alkioiden_lkm - 1

    def poista(self, poistettava_alkio):
        poistetun_alkion_indeksi = self.poista_alkio_listasta(poistettava_alkio)

        alkio_poistettu = poistetun_alkion_indeksi != -1
        if alkio_poistettu:
            self.siirra_seuraavat_alkiot_vasemmalle(poistetun_alkion_indeksi)

    def kopioi_lista(self, lahde, kohde):
        for i in range(0, len(lahde)):
            kohde[i] = lahde[i]

    def mahtavuus(self):
        return self.alkioiden_lkm

    def to_int_list(self):
        lista = self._luo_lista(self.alkioiden_lkm)

        for i in range(0, len(lista)):
            lista[i] = self.lukujono[i]

        return lista

    @staticmethod
    def yhdiste(joukko1, joukko2):
        joukko_metodi = JoukkoMetodi(joukko1, joukko2)
        yhdistejoukko = joukko_metodi.aja("yhdiste")
        return yhdistejoukko

    # A static method knows nothing about the class or instance it was called on
    @staticmethod
    def leikkaus(joukko1, joukko2):
        joukko_metodi = JoukkoMetodi(joukko1, joukko2)
        leikkausjoukko = joukko_metodi.aja("leikkaus")
        return leikkausjoukko

    @staticmethod
    def erotus(joukko1, joukko2):
        joukko_metodi = JoukkoMetodi(joukko1, joukko2)
        erotusjoukko = joukko_metodi.aja("erotus")
        return erotusjoukko

    def __str__(self):
        if self.alkioiden_lkm == 0:
            return "{}"
        elif self.alkioiden_lkm == 1:
            ainut_alkio = self.lukujono[0]
            return "{" + str(ainut_alkio) + "}"
        else:
            tuloste = "{"
            for indeksi in range(0, self.alkioiden_lkm - 1):
                alkio = self.lukujono[indeksi]
                tuloste = tuloste + str(alkio)
                tuloste = tuloste + ", "
            viimeinen_alkio = self.lukujono[self.alkioiden_lkm - 1]
            tuloste = tuloste + str(viimeinen_alkio)
            tuloste = tuloste + "}"
            return tuloste
