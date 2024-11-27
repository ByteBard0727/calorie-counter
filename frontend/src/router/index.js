import { createRouter, createWebHistory } from 'vue-router'

import LoginPage from '../LoginPage.vue';
import RegisterPage from '../RegisterPage.vue';

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL || '/')
,
    routes: [
      { path: '/', component: LoginPage },
      { path: '/RegisterPage', component: RegisterPage },
    ]
  })

export default router