import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

import Editar from '../views/Editar.vue';
import Nuevo from '../views/Nuevo.vue';
import Registrar from '../views/Registrar.vue'
import Transacciones from '../views/Transacciones.vue'
import Operaciones from '../views/Operaciones.vue'
import Cuentas from '../views/Cuentas.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/registro',
    name: 'Registro',
    component: Registrar
  },
  {
    path: '/transacciones',
    name: 'Transacciones',
    component: Transacciones
  },
  {
    path: '/operaciones',
    name: 'operaciones',
    component: Operaciones
  },
  {
    path: '/cuentas',
    name: 'cuentas',
    component: Cuentas
  },
  {
    path: '/editar/:id',
    name: 'Editar',
    component: Editar
  },
  {
    path: '/nuevo',
    name: 'Nuevo',
    component: Nuevo
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
