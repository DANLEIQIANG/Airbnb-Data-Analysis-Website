import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/overview'
  },
  {
    path: '/overview',
    name: 'Overview',
    meta: {
      title: 'Overview'
    },
    component: () => import('../components/Overview.vue')
  },
  {
    path: '/tenant',
    name: 'Tenant',
    meta: {
      title: 'Tenant'
    },
    component: () => import('../components/Tenant.vue')
  },
  {
    path: '/landlord',
    name: 'Landlord',
    meta: {
      title: 'Landlord'
    },
    component: () => import(/* webpackChunkName: "about" */ '../components/Landlord.vue')
  },
  {
    path: '/investor',
    name: 'Investor',
    meta: {
      title: 'Investor'
    },
    component: () => import(/* webpackChunkName: "about" */ '../components/Investor.vue')
  },
   {
    path: '/machinelearning',
    name: 'MachineLearning',
    meta: {
      title: 'MachineLearning'
    },
    component: () => import(/* webpackChunkName: "about" */ '../components/MachineLearning.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
