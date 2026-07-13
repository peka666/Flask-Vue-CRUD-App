<script>
import axios from 'axios'
import { r } from 'vue-router/dist/devtools-EWN81iOl.mjs'

export default {
  name: 'ProfileView',
  props: ['id'],
  data() {
    return {
      idKorisnika: '',
      korisnici: [],
      kupovine: [],
      pseudoKorisnik: '',
      greska: '',
      potvrdasifre: '',
      user:{
       username: '',
       password: '',
       vrstaKorisnika: '',
      },
      korisnik: {
        username: '',
        password: '',
        email: '',
        godinaRodjenja: '',
        profilnaSlika: '',
        trenutnoStanjeNovca: 0,
        vrstaKorisnika: 0,
      },
    }
  },
  methods: {
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    async dohvatiID(username){
      const response = await axios.get(`http://127.0.0.1:5000/korisnici/${username}`)
      this.idKorisnika = this.parseIfString(response.data.korisnikID)
      console.log(this.idKorisnika)
    },
    async dohvatiKupovine(){
      const response = await axios.get(`http://127.0.0.1:5000/kupovine/${this.idKorisnika}`)
      this.kupovine = this.parseIfString(response.data.kupovine)
      console.log(this.idKorisnika)
    },
    async dohvatiSveKorisnike() {
      const response = await axios.get('http://127.0.0.1:5000/korisnici')
      this.korisnici = this.parseIfString(response.data.korisnici)
      const data = localStorage.getItem('user')
      if (data) {
        this.pseudoKorisnik = JSON.parse(data)
        this.user = JSON.parse(data)
      }
      else{
        this.$router.push('/login')
      }
      console.log(this.korisnici[0])
      for(let i = 0; i < this.korisnici.length; i++) {
        if(this.pseudoKorisnik.username == this.korisnici[i].Username) {
          this.korisnik.username = this.korisnici[i].Username
          this.korisnik.password = this.korisnici[i].Password
          this.korisnik.email = this.korisnici[i].Email
          this.korisnik.godinaRodjenja = this.korisnici[i].GodinaRodjenja
          this.korisnik.trenutnoStanjeNovca = this.korisnici[i].TrenutnoStanjeNovca
          this.korisnik.profilnaSlika = this.korisnici[i].ProfilnaSlika
          console.log(this.korisnik.profilnaSlika)
          if(this.korisnici[i].VrstaKorisnika_ID==1){
            this.korisnik.vrstaKorisnika = 'Kupac'
          }
          if(this.korisnici[i].VrstaKorisnika_ID==2){
            this.korisnik.vrstaKorisnika = 'Prodavac'
          }
          if(this.korisnici[i].VrstaKorisnika_ID==3){
            this.korisnik.vrstaKorisnika = 'Administrator'
          }
        }
      }
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    },
    izmeni(id){
      this.$router.push(`/profile/update/${id}`)
    }
  },
   async mounted() {
      await this.dohvatiSveKorisnike()
      await this.dohvatiID(this.user.username)
      await this.dohvatiKupovine()
  },
}
</script>

<template>
  <h1>Zdravo {{ korisnik.username }}</h1>
  <div v-if = 'korisnik.vrstaKorisnika!==""'>
    <h3 style="font-weight: 600">{{korisnik.vrstaKorisnika}}</h3>
  </div>
  <div class="profilePicture" style="margin-bottom: 1em">
    <img :src="korisnik.profilnaSlika" style="width: 150px; height: 150px;" alt="Ucitavanje">
  </div>
  <div class="forma">
    <span class="text-danger">{{ greska }}</span>
    <div class="col-md-3">
      Username:
      <input type="text" class="form-control" v-model="korisnik.username" readonly />
    </div>
    <div class="col-md-3">
      Email:
      <input type="text" class="form-control" v-model="korisnik.email" readonly />
    </div>
    <div class="col-md-3">
      Godina Rodjenja:
      <input type="text" class="form-control" v-model="korisnik.godinaRodjenja" readonly />
    </div>
    <div class="col-md-3">
      Korisnik:
      <input type="text" class="form-control" v-model="korisnik.vrstaKorisnika" readonly />
    </div>
    <div v-if='user.vrstaKorisnika==="kupac"||user.vrstaKorisnika==="prodavac"'>
      <div class="col-md-3">
        Stanje na racunu:
        <input type="number" v-model = 'korisnik.trenutnoStanjeNovca' class = 'form-control' readonly>
      </div>
    </div>
    <button @click="izmeni(idKorisnika)" class="btn btn-primary">Izmeni Profil</button>
    <button @click="logout" class="btn btn-danger">Logout</button>
    <table class = 'table'>
      <thead>
        <tr></tr>
      </thead>
    </table>
  </div>
  <div v-if = 'user.vrstaKorisnika==="kupac"'>
    <h1>Istorija kupovina:</h1>
    <table class = "table">
      <thead>
        <tr>
          <th>Datum</th>
          <th>Vrednost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for = 'kupovina in kupovine' :key = 'kupovina.ID'>
          <th>{{kupovina.DatumKupovine}}</th>
          <th>{{kupovina.UkupnaCena}}</th>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
button {
  margin: 1em 1em 0 0em;
}
</style>
