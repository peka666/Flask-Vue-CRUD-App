<script>
import axios from 'axios'

export default {
  name: 'AddAdminView',
  data() {
    return {
      user: null,
      korisnici: [],
      greska: '',
      potvrdasifre: '',
      korisnik: {
        username: '',
        password: '',
        email: '',
        godinaRodjenja: '',
        profilnaSlika: '',
        trenutnoStanjeNovca: 0,
        vrstaKorisnika: '',
      },
    }
  },
  methods: {
    resetForm(){
      this.korisnik = {
        username: '',
        password: '',
        email: '',
        godinaRodjenja: '',
        profilnaSlika: '',
        vrstaKorisnika: '',
        trenutnoStanjeNovca: 0,
      };
      this.potvrdasifre = '';
    },
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    async dohvatiSveKorisnike() {
      const response = await axios.get('http://127.0.0.1:5000/korisnici')
      this.korisnici = this.parseIfString(response.data.korisnici)
      const data = localStorage.getItem('user')
      if (data){
        this.user = JSON.parse(data)
      }
      else{
        this.$router.push('/')
      }
    },
    async register() {
      this.korisnik.vrstaKorisnika = 'administrator'
      if (
        this.korisnik.username == '' ||
        this.korisnik.password == '' ||
        this.potvrdasifre == '' ||
        this.korisnik.email == '' ||
        this.korisnik.godinaRodjenja == '' ||
        this.korisnik.vrstaKorisnika == ''
      ) {
        this.greska = 'Svi podaci moraju biti popunjeni!'
        return
      }
      if (this.korisnik.username.length < 5) {
        this.greska = 'Username mora imati makar 5 karaktera!'
        return
      }
      for (let i = 0; i < this.korisnici.length; i++) {
        if (this.korisnik.username.toLowerCase() === this.korisnici[i].Username.toLowerCase()) {
          this.greska = 'Taj username vec postoji!'
          return
        }
      }
      if (this.korisnik.password.length < 5) {
        this.greska = 'Sifra mora imati makar 5 karaktera!'
        return
      }
      if (this.korisnik.email.length < 10 || !this.korisnik.email.includes('@')) {
        this.greska = 'Email mora imati makar 10 karaktera i @ znak'
        return
      }
      if (this.korisnik.godinaRodjenja < 1900 || this.korisnik.godinaRodjenja > 2026) {
        this.greska = 'Godina rodjenja mora biti izmedju 1900 i 2026!'
        return
      }
      if (this.korisnik.password != this.potvrdasifre) {
        this.greska = 'Sifre se ne poklapaju!'
        return
      }
      try {
        const korisnikData = {
          username: this.korisnik.username,
          password: this.korisnik.password,
          email: this.korisnik.email,
          profilnaSlika: this.korisnik.profilnaSlika || '',
          trenutnoStanjeNovca: this.korisnik.trenutnoStanjeNovca || 0.0,
          godinaRodjenja: this.korisnik.godinaRodjenja,
          vrstaKorisnika: 'administrator',
        }
        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(korisnikData),
        })

        const rez = await response.json();
        console.log('Server response:', rez);

        if (response.ok && rez.success) {
          this.greska = ''
          alert(rez.message || 'Uspesno ste se registrovali!')
          this.resetForm()
        } else {
          this.greska = rez.error || 'Doslo je do greske pri registraciji!'
        }
        this.$router.push('/')
      } catch (error) {
        console.error('Error:', error)
        this.greska = 'Doslo je do greske pri povezivanju sa serverom!'
        return
      }
    }
  },
  async mounted() {
    await this.dohvatiSveKorisnike()
  },
}
</script>

<template>
  <h1>Dodavanje admina</h1>
  <div class="profilePicture">
    <img :src="'/' + korisnik.profilnaSlika" style="width: 150px; height: 150px" />
  </div>
  <div class="forma">
    <span class="text-danger">{{ greska }}</span>
    <div class="col-md-3">
      Username:
      <input type="text" class="form-control" v-model="korisnik.username" />
    </div>
    <div class="col-md-3">
      Password:
      <input type="password" class="form-control" v-model="korisnik.password" />
    </div>
    <div class="col-md-3">
      Potvrdi password:
      <input type="password" class="form-control" v-model="potvrdasifre" />
    </div>
    <div class="col-md-3">
      Email:
      <input type="text" class="form-control" v-model="korisnik.email" />
    </div>
    <div class="col-md-3">
      Godina Rodjenja:
      <input type="text" class="form-control" v-model="korisnik.godinaRodjenja" />
    </div>
    <div class="col-md-3">
      Slika(Moze da se izmeni posle):
      <select class="form-select" v-model="korisnik.profilnaSlika">
        <option value="">Bez slike</option>
        <option value="pictures/slika1.avif">Slika 1</option>
        <option value="pictures/slika2.avif">Slika 2</option>
        <option value="pictures/slika3.avif">Slika 3</option>
      </select>
    </div>
    <button @click="register" class="btn btn-primary">Register</button>
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
