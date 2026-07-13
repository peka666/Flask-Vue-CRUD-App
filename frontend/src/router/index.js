import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProfileUpdate from '@/views/ProfileUpdate.vue'
import ProductsView from '@/views/ProductsView.vue'
import ProductAddView from '@/views/ProductAddView.vue'
import ProductView from '@/views/ProductView.vue'
import UplataNaRacunView from '@/views/UplataNaRacunView.vue'
import AllUsersView from '@/views/AllUsersView.vue'
import AdminUpdateUser from '@/views/AdminUpdateUser.vue'
import AddAdminView from '@/views/AddAdminView.vue'
import ProizvodiProdavcaView from '@/views/ProizvodiProdavcaView.vue'
import ProductUpdateView from '@/views/ProductUpdateView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: "HomeView",
      component: HomeView
    },
    {
      path: '/login',
      name: "LoginView",
      component: LoginView,
    },
    {
      path: '/register',
      name: "RegisterView",
      component: RegisterView,
    },
    {
      path: '/profile',
      name: "ProfileView",
      component: ProfileView,
    },
    {
      path: '/profile/update/:id',
      name: "ProfileUpdate",
      component: ProfileUpdate,
      props: true,
    },
    {
      path: '/products',
      name: "ProductsView",
      component: ProductsView,
    },
    {
      path:'/productView/:id',
      name: 'ProductView',
      component: ProductView,
      props: true
    },
    {
      path:'/uplataNaRacun/:id',
      name: 'UplataNaRacunView',
      component: UplataNaRacunView,
      props: true
    },
    {
      path: '/products/add',
      name: "ProductAddView",
      component: ProductAddView,
    },
    {
      path: '/admin/users',
      name: "AllUsersView",
      component: AllUsersView,
    },
    {
      path: '/admin/users/update/:id',
      name: "AdminUpdateUser",
      component: AdminUpdateUser,
      props: true,
    },
    {
      path: '/add/admin',
      name: "AddAdminView",
      component: AddAdminView
    },
    {
      path: '/products/user/:username',
      name: 'ProizvodiProdavcaView',
      component: ProizvodiProdavcaView,
      props: true
    },
    {
      path: '/product/update/:id',
      name: 'ProductUpdateView',
      component: ProductUpdateView,
      props: true,
    }
  ],
})

export default router
