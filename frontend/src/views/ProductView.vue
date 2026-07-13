<script>
import axios from 'axios'
export default {
  name: 'ProductView',
  props: ['id'],
  data() {
    return {
      proizvodi: [],
      komentari: [],
      greska: '',
      NovaCena: 0,
      naslov: '',
      tekst: '',
      komentar: {
        naslov: '',
        tekst: '',
      },
      user: {
        username: '',
        password: '',
        vrstaKorisnika: '',
      },
      proizvod: {
        Id: '',
        Naziv: '',
        Opis: '',
        Cena: '',
        KolicinaNaStanju: '',
        Popust: '',
      },
    }
  },
  methods: {
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    async dohvatiProizvodPoId() {
      const response = await axios.get('http://127.0.0.1:5000/products')
      this.proizvodi = this.parseIfString(response.data.proizvodi)
      this.proizvod = this.proizvodi.find((p) => p.ID === Number(this.id))
    },
    async dohvatiKomentare() {
      const response = await axios.get(`http://127.0.0.1:5000/comments/${this.id}`)
      this.komentari = this.parseIfString(response.data.komentari)
    },
    izracunajNovuCenu() {
      this.NovaCena = this.proizvod.Cena * (100 - this.proizvod.Popust) * 0.01
    },
    vratiSe() {
      this.$router.push(`/`)
    },
    proveriUsera() {
      const data = localStorage.getItem('user')
      if (data) {
        this.user = JSON.parse(data)
      }

    },
    async obrisi(proizvod_ID, komentar_ID){
      await axios.delete(`http://127.0.0.1:5000/products/${proizvod_ID}/comment/delete/${komentar_ID}`)
      await this.dohvatiKomentare()
    },
    async dodaj(id) {
      this.greska = '';

      if (!this.komentar.naslov?.trim() || !this.komentar.tekst?.trim()) {
        this.greska = "Svi podaci komentara moraju biti popunjeni!";
        return;
      }

      if (this.komentar.naslov.trim().length < 4) {
        this.greska = "Naslov komentara mora imati makar 4 karaktera!";
        return;
      }

      if (this.komentar.tekst.trim().length < 5) {
        this.greska = "Komentar mora imati najmanje 5 karaktera!";
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/products/${id}/comment`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            naslov: this.komentar.naslov.trim(),
            tekst: this.komentar.tekst.trim(),
          }),
        });

        const rez = await response.json();

        if (response.ok && rez.success) {
          this.greska = '';
          this.$toast.success("Uspesno ste dodali komentar")
          alert(rez.message || 'Uspesno ste dodali komentar!');
          this.resetForm();
          this.$router.push('/');
        } else {
          this.greska = rez.error || 'Greska pri komenatrisanju!';
        }

      } catch (error) {
        console.error('Error:', error);
        this.greska = 'Doslo je do greske pri povezivanju sa serverom!';
      }
      await this.dohvatiKomentare()
      this.greska = ''
      this.komentar.naslov = ''
      this.komentar.tekst = ''
    }
  },
  async mounted() {
    await this.dohvatiProizvodPoId()
    await this.dohvatiKomentare()
    this.izracunajNovuCenu()
    this.proveriUsera()
  },
}
</script>

<template>
  <div class="container">
    <h1>Pregled proizvoda</h1>
    <div class="form" style="margin-bottom: 2em">
      <div class="col-md-3">
        Naziv proizvoda:
        <input type="text" class="form-control" v-model="proizvod.Naziv" style="font-weight: 500" readonly />
      </div>
      <div class="col-md-3">
        Opis:
        <textarea type="text-area" class="form-control" v-model="proizvod.Opis" style="font-weight: 500" readonly></textarea>
      </div>
      <div class="col-md-3">
        Regularna Cena:
        <input type="text" class="form-control" v-model="proizvod.Cena" style="font-weight: 500" readonly />
      </div>
      <div class="col-md-3">
        Popust:
        <input type="text" class="form-control" v-model="proizvod.Popust" style="font-weight: 500" readonly />
      </div>
      <div class = 'col-md-3'>
        Cena sa snizenjem:
        <input type="text" class="form-control" v-model="NovaCena" style="font-weight:500" readonly />
      </div>
      <div class="col-md-3">
        Dostupna Kolicina:
        <input type="text" class="form-control" v-model="proizvod.KolicinaNaStanju" style="font-weight: 500" readonly />
      </div>
      <div class="Komentari">
        <h1>Komentari:</h1>
        <table class="table">
          <thead>
            <tr>
              <th>Redni br.</th>
              <th>Naslov</th>
              <th>Tekst</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(komentar, index) in komentari" :key="komentar.ID">
              <th>{{ index + 1 }}</th>
              <th>{{ komentar.Naslov }}</th>
              <th>{{ komentar.Tekst }}</th>
              <th v-if="user.vrstaKorisnika === 'administrator' || user.vrstaKorisnika ==='prodavac'">
                <button @click="obrisi(proizvod.Id, komentar.ID)" class="btn btn-danger">Obrisi</button>
              </th>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="user.vrstaKorisnika === 'kupac'">
        <h2>Ostavite komentar:</h2>
        <div class="forma">
          <span class="text-danger">{{ greska }}</span>
          <div class="col-md-4">
            Naslov:
            <input type="text" class="form-control" v-model="komentar.naslov" />
          </div>
          <div class="col-md-4">
            Tekst:
            <textarea type="text-area" class="form-control" v-model="komentar.tekst"></textarea>
          </div>
          <button @click="dodaj(proizvod.ID)" class="btn btn-success">Dodaj Komentar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
button {
  margin: 1em 1em 1em 0;
}
span {
  font-weight: 900;
}
</style>
