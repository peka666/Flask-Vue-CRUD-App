<script>
import axios from 'axios'

export default {
  name: 'AllUsersView',
  data() {
    return {
      user: null,
      korisnici: [],
      greska: '',
    }
  },
  methods: {
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    proveriAdmina() {
      const data = localStorage.getItem('user')
      if (data) {
        this.user = JSON.parse(data)
      }
      if (this.user.vrstaKorisnika !== 'administrator') {
        this.$router.push('/')
      }
    },
    async dohvatiUsere(){
      const response = await axios.get('http://127.0.0.1:5000/admin/users')
      this.korisnici = this.parseIfString(response.data.korisnici)
    },
    async obrisi(korisnik){
      if(korisnik.VrstaKorisnika_ID==3){
        this.greska = "Ne mozete obrisati admina!"
        return
      }
      await axios.delete(`http://127.0.0.1:5000/admin/users/delete/${korisnik.ID}`)
      await this.dohvatiUsere()
    },
    izmeni(id){
      this.$router.push(`/admin/users/update/${id}`)
    }
  },
  mounted() {
    this.proveriAdmina()
    this.dohvatiUsere()
  },
}
</script>

<template>
  <div class="container">
    <h1>Svi korisnici</h1>
    <span class = 'text-danger'>{{greska}}</span>
    <table class = 'table'>
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Password</th>
          <th>Email</th>
          <th>Godina Rodjenja</th>
          <th>Stanje Novca</th>
          <th>Korisnik</th>
          <th>Opcije</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for = 'korisnik in korisnici' :key = 'korisnik.ID'>
          <th>{{korisnik.ID}}</th>
          <th>{{korisnik.Username}}</th>
          <th>{{korisnik.Password}}</th>
          <th>{{korisnik.Email}}</th>
          <th>{{korisnik.GodinaRodjenja}}.</th>
          <th>{{korisnik.TrenutnoStanjeNovca}} RSD</th>
          <th style="color: blue" v-if = 'korisnik.VrstaKorisnika_ID == 1'>
            Kupac
          </th>
          <th style="color: green" v-if = 'korisnik.VrstaKorisnika_ID == 2'>
            Prodavac
          </th>
          <th style = 'color: red' v-if = 'korisnik.VrstaKorisnika_ID == 3'>
            Admin
          </th>
          <th>
            <button @click = 'obrisi(korisnik)' class = 'btn btn-danger'>Obrisi</button>
          </th>
          <th>
            <button @click = 'izmeni(korisnik.ID)' class = 'btn btn-primary'>Izmeni</button>
          </th>
        </tr>
      </tbody>
    </table>
  </div>

</template>

<style scoped>
  span{
    font-weight: 900;
  }
</style>
