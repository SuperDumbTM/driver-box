import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import './index.css'
import router from './router'

createApp(App).use(router).mount('#app')
