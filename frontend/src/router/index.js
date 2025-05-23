import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Index.vue'
import Auth from '../views/Auth.vue'
import Regestration from '../views/Regestration.vue'
import Anket from '../views/Ankets.vue'
import Profile from '../views/Profile.vue'
import Recomendations from '../views/Recomendations.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/auth', component: Auth},
  { path: '/regestration', component: Regestration},
  { path: '/createanket', component: Anket},
  { path: '/profile', component: Profile},
  { path: '/recomendations', component: Recomendations}

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router