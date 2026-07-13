<script>
import axios from 'axios'

export default {
  name: 'LoginView',
  data() {
    return {
      kupci: [],
      prodavci: [],
      admini: [],
      greska: '',
      UserNadjen: 0,
      forma: {
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
    async dohvatiKorisnike() {
      const responseKupci = await axios.get('http://127.0.0.1:5000/kupci')
      const responseProdavci = await axios.get('http://127.0.0.1:5000/prodavci')
      const responseAdmini = await axios.get('http://127.0.0.1:5000/admini')

      this.kupci = this.parseIfString(responseKupci.data.kupci)
      this.prodavci = this.parseIfString(responseProdavci.data.prodavci)
      this.admini = this.parseIfString(responseAdmini.data.admini)
    },
    login() {
      this.UserNadjen = 0
      const data = localStorage.getItem('user')
      if(data){
        this.greska = "Vec ste ulogovani, morate se izlogovati!"
        return
      }
      if (
        this.forma.username == '' ||
        this.forma.password == '' ||
        this.forma.vrstaKorisnika == ''
      ) {
        this.greska = 'Nisu uneti svi podaci'
        return
      }
      if (this.forma.username.length < 5) {
        this.greska = 'Username mora imati najmanje 5 karaktera'
        return
      }
      if (this.forma.vrstaKorisnika == 'kupac') {
        let kupac = null
        for (let i = 0; i < this.kupci.length; i++) {
          if (this.forma.username == this.kupci[i].Username) {
            kupac = this.kupci[i]
            this.UserNadjen = 1
            break
          }
        }
        if (this.UserNadjen == 0) {
          this.greska = 'Ne postoji kupac sa tim userom!'
          return
        }

        if (this.forma.password != kupac.Password) {
          this.greska = 'Netacan password!'
          return
        }

        localStorage.setItem('user', JSON.stringify(this.forma))
        this.$router.push('/')
      }
      if (this.forma.vrstaKorisnika == 'prodavac') {
        let prodavac = null
        for (let i = 0; i < this.prodavci.length; i++) {
          if (this.forma.username == this.prodavci[i].Username) {
            prodavac = this.prodavci[i]
            this.UserNadjen = 1
            break
          }
        }
        if (this.UserNadjen == 0) {
          this.greska = 'Ne postoji prodavac sa tim userom!'
          return
        }

        if (this.forma.password != prodavac.Password) {
          this.greska = 'Netacan password!'
          return
        }
        localStorage.setItem('user', JSON.stringify(this.forma))
        this.$router.push('/')
      }
      if (this.forma.vrstaKorisnika == 'administrator') {
        let admin = null
        for (let i = 0; i < this.prodavci.length; i++) {
          if (this.forma.username == this.admini[i].Username) {
            admin = this.admini[i]
            this.UserNadjen = 1
            break
          }
        }
        if (this.UserNadjen == 0) {
          this.greska = 'Ne postoji admin sa tim userom!'
          return
        }

        if (this.forma.password != admin.Password) {
          this.greska = 'Netacan password!'
          return
        }
        localStorage.setItem('user', JSON.stringify(this.forma))
        this.$router.push('/')
      }
    },
    otkazi() {
      this.$router.push('/')
    },
  },
  mounted() {
    this.dohvatiKorisnike()
  },
}
</script>

<template>
  <h1>Login</h1>
  <div class="forma">
    <span class="text-danger">{{ greska }}</span>
    <div class="col-md-3">
      Username:
      <input type="text" class="form-control" v-model="forma.username" />
    </div>
    <div class="col-md-3">
      Password:
      <input type="password" class="form-control" v-model="forma.password" />
    </div>
    <div class="col-md-3">
      Vrsta Korisnika:
      <select class="form-select" v-model="forma.vrstaKorisnika">
        <option value="kupac">Kupac</option>
        <option value="prodavac">Prodavac</option>
        <option value="administrator">Administrator</option>
      </select>
    </div>
    <button @click="login" class="btn btn-primary">Login</button>
    <button @click="otkazi" class="btn btn-danger">Cancel</button>
  </div>
</template>

<style scoped>
span {
  font-weight: 900;
}
button {
  margin: 1em 1em 0 0em;
}
</style>
