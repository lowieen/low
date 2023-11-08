import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/index';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: {requiresAuth: true}
    },
    {
      path: '/support',
      name: 'support',
      component: () => import('../views/SupportView.vue'),
      meta: {requiresAuth:true}
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue'),
      meta: {requiresAuth:true}
    },
    {
      path: '/messages',
      name: 'messages',
      component: () => import('../views/MessagesView.vue'),
      meta: {requiresAuth:true},
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: () => import('../views/NotificationsView.vue'),
      meta: {requiresAuth:true}
    },
    {
      path: '/options',
      name: 'options',
      component: () => import('../views/OptionsView.vue'),
      meta: {requiresAuth:true}
    },
    {
      path: '/new-password/:token',
      name: 'new-password',
      component: () => import('../views/NewPassword.vue'),
    },
    {
      path: '/restore-password',
      name: 'restore-password',
      component: () => import('../views/RestorePassword.vue'),
    },
    {
      path: '/:user',
      name: 'user-profile',
      component: () => import('../components/UserProfile.vue'),
      props: true,
    }
  ]
})

// Verificar la autenticación
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated; // Usa el getter del store importado

  if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated) {
    // Si la ruta requiere autenticación y el usuario no está autenticado, redirige a /login
    next('/login');
  } else {
    next();
  }
});


export default router
