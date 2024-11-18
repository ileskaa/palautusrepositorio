import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 6
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 4)
            if tuote_id == 3:
                return Tuote(3, "olut", 8)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self):
        TILINUMERO = "12345"
        MAIDON_HINTA = 5
        viite = self.viitegeneraattori_mock.uusi()

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", TILINUMERO)

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            viite,
            TILINUMERO,
            self.kauppa._kaupan_tili,
            MAIDON_HINTA
        )

    def test_tilisiirto_toimii_kahdella_eri_tuotteella(self):
        TILINUMERO = "12345"
        MAIDON_HINTA = 5
        LEIVAN_HINTA = 4
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", TILINUMERO)

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            self.viitegeneraattori_mock.uusi(),
            TILINUMERO,
            self.kauppa._kaupan_tili,
            MAIDON_HINTA + LEIVAN_HINTA
        )

    def test_tilisiirto_toimii_kahdella_samalla_tuotteella(self):
        TILINUMERO = "12345"
        MAIDON_HINTA = 5
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", TILINUMERO)

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            self.viitegeneraattori_mock.uusi(),
            TILINUMERO,
            self.kauppa._kaupan_tili,
            MAIDON_HINTA * 2
        )

    def test_kauppa_ei_veloita_jos_tuote_loppu(self):
        TILINUMERO = "12345"
        MAIDON_HINTA = 5
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", TILINUMERO)

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            self.viitegeneraattori_mock.uusi(),
            TILINUMERO,
            self.kauppa._kaupan_tili,
            MAIDON_HINTA
        )

    def test_metodi_aloita_asiointi_nollaa_tiedot(self):
        TILINUMERO = "12345"
        LEIVAN_HINTA = 4

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            self.viitegeneraattori_mock.uusi(),
            TILINUMERO,
            self.kauppa._kaupan_tili,
            LEIVAN_HINTA
        )

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.viitegeneraattori_mock.uusi.assert_called()

    def test_kaupan_metodi_poista_korista_toimii(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("pekka", "12345")

        TILINUMERO = "12345"
        KORIN_HINTA = 0
        viite = self.viitegeneraattori_mock.uusi()

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka",
            viite,
            TILINUMERO,
            self.kauppa._kaupan_tili,
            KORIN_HINTA
        )
