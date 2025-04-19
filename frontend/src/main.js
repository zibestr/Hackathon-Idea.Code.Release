import './assets/AuthReg.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import App from './App.vue'
import router from './router'


createApp(App).use(router).use(createPinia(App).use(piniaPluginPersistedstate)).mount('#app')
