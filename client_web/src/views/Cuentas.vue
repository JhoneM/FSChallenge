<template>
    <div>
        <Header v-if="sucess" />
        <div v-if="sucess == false"><img src="@/assets/loading.gif" alt="loading"/></div>
        <div class="container izquierda" v-if="sucess">

            <button class="btn btn-primary" v-on:click="nuevo()" >Nueva cuenta</button>
            <br><br>


            <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">Moneda</th>
                    <th scope="col">Balance</th>
                    <th scope="col">Ult. Transaccion</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="cuenta in ListaCuentas" :key="cuenta.acc_id">
                    <td>{{ cuenta.iso_code }}</td>
                    <td>{{ cuenta.balance }}</td>
                    <td>{{ cuenta.last_transaction }}</td>
                </tr>
        
            </tbody>
            </table>

        </div>
        <div class="container" v-if="new_cta">
            <h3>Nueva cuenta</h3>
            <form action="" class="form-horizontal">
                <div class="form-group left">
                    <label for="" class="control-label col-sm-2">Cuentas</label>
                    <div class="col-sm-12">
                        <select class="form-control" name="coin" id="coin" v-model="coin">
                            <option disabled value="">Seleccione una moneda</option>
                            <option v-for="cta in ListaCuentasNew" :key="cta.id" v-bind:value="cta.id">
                                {{ cta.value }}
                            </option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <button type="button" class="btn btn-primary" v-on:click="apertura()" >Apertura de Cuenta</button>
                    <button type="button" class="btn btn-dark margen" v-on:click="salir()"  >Salir</button>
                </div> 
            </form>
        </div>

        <Footer />
    </div>
</template>
<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';
export default {
    name:"Cuentas",
    data(){
        return {
            ListaCuentas:null,
            ListaCuentasNew: null,
            token: localStorage.getItem("token"),
            sucess: false,
            usuario: "",
            new_cta: false,
            coin: ""
        }
    },
    components:{
        Header,
        Footer
    },
    methods:{
        getData(){
            let direccion = "http://localhost:5000/api/accounts";
            axios.get(direccion,{
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then( data =>{
                this.$root.usuario = data.data.result.username
                this.ListaCuentas = data.data.result.accounts
                setTimeout( () => this.sucess = true, 500);
            }).catch(e =>{
                this.sucess = false
                setTimeout( () => this.makeToast("Error Cuentas",`${e}`,"danger"), 500);
                setTimeout( () => this.$router.push({ path: '/'}), 2000);
            });
        },
        nuevo(){
            this.new_cta = true
            let url = "http://localhost:5000/api/accounts_dis";
            axios.get(url,{
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then(data =>{
                this.ListaCuentasNew = data.data.result.values
            }).catch(e =>{
                this.new_cta = false
                this.makeToast("Error de servidor",`${e}`,"danger")
            })
        },
        apertura(){
            if (this.coin == ""){
                this.makeToast("Advertencia","Debe seleccionar una opcion","warning");
            }else{
                let json = {
                    "coin_id": this.coin
                };
                console.log(json)
                axios.post("http://localhost:5000/api/account_new_us", json,{
                    headers: {
                        "Authorization": `Bearer ${this.token}`
                    }
                })
                .then(data =>{
                    console.log(data.data)
                    if (data.data.acc){
                        this.makeToast("Hecho","Cuenta Creada","success");
                        this.salir();
                        this.coin = ""
                        this.getData()
                    }else{
                        this.makeToast("Error","Error al guardar","danger");
                    }

                }).catch( e =>{
                    console.log(e);
                    this.makeToast("Error","Error al guardar","danger");
                })
            }
        },
        salir(){
            this.new_cta = false
        },
        makeToast(titulo,texto,tipo) {
            this.toastCount++
            this.$bvToast.toast(texto, {
                title: titulo,
                variant: tipo,
                autoHideDelay: 5000,
                appendToast: true
            })
        }
    },
    created(){
        if (this.token == null){
            this.$router.push('/');
        }
    },
    mounted:function(){
        this.getData()
    }
}
</script>
<style  scoped>
    .izquierda{
        text-align: left;
    }
</style>