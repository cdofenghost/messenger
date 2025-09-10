import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/components/Register.vue'
import Authorize from '@/components/Authorize.vue'
import MainWindow from '@/components/MainWindow.vue'

const routes = [
  {
    path: '/authorize',
    name: 'Authorize',
    component: Authorize
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/funchat',
    name: 'MainWindow',
    component: MainWindow
  },


  // By Default:
  {
    path: '/',  
    redirect: '/authorize'  
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
