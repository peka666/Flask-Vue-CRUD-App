<script>
import axios from 'axios'

export default {
  name: 'HomeView',
  data() {
    return {
      proizvodi: [],
      korisnik: {
        username: '',
        password: '',
        vrstaKorisnika: '',
      },
    }
  },
  methods: {
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    dohvatiUsera() {
      const data = localStorage.getItem('user')
      if (data) {
        this.korisnik = JSON.parse(data)
      }
    },
    async dohvatiProizvode() {
      const response = await axios('http://127.0.0.1:5000/products')
      this.proizvodi = this.parseIfString(response.data.proizvodi)
    },
    vidiProizvode() {
      this.$router.push('/products')
    },
    uplati() {
      this.$router.push('/uplataNaRacun')
    },
    dodaj() {
      this.$router.push('/products/add')
    },
    sviUseri() {
      this.$router.push('/admin/users')
    },
    dodajAdmina() {
      this.$router.push("/add/admin")
    },
    prodavacProizvodi(username){
      this.$router.push(`/products/user/${username}`)
    },
    login(){
      this.$router.push(`/login`)
    },
    register(){
      this.$router.push(`/register`)
    },
  },
  mounted() {
    this.dohvatiUsera()
    this.dohvatiProizvode()
  },
}
</script>

<template>
  <div class="container">
    <h1>Zdravo {{ this.korisnik.username }}</h1>
    <div v-if="!korisnik.username || !korisnik.vrstaKorisnika">
      <button @click = 'login' class = 'btn btn-primary'>Login</button>
      <button @click = 'register' class = 'btn btn-info'>Register</button>
    </div>
    <div v-if="korisnik.vrstaKorisnika === 'kupac'">
      <button @click="vidiProizvode" class="btn btn-primary">Vidi sve proizvode</button>
    </div>
    <div v-if="korisnik.vrstaKorisnika === 'prodavac'">
      <button @click="prodavacProizvodi(korisnik.username)" class="btn btn-primary">Vidi svoje proizvode</button>
      <button @click="dodaj" class="btn btn-danger">Dodaj Proizvod</button>
    </div>
    <div v-if="korisnik.vrstaKorisnika === 'administrator'">
      <button @click="sviUseri" class="btn btn-primary">Svi korisnici</button>
      <button @click="vidiProizvode" class="btn btn-danger">Svi proizvodi</button>
      <button @click="dodajAdmina" class="btn btn-success">Dodaj Admina</button>
    </div>
  </div>
</template>

<style scoped>
button {
  margin: 1em 1em 0 0;
  width: 250px;
  height: 50px;
}
</style>
