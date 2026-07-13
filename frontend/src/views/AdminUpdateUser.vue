<script>
import axios from 'axios'

export default {
  name: 'AdminUpdateUser',
  props: ['id'],
  data() {
    return {
      admin: null,
      Password: '',
      korisnici: [],
      user: {
        ID: '',
        Username: '',
        Password: '',
        Email: '',
        GodinaRodjenja: '',
        ProfilnaSlika: '',
        TrenutnoStanjeNovca: '',
      },
      greska: '',
    }
  },
  methods: {
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    async dohvatiUsera() {
      const response = await axios.get(`http://127.0.0.1:5000/korisnici`)
      this.korisnici = this.parseIfString(response.data.korisnici)
      this.user = this.korisnici.find((k)=>k.ID === Number(this.id))
      console.log(response.data.korisnici)
      this.Password = this.user.Password
      this.user.GodinaRodjenja = Number(this.user.GodinaRodjenja)
      this.user.TrenutnoStanjeNovca = parseFloat(this.user.TrenutnoStanjeNovca)
      console.log(this.user.TrenutnoStanjeNovca)
    },
    otkazi(){
      this.$router.push('/admin/users')
    },
    async izmeni(id){
      if (
        this.user.Username === '' ||
        this.user.Password === '' ||
        this.Password === '' ||
        this.user.Email === '' ||
        this.user.GodinaRodjenja === '' ||
        this.user.TrenutnoStanjeNovca === ''
      ) {
        this.greska = 'Svi podaci moraju biti popunjeni!'
        return
      }
      if (this.user.Password.length < 5) {
        this.greska = 'Sifra mora imati makar 5 karaktera!'
        return
      }
      if (this.user.Password !== this.Password) {
        this.greska = 'Sifre se ne poklapaju!'
        return
      }
      if (this.user.Email.length < 10 || !this.user.Email.includes('@')) {
        this.greska = 'Email mora imati makar 10 karaktera i @ znak'
        return
      }
      if (this.user.GodinaRodjenja < 1900 || this.user.GodinaRodjenja > 2026) {
        this.greska = 'Godina rodjenja mora biti izmedju 1900 i 2026!'
        return
      }
      const korisnikData = {
        username: this.user.Username,
        password: this.user.Password,
        email: this.user.Email,
        godinaRodjenja: parseInt(this.user.GodinaRodjenja),
        profilnaSlika: this.user.ProfilnaSlika || "",
        trenutnoStanjeNovca: parseFloat(this.user.TrenutnoStanjeNovca) || 0.0,
      }
      try {
        const response = await fetch(`http://localhost:5000/admin/users/update/${id}`,{
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(korisnikData),
        })

        const rez = await response.json()
        if (rez.success) {
          alert('Uspesno!')
          this.$router.push('/admin/users')
        } else {
          this.greska = rez.error
        }
      } catch (error) {
        this.greska = 'Server error'
      }
    }
  },
  mounted(){
    this.dohvatiUsera()
  },
}
</script>

<template>
  <div class="container">
    <h1>Update user</h1>
    <div class="profilePicture">
      <img :src="'/' + user.ProfilnaSlika" style="width: 150px; height: 150px" alt="Bez Slike" />
    </div>
    <div class="forma">
      <span class="text-danger">{{ greska }}</span>
      <div class="col-md-3">
        Username
        <input type="text" class="form-control" v-model="user.Username" readonly />
      </div>
      <div class="col-md-3">
        Password
        <input type="password" class="form-control" v-model="user.Password" />
      </div>
      <div class="col-md-3">
        Potvrda Passworda
        <input type="password" class="form-control" v-model="Password" />
      </div>
      <div class="col-md-3">
        Email
        <input type="text" class="form-control" v-model="user.Email" />
      </div>
      <div class="col-md-3">
        Godina Rodjenja
        <input type="text" class="form-control" v-model="user.GodinaRodjenja" />
      </div>
      <div class="col-md-3">
        Profilna
        <select class="form-select" v-model="user.ProfilnaSlika">
          <option value="">Bez slike</option>
          <option value="pictures/slika1.avif">Slika 1</option>
          <option value="pictures/slika2.avif">Slika 2</option>
          <option value="pictures/slika3.avif">Slika 3</option>
        </select>
      </div>
      <div class="col-md-3">
        Stanje na Racunu
        <input type="text" class="form-control" v-model="user.TrenutnoStanjeNovca" />
      </div>
      <button @click="izmeni(user.ID)" class="btn btn-primary">Izmeni</button>
      <button @click="otkazi" class="btn btn-danger">Otkazi</button>
    </div>
  </div>
</template>

<style scoped>
span {
  font-weight: 900;
}
button {
  margin: 1em 1em 0 0;
}
</style>
