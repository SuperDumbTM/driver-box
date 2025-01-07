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
      component: () => import('../views/driver/DriverGroupView.vue')
    },
    {
      path: '/drivers/create',
      component: () => import('../views/driver/DriverGroupFormView.vue')
    },
    {
      path: '/drivers/edit/:id',
      component: () => import('../views/driver/DriverGroupFormView.vue')
    },
    {
      path: '/settings',
      name: 'setting',
      component: () => import('../views/app_setting/AppSettingView.vue')
    },
    {
      path: '/porter',
      name: 'porter',
      component: () => import('../views/porter/PorterView.vue')
    }
  ]
})

export default router
