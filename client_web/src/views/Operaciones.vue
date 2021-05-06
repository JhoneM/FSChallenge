<template>
    <div>
        <Header v-if="sucess" />
        <div v-if="sucess == false"><img src="@/assets/loading.gif" alt="loading"/></div>
        <div class="wrapper" style="width:80%;margin:auto" v-if="sucess">
            <h3>Operaciones</h3>
            <form>
                <div class="form-row">
                    <div class="form-group col-md-6">
                        <label for="inputState">Operacion</label>
                        <select id="inputState" class="form-control" v-model="form.operation" @change="onChangeOp()">
                            <option v-for="op in ListOperations" :key="op.id" v-bind:value="op.id">
                                {{ op.name }}
                            </option>
                        </select>
                    </div>
                    <div class="form-group col-md-6">
                        <label for="inputState">Cuenta Orig</label>
                        <select id="inputState" class="form-control" v-model="form.cta_org" @change="onChangeCtaOr()">
                            <option v-for="cta_org in ListOrigen" :key="cta_org.iso_code" v-bind:value="cta_org.iso_code">
                                {{ cta_org.iso_code }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group col-md-6">
                        <label for="inputState">Cta Destino</label>
                        <select id="inputState" class="form-control" :disabled="validated == 0" v-model="form.cta_dts">
                            <option v-for="cta_des in ListCtaDest" :key="cta_des.id" v-bind:value="cta_des.id">
                                {{ cta_des.acc_name }}
                            </option>
                        </select>
                    </div>
                    <div class="form-group col-md-6">
                        <label for="inputCity">Monto</label>
                        <vue-numeric class="form-control" currency="$" separator="." v-model="form.amount" v-bind:precision="2" :empty-value="0" @change="onChangeAmount()"></vue-numeric>
                        <div style="color:green;font-size:12px" v-if="balanceCta > 0">
                            El limite para transacciones es de {{balanceCta}}
                        </div>
                        <div style="color:red;font-size:12px" v-if="error_amount">
                            {{error_msg}}
                        </div>
                    </div>
                </div>
                <button type="button" class="btn btn-primary" :disabled="validatedBtn == 0" v-on:click="confirmar()">Confirmar</button>
            </form>
        </div>
        <Footer/>
    </div>
</template>
<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';
import VueNumeric from 'vue-numeric';

export default {
    name:"Operaciones",
    data(){
        return{
            ListOrigen: null,
            ListOperations: null,
            ListCtaDest: null,
            transfer: false,
            ctaOrg: false,
            sucess: false,
            error_amount: false,
            error_msg: "",
            limitAmount: false,
            balanceCta: 0,
            token: localStorage.getItem("token"),
            usuario: "",
            validated: 0,
            validatedBtn: 0,
            form: {
                "operation": "",
                "cta_org": "",
                "cta_dts": "",
                "amount": ""
            }
        }
    },
    components:{
        Header,
        Footer,
        VueNumeric
    },
    methods: {
        getCtaOrigen(){
            let url = "http://localhost:5000/api/accounts";
            axios.get(url,{
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then( data =>{
                // console.log(data.data.result.username)
                this.$root.usuario = data.data.result.username
                this.ListOrigen = data.data.result.accounts
                setTimeout( () => this.sucess = true, 500);
                // setTimeout( () => this.ListaCuentas = data.data.result.accounts, 1500);
            }).catch(e =>{
                this.sucess = false
                setTimeout( () => this.makeToast("Error Servidor Cuentas",`${e}`,"danger"), 1000);
                setTimeout( () => this.$router.push({ path: 'cuentas'}), 2000);
            });
        },
        getOperations(){
            let url = "http://localhost:5000/api/operations_us";
            axios.get(url,{
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then( data =>{
                // console.log(data.data.result)
                this.ListOperations = data.data.result.operations
            }).catch(e =>{
                this.sucess = false
                setTimeout( () => this.makeToast("Error Servidor Operaciones",`${e}`,"danger"), 1000);
                setTimeout( () => this.$router.push({ path: 'cuentas'}), 2000);
            });
        },
        getCtsDest(){
            let url = "http://localhost:5000/api/accounts_dest?iso=" + this.form.cta_org;
            axios.get(url,{
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then( data => {
                this.ListCtaDest = data.data.result.accounts
            }).catch( e =>{
                setTimeout( () => this.makeToast("Error Servidor Cuentas",`${e}`,"danger"), 1000);
                setTimeout( () => this.$router.push({ path: 'cuentas'}), 2000);
            });
        },
        getMontoMax(){
            let url = "http://localhost:5000/api/acc_amount_max?iso=" + this.form.cta_org;
            axios.get(url,{
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then( data => {
                this.balanceCta = data.data.result.account.balance
                if (this.balanceCta == 0){
                    this.error_amount = true;
                    this.error_msg = "Usted no posee fondos en esta cuenta."
                    this.validatedBtn = 0
                }else if (this.balanceCta > 0){
                    this.error_amount = false;
                    this.error_msg = "";
                    this.validatedBtn = 0
                }
            }).catch( e =>{
                setTimeout( () => this.makeToast("Error Servidor Cuentas",`${e}`,"danger"), 1000);
                setTimeout( () => this.$router.push({ path: 'cuentas'}), 2000);
            });
        },
        onChangeOp(){
            this.form.amount = 0;
            // this.onChangeAmount();

            if (this.form.operation == 3){
                this.transfer = true;

            }else if (this.form.operation == 1 && this.ctaOrg){
                this.transfer = false;
                this.error_amount = false;
                this.error_msg = "";
                this.balanceCta = 0;
            }else if (this.form.operation == 2 && this.ctaOrg){
                this.transfer = false;
                this.getMontoMax();
            }
            
            if (this.transfer && this.ctaOrg){
                this.getCtsDest();
                this.getMontoMax();
                this.validated = 1;
                if (this.form.cta_dts == ""){
                    this.getMontoMax();
                    this.validatedBtn = 0
                }
            }
            else{
                this.validated = 0;
                this.form.cta_dts = "";
            }
        },
        onChangeCtaOr(){
            this.form.amount = 0;
            if (this.form.cta_org != ""){
                this.ctaOrg = true;
                if (this.ctaOrg && (this.form.operation == 2 || this.form.operation == 3 )){
                    console.log("hola")
                    this.getMontoMax();
                }
                else if (this.ctaOrg && this.form.operation == 1){
                    this.transfer = false;
                    this.error_amount = false;
                    this.error_msg = "";
                    this.balanceCta = 0;
                }
            }else{
                this.ctaOrg = false;
            }
            if (this.transfer && this.ctaOrg){
                this.getCtsDest();
                this.validated = 1;
                if (this.form.cta_dts != ""){
                    this.getMontoMax();
                }else{
                    this.validatedBtn = 0
                }
            }else{
                this.validated = 0;
                this.form.cta_dts = "";
            }
        },
        onChangeAmount(){
            if (this.form.operation != 1 ){
                if (this.form.amount > this.balanceCta){
                    this.error_amount = true;
                    this.error_msg = "Este monto supera el balance de su cuenta.";
                    this.validatedBtn = 0;
                }else if(this.form.amount == 0){
                    this.error_amount = true;
                    this.error_msg = "Tiene que ingresar un monto valido.";
                    this.validatedBtn = 0;

                }else{
                    this.validatedBtn = 1;
                    this.error_amount = false;
                    this.error_msg = "";
                }

            }else if (this.form.operation == 1 && this.form.amount == 0){
                this.error_amount = true;
                this.error_msg = "Tiene que ingresar un monto valido.";
                this.validatedBtn = 0;
            }
            else{
                this.validatedBtn = 1;
                this.error_amount = false;
                this.error_msg = "";
            }

        },
        confirmar(){
            let url = "http://localhost:5000/api/make_operation";
            axios.post(url, this.form, {
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            }).then( data =>{
                console.log(data)
                if (data.status == 200){
                    this.makeToast("Hecho","Operacion realizada. Redirigiendo","success");
                    this.validatedBtn = 0;
                    setTimeout( () => this.$router.push({ path: 'transacciones'}), 500);
                }else{
                    this.makeToast("Error","Hubo un error, por favor intente más tarde.","danger");
                }
            }).catch( e => {
                this.validatedBtn = 0;
                this.makeToast("Error",`${e}`,"danger");
                setTimeout( () => this.$router.push({ path: 'cuentas'}), 500);
            })
        },
        makeToast(titulo,texto,tipo) {
            this.toastCount++
            this.$bvToast.toast(texto, {
                title: titulo,
                variant: tipo,
                autoHideDelay: 5000,
                appendToast: true
            })
        },

    },
    created(){
    },
    mounted(){
        this.getCtaOrigen();
        this.getOperations();
    }
}
</script>