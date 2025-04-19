import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Index.vue'
import Auth from '../views/Auth.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/auth', component: Auth}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router