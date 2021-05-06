<template>
  <div style="margin-bottom:2%">
    <nav class="navbar navbar-expand-sm   navbar-light bg-light">
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item">
            <a class="nav-link">Home <span>{{$root.usuario}}</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" style="cursor:pointer;" v-on:click="cuentas()">Cuentas</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" style="cursor:pointer;" v-on:click="transacciones()">Transacciones Historicas</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" style="cursor:pointer;" v-on:click="operaciones()">Operaciones</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" style="cursor:pointer;" v-on:click="salir()">Salir</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>

</template>
<script>
import axios from 'axios';
export default {
    name:"Header",
    data(){
        return {
          usuario: ""
        }
    },
    components:{
    },
    methods:{
      cuentas(){
        this.$router.push('/cuentas');
      },
      transacciones(){
        this.$router.push('/transacciones');
      },
      operaciones(){
        this.$router.push('/operaciones');
      },
      salir(){
        let url = "http://localhost:5000/api/logout";
        axios.get(url).then(data =>{
          if (data.data.status == "ok"){
            localStorage.removeItem('token');
            this.$router.push('/');
          }
        });
      }

    },
}
</script>
<style  scoped>
  .social-part .fa{
    padding-right:20px;
  }
  ul li a{
      margin-right: 20px;
  }

</style>