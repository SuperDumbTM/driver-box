import { i18n } from '@/i18n'
import { createApp } from 'vue'
import { LoadingPlugin } from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/css/index.css'
import ToastPlugin from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-bootstrap.css'
import App from './App.vue'
import './assets/main.css'
import './index.css'
import router from './router'

const app = createApp(App)
  .use(router)
  .use(ToastPlugin, { position: 'top-right' })
  .use(i18n)
  .use(LoadingPlugin)

app.config.globalProperties.$window = window

app.mount('#app')
