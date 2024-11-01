import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/drivers',
      name: 'driver',
      component: () => import('../views/DriverView.vue')
    },
    {
      path: '/settings',
      name: 'setting',
      component: () => import('../views/AppSettingView.vue')
    }
  ]
})

export default router
