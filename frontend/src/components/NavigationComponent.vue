<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'NavigationComponent',
  data() {
    return {
      menu: [
        {
          url: '/',
          title: 'Home',
        },
        {
          url: '/profile',
          title: 'Profile',
        },
      ]
    }
  }
})
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <router-link
            class="nav-link"
            :to="link.url"
            v-for="link in menu"
            :key="link.url"
            :class="{ active: $route.path === link.url }"
          >
            {{ link.title }}
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped></style>
