<script>
import axios from 'axios'
export default {
  name: 'ProizvodiProdavcaView',
  props: ['username'],
  data() {
    return {
      proizvodi: [],
      user: null,
    }
  },
  methods: {
    parseIfString(data) {
      return typeof data === 'string' ? JSON.parse(data) : data
    },
    async dohvatiSveProizvode() {
      const response = await axios.get(`http://127.0.0.1:5000/products/${this.username}`)
      this.proizvodi = this.parseIfString(response.data.proizvodi)
      console.log(response.data.proizvodi)
    },
    izracunajCenu(cena,popust){
      cena = cena * (100-popust)*0.01
      return cena
    },
    vidi(id){
      this.$router.push(`/productView/${id}`)
    },
    izmeni(id){
      this.$router.push(`/product/update/${id}`)
    },
    dohvatiUsera(){
      const data = localStorage.getItem("user")
      if(data){
        this.user = JSON.parse(data)
      }
    },
    async obrisi(id){
      await axios.delete(`http://127.0.0.1:5000/products/delete/${id}`)
      await this.dohvatiSveProizvode()
    },
  },
  mounted() {
    this.dohvatiSveProizvode()
    this.dohvatiUsera()
  },
}
</script>

<template>
  <div class = 'container'>
    <h1>Proizvodi:</h1>
    <table class = 'table'>
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
      <tr v-for = 'proizvod in proizvodi' :key = 'proizvod.ID'>
        <th>{{proizvod.ID}}</th>
        <th>{{proizvod.Naziv}}</th>
        <th>{{proizvod.Opis}}</th>
        <th>{{proizvod.Cena}}</th>
        <th>{{proizvod.KolicinaNaStanju}}</th>
        <th>{{proizvod.Popust}}%</th>
        <th>{{izracunajCenu(proizvod.Cena, proizvod.Popust)}}</th>
        <th>
          <button @click = 'vidi(proizvod.ID)' class = 'btn btn-primary'>Detaljnije</button>
        </th>
        <th>
          <button @click = 'izmeni(proizvod.ID)' class = 'btn btn-success'>Izmeni</button>
        </th>
        <th>
          <button @click = 'obrisi(proizvod.ID)' class = 'btn btn-danger'>Obrisi</button>
        </th>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped></style>
