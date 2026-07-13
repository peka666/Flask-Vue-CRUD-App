<script>
import axios from 'axios'
import { w } from 'vue-router/dist/devtools-EWN81iOl.mjs'
export default {
  name: 'ProductsView',
  data() {
    return {
      proizvodi: [],
      ID: '',
      user: {
        username: '',
        password: '',
        vrstaKorisnika: '',
      },
      korpa: [],
    }
  },
  methods: {
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    async dohvatiKorpu() {
      const response = await axios.get(`http://127.0.0.1:5000/cart/${this.ID}`)
      this.korpa = this.parseIfString(response.data.korpa)
    },
    async dohvatiId(username) {
      const response = await axios.get(`http://127.0.0.1:5000/korisnici/${username}`)
      this.ID = this.parseIfString(response.data.korisnikID)
    },
    async dohvatiSveProizvode() {
      const response = await axios.get('http://127.0.0.1:5000/products')
      this.proizvodi = this.parseIfString(response.data.proizvodi)
    },
    izracunajCenu(cena, popust) {
      cena = cena * (100 - popust) * 0.01
      return cena
    },
    vidi(id) {
      this.$router.push(`/productView/${id}`)
    },
    izmeni(id) {
      this.$router.push(`/product/update/${id}`)
    },
    async dodajUKorpu(proizvodID, korisnikID) {
      try {
        const korpaData = {
          ProizvodID: proizvodID,
          Kolicina: 1,
          KorisnikID: korisnikID,
        }
        const response = await fetch('http://localhost:5000/cart/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(korpaData),
        })

        const rez = await response.json()
        console.log('Server response:', rez)
        await this.dohvatiKorpu()

        if (response.ok && rez.success) {
          this.greska = ''
          alert(rez.message || 'Uspesno ste dodali u korpu!')
          this.resetForm()
        } else {
          this.greska = rez.error || 'Doslo je do greske pri dodavanju u korpu!'
        }
        this.$router.push('/')
      } catch (error) {
        console.error('Error:', error)
        this.greska = 'Doslo je do greske pri povezivanju sa serverom!'
        return
      }
    },
    async kupi() {
      try {
        const response = await fetch('http://localhost:5000/checkout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.korpa),
        })
        const rez = await response.json()
        console.log('Server response:', rez)
        await this.dohvatiKorpu()
        this.$toast.success("Uspesna kupovina!")

        if (response.ok && rez.success) {
          this.greska = ''
          alert(rez.message || 'Uspesno ste dodali u korpu!')
          this.resetForm()
        } else {
          this.greska = rez.error || 'Doslo je do greske pri dodavanju u korpu!'
        }
        this.$router.push('/')
      } catch (error) {
        console.error('Error:', error)
        this.greska = 'Doslo je do greske pri povezivanju sa serverom!'
        return
      }
    },
    dohvatiUsera() {
      const data = localStorage.getItem('user')
      if (data) {
        this.user = JSON.parse(data)
      }
    },
    async obrisi(id) {
      await axios.delete(`http://127.0.0.1:5000/products/delete/${id}`)
      await this.dohvatiSveProizvode()
    },
    async ukloni(id){
      await axios.delete(`http://127.0.0.1:5000/cart/delete/${id}`)
      await this.dohvatiKorpu()
    }
  },
  async mounted() {
    await this.dohvatiSveProizvode()
    this.dohvatiUsera()
    await this.dohvatiId(this.user.username)
    await this.dohvatiKorpu()
  },
}
</script>

<template>
  <div class="container">
    <div v-if = 'user.vrstaKorisnika === "kupac"'>
      <h1>Vasa narudzbina:</h1>
      <table class="table">
        <thead>
          <tr>
            <th>Naziv</th>
            <th>Kolicina</th>
            <th>Opcija</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="proizvod in korpa" :key="proizvod.Proizvod_ID">
            <th>{{ proizvod.Naziv}}</th>
            <th>{{ proizvod.Kolicina }}</th>
            <th>
              <button @click = 'ukloni(proizvod.Proizvod_ID)' class = 'btn btn-danger'>Ukloni</button>
            </th>
          </tr>
        </tbody>
      </table>
      <div v-if="this.korpa.length !== 0">
        <button @click="kupi()" class="btn btn-success">Naruci</button>
      </div>
    </div>
    <h1>Svi proizvodi</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Redni br.</th>
          <th>Naziv</th>
          <th>Opis</th>
          <th>Regularna Cena</th>
          <th>Kolicina na stanju</th>
          <th>Popust</th>
          <th>Nova cena</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="proizvod in proizvodi" :key="proizvod.ID">
          <th>{{ proizvod.ID }}</th>
          <th>{{ proizvod.Naziv }}</th>
          <th>{{ proizvod.Opis }}</th>
          <th>{{ proizvod.Cena }}</th>
          <th>{{ proizvod.KolicinaNaStanju }}</th>
          <th>{{ proizvod.Popust }}%</th>
          <th>{{ izracunajCenu(proizvod.Cena, proizvod.Popust) }}</th>
          <th>
            <button @click="vidi(proizvod.ID)" class="btn btn-primary">Detaljnije</button>
          </th>
          <th v-if="user.vrstaKorisnika === 'kupac'">
            <button @click="dodajUKorpu(proizvod.ID, ID)" class="btn btn-info">
              Dodaj u korpu
            </button>
          </th>
          <th v-if="user.vrstaKorisnika === 'administrator'">
            <button @click="izmeni(proizvod.ID)" class="btn btn-success">Izmeni</button>
          </th>
          <th v-if="user.vrstaKorisnika === 'administrator'">
            <button @click="obrisi(proizvod.ID)" class="btn btn-danger">Obrisi</button>
          </th>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped></style>
