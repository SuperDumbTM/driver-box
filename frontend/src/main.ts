import { createApp } from 'vue'
import ToastPlugin from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-bootstrap.css'
import App from './App.vue'
import './assets/main.css'
import './index.css'
import router from './router'

const app = createApp(App).use(router).use(ToastPlugin)

app.config.globalProperties.$window = window

app.mount('#app')
