import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Index.vue'
import Auth from '../views/Auth.vue'
import Regestration from '../views/Regestration.vue'
import Anket from '../views/Ankets.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/auth', component: Auth},
  { path: '/regestration', component: Regestration},
  { path: '/createanket', component: Anket},

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router