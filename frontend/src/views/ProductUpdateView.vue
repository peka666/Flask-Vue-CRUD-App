<script>
import axios from 'axios'

export default {
  name: 'ProductUpdateView',
  props: ['id'],
  data(){
    return{
      korisnik:{
        username: '',
        sifra: '',
        vrstaKorisnika: '',
      },
      proizvodi: [],
      greska: '',
      proizvod:{
        Naziv: '',
        Opis: '',
        Cena: '',
        KolicinaNaStanju: '',
        Popust: '',
      }
    }
  },
  methods:{
    dohvatiKorisnika(){
      const data = localStorage.getItem('user')
      if(data){
        this.korisnik = JSON.parse(data)
      }
    },
    otkazi(){
      this.$router.push('/')
    },
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    async dohvatiSveProizvode() {
      const response = await axios.get('http://127.0.0.1:5000/products')
      this.proizvodi = this.parseIfString(response.data.proizvodi)
      this.proizvod = this.proizvodi.find((p)=>p.ID===Number(this.id))
      console.log(this.id)
    },
    async izmeni(id){
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
      if(this.proizvod.KolicinaNaStanju<=0){
        this.greska = "Kolicina ne sme biti manja od 0"
        return
      }
      if(this.proizvod.Cena<=0){
        this.greska = "Cena mora biti veca od 0!"
        return
      }

      console.log(this.proizvod.Popust)

      const proizvodData = {
        Naziv: this.proizvod.Naziv,
        Opis: this.proizvod.Opis,
        Cena: parseFloat(this.proizvod.Cena),
        KolicinaNaStanju: parseInt(this.proizvod.KolicinaNaStanju),
        Popust: parseFloat(this.proizvod.Popust)
      }
      try {
        const response = await fetch(`http://localhost:5000/products/update/${id}`,{
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(proizvodData),
        })

        const rez = await response.json()
        if (rez.success) {
          alert('Uspesno!')
          this.$router.push(`/`)
        } else {
          this.greska = rez.error
        }
      } catch (error) {
        this.greska = 'Server error'
      }
    }
  },
  mounted() {
    this.dohvatiSveProizvode()
    this.dohvatiKorisnika()
  }
}
</script>

<template>
  <div class="container">
    <h1>Izmena proizvoda:</h1>
    <div class="form">
      <span class = 'text-danger'>{{greska}}</span>
      <div class="col-md-3">
        Naziv
        <input type="text" class="form-control" v-model="proizvod.Naziv" />
      </div>
      <div class="col-md-3">
        Opis
        <input type="text" class="form-control" v-model="proizvod.Opis" />
      </div>
      <div class="col-md-3">
        Cena
        <input type="text" class="form-control" v-model="proizvod.Cena" />
      </div>
      <div class="col-md-3">
        Kolicina
        <input type="text" class="form-control" v-model="proizvod.KolicinaNaStanju" />
      </div>
      <div class="col-md-3">
        Popust
        <input type="text" class="form-control" v-model="proizvod.Popust" />
      </div>
      <button @click="izmeni(id)" class="btn btn-primary">Izmeni</button>
      <button @click="otkazi" class="btn btn-danger">Otkazi</button>
    </div>
  </div>
</template>

<style scoped>
  span{
    font-weight: 900;
  }
  button{
    margin: 1em 1em 0 0;
  }
</style>
