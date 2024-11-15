import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/home/HomeView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/drivers',
      name: 'driver',
      component: () => import('../views/driver/DriverView.vue')
    },
    {
      path: '/settings',
      name: 'setting',
      component: () => import('../views/app_setting/AppSettingView.vue')
    }
  ]
})

export default router
