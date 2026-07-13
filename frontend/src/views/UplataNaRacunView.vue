<script>
export default {
  name: 'UplataNaRacunView',
  data(){
    return{
      greska: '',
      iznos: 0
    }
  },
  methods:{
    uplati(){
      if(this.iznos<=0){
        this.greska = "Neispravan unos"
        return
      }
    },
    otkazi(){
      this.$router.push('/')
    }
  }
}
</script>

<template>
  <div class = 'container'>
    <h1>Zdravo</h1>
    <div class = 'forma'>
      <span class = 'text-danger'>{{greska}}</span>
      <div class = 'col-md-3'>
        Unesite iznos koji zelite da uplatite:
        <input type="number" class = 'form-control' v-model="iznos">
      </div>
      <button @click = 'uplati' class = 'btn btn-primary'>Uplati</button>
      <button @click = 'otkazi' class = 'btn btn-danger'>Otkazi</button>
    </div>
  </div>
</template>

<style scoped>
  button{
    margin: 1em 1em 0 0;
  }
  span{
    font-weight: 900;
  }
</style>
