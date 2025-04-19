import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Index.vue'
import Auth from '../views/Auth.vue'
import Regestration from '../views/Regestration.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/auth', component: Auth},
  { path: '/regestration', component: Regestration}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router