<script>
export default {
  name: 'ProductAddView',
  data() {
    return {
      user: {
        username: '',
        password: '',
        vrstaKorisnika: '',
      },
      greska: '',
      proizvod:{
        Naziv: '',
        Opis: '',
        Cena: 0,
        KolicinaNaStanju: 0,
        Popust: 0,
      }
    }
  },
  methods: {
    dohvatiUsera() {
      const data = localStorage.getItem('user')
      if (data) {
        this.user = JSON.parse(data)
      }
      if (this.user.vrstaKorisnika !== 'prodavac') {
        this.$router.push('/')
      }
    },
    otkazi(){
      this.$router.push('/')
    },
    async dodaj(){
      if(this.proizvod.Naziv === '' ||
        this.proizvod.Opis===''||
        this.proizvod.Cena===''||
        this.proizvod.KolicinaNaStanju === ''||
        this.proizvod.Popust===''){
        this.greska = "Svi podaci moraju biti popunjeni!"
        return
      }
      if(this.proizvod.Naziv.length<3){
        this.greska = "Naziv mora imati makar 3 karaktera"
        return
      }
      if(this.proizvod.KolicinaNaStanju<0){
        this.greska = "Kolicina ne sme biti manja od 0"
        return
      }
      if(this.proizvod.Cena<=0){
        this.greska = "Cena mora biti veca od 0!"
        return
      }
      try{
        const korisnikData = {
          Naziv: this.proizvod.Naziv,
          Opis: this.proizvod.Opis,
          Cena: this.proizvod.Cena,
          KolicinaNaStanju: this.proizvod.KolicinaNaStanju,
          Popust: this.proizvod.Popust,
          username: this.user.username
        }
        const response = await fetch(`http://localhost:5000/products/add`, {
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
          alert(rez.message || 'Uspesno dodavanje Proizvoda!')
          this.resetForm()
        } else {
          this.greska = rez.error || 'Greska pri dodavanju!'
        }
        this.$router.push('/')
      } catch (error) {
        console.error('Error:', error)
        this.greska = 'Doslo je do greske pri povezivanju sa serverom!'
        this.$router.push('/')
        return
      }
    }
  },
  mounted() {
    this.dohvatiUsera()
  },
}
</script>

<template>
  <div class="container">
    <h1>Dodavanje proizvoda</h1>
    <div class="forma">
      <span class = 'text-danger'>{{greska}}</span>
      <div class = 'col-md-3'>
        Naziv:
        <input type="text" class = 'form-control' v-model = 'proizvod.Naziv'>
      </div>
      <div class = 'col-md-3'>
        Opis:
        <textarea  class = 'form-control' placeholder="Unesite opis" v-model="proizvod.Opis"></textarea>
      </div>
      <div class = 'col-md-3'>
        Cena:
        <input type="number" class = 'form-control' v-model = 'proizvod.Cena'>
      </div>
      <div class = 'col-md-3'>
        Kolicina na stanju:
        <input type="number" class = 'form-control' v-model = 'proizvod.KolicinaNaStanju'>
      </div>
      <div class = 'col-md-3'>
        Popust:
        <input type="number" class = 'form-control' v-model = 'proizvod.Popust'>
      </div>
      <button @click = 'dodaj(user.username)' class = 'btn btn-primary'>Dodaj</button>
      <button @click = 'otkazi' class = 'btn btn-danger'>Otkazi</button>
    </div>
  </div>
</template>

<style scoped>
  span{
    font-weight: 900;
  }
  button{
    margin: 1em 1em 1em 0;
  }
</style>
