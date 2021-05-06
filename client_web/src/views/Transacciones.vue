<template>
    <div>
        <Header v-if="sucess" />
        <div v-if="sucess == false"><img src="@/assets/loading.gif" alt="loading"/></div>
        <div class="container izquierda" v-if="sucess">
            <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">Operacion</th>
                    <th scope="col">Moneda</th>
                    <th scope="col">Monto</th>
                    <th scope="col">Monto inicial</th>
                    <th scope="col">Monto final</th>
                    <th scope="col">Fecha</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="transaccion in ListTransacciones" :key="transaccion.id">
                    <td>{{ transaccion.op_name }}</td>
                    <td>{{ transaccion.acc_coin }}</td>
                    <td>{{ transaccion.amount }}</td>
                    <td>{{ transaccion.acc_amount_initial }}</td>
                    <td>{{ transaccion.acc_amount_final }}</td>
                    <td>{{ transaccion.date }}</td>
                </tr>
            </tbody>
            </table>
        </div>
        <Footer />
    </div>
</template>
<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';

export default {
    name: "Transacciones",
    data(){
        return {
            ListTransacciones: null,
            token: localStorage.getItem("token"),
            sucess: false
        }
    },
    components:{
        Header,
        Footer,
    },
    methods:{
        getData(){
            let direccion = "http://localhost:5000/api/transactions";
            axios.get(direccion,{
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then( data =>{
                this.$root.usuario = data.data.result.username
                this.ListTransacciones = data.data.result.transactions
                setTimeout( () => this.sucess = true, 500);
            }).catch(e =>{
                this.sucess = false
                setTimeout( () => this.makeToast("Error Transacciones",`${e}`,"danger"), 500);
                setTimeout( () => this.$router.push({ path: '/'}), 2000);
            });
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
    mounted(){
        this.getData();
    }
}
</script>
