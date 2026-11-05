<template>
  <header class="site-header">
    <div class="header-surface">
      <div class="header-content">
        <RouterLink to="/" class="brand">
          SkillGig
        </RouterLink>

        <nav class="primary-nav" aria-label="Primary navigation">
          <RouterLink to="/" class="nav-link" exact-active-class="is-active">Home</RouterLink>
          <RouterLink to="/get-started" class="nav-link" exact-active-class="is-active">Get started</RouterLink>
          <RouterLink to="/questions" class="nav-link" exact-active-class="is-active">Questions</RouterLink>
          <RouterLink to="/faq" class="nav-link" exact-active-class="is-active">FAQ</RouterLink>
          <RouterLink to="/about" class="nav-link" exact-active-class="is-active">About</RouterLink>
        </nav>

        <div class="header-actions">
          <template v-if="!isAuthenticated">
            <RouterLink to="/register" class="register-btn">
              Register Now
            </RouterLink>
            <RouterLink to="/login" class="login-link">
              Log in
            </RouterLink>
          </template>
          <UserMenu v-else />
        </div>

        <label class="hamburger" :class="{ 'is-active': isMenuOpen }">
          <input 
            type="checkbox" 
            :checked="isMenuOpen"
            @change="toggleMenu"
            aria-label="Toggle navigation"
          >
          <svg viewBox="0 0 32 32">
            <path class="line line-top-bottom" d="M27 10 13 10C10.8 10 9 8.2 9 6 9 3.5 10.8 2 13 2 15.2 2 17 3.8 17 6L17 26C17 28.2 18.8 30 21 30 23.2 30 25 28.2 25 26 25 23.8 23.2 22 21 22L7 22"></path>
            <path class="line" d="M7 16 27 16"></path>
          </svg>
        </label>
      </div>
    </div>

    <transition name="slide-fade">
      <div v-if="isMenuOpen" class="mobile-panel">
        <nav class="mobile-nav" aria-label="Mobile navigation">
          <RouterLink to="/" class="mobile-link" exact-active-class="is-active" @click="closeMenu">Home</RouterLink>
          <RouterLink to="/get-started" class="mobile-link" exact-active-class="is-active" @click="closeMenu">Get started</RouterLink>
          <RouterLink to="/questions" class="mobile-link" exact-active-class="is-active" @click="closeMenu">Questions</RouterLink>
          <RouterLink to="/faq" class="mobile-link" exact-active-class="is-active" @click="closeMenu">FAQ</RouterLink>
          <RouterLink to="/about" class="mobile-link" exact-active-class="is-active" @click="closeMenu">About</RouterLink>
          <template v-if="!isAuthenticated">
            <RouterLink to="/register" class="mobile-register-btn" @click="closeMenu">Register Now</RouterLink>
            <RouterLink to="/login" class="mobile-login-link" @click="closeMenu">Log in</RouterLink>
          </template>
          <template v-else>
            <div class="user-info-mobile">
              <span class="user-name-mobile">{{ mobileUserName }}</span>
              <span class="user-email-mobile">{{ user?.email }}</span>
            </div>
            <RouterLink
              to="/profile"
              class="mobile-link"
              exact-active-class="is-active"
              @click="closeMenu"
            >
              Profile
            </RouterLink>
            <button class="mobile-link mobile-logout" @click="handleLogout">
              Log out
            </button>
          </template>
        </nav>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/useAuthStore'
import UserMenu from './UserMenu.vue'

const isMenuOpen = ref(false)
const router = useRouter()
const authStore = useAuthStore()
const { isAuthenticated, user } = storeToRefs(authStore)

const mobileUserName = computed(() => {
  const currentUser = user.value
  if (!currentUser) {
    return 'User'
  }

  const fullName = [
    currentUser.firstName ?? currentUser.name?.split(' ')?.[0],
    currentUser.lastName ?? currentUser.name?.split(' ')?.[1]
  ]
    .filter(Boolean)
    .join(' ')

  return (
    fullName ||
    currentUser.name ||
    currentUser.username ||
    currentUser.email ||
    'User'
  )
})

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
  closeMenu()
}

onMounted(() => {
  if (authStore.getIsAuthenticated && !user.value) {
    authStore.hydrateUser().catch((error) => {
      console.error('Header hydrate error:', error)
    })
  }
})
</script>

<style scoped>
.site-header {
  position: relative;
  display: flex;
  justify-content: center;
}

.header-surface {
  width: 100%;
  background: #FFFFFF;
  padding: 1rem 1.25rem;
  display: flex;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 90%;
  max-width: 1400px;
}

.brand {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--text-dark);
  flex-shrink: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.primary-nav {  
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-left: auto;
  margin-right: 24px;
}



.nav-link {
  font-size: 0.95rem;
  color: var(--text-dark);
  cursor: pointer;
  position: relative;
  font-family: Arial, Helvetica, sans-serif;
  transition-timing-function: cubic-bezier(0.25, 0.8, 0.25, 1);
  transition-duration: 400ms;
  transition-property: color;
}

.nav-link:focus,
.nav-link:hover {
  color: #000000;
}

.nav-link:focus:after,
.nav-link:hover:after {
  width: 100%;
  left: 0%;
}

.nav-link:after {
  content: "";
  pointer-events: none;
  bottom: -2px;
  left: 50%;
  position: absolute;
  width: 0%;
  height: 2px;
  background-color: #000000;
  transition-timing-function: cubic-bezier(0.25, 0.8, 0.25, 1);
  transition-duration: 400ms;
  transition-property: width, left;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link.is-active {
  color: #000000;
  font-weight: 600;
}

.nav-link.is-active:after {
  width: 100%;
  left: 0%;
}

.register-btn,
.login-link {
  font-size: 16.3px;  
  margin-top: -5px;
  background: transparent;
  border: none;
  padding: 0.6em 0.8rem;
  color: #337f35;
  font-weight: 400;
  position: relative;
  transition: 0.5s ease;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  z-index: 1;
}

.register-btn::before,
.login-link::before {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 2px;
  width: 0;
  background-color: #4CAF4F;
  transition: 0.5s ease;
  pointer-events: none;
}

.register-btn:hover,
.login-link:hover {
  color: #FFFFFF;
  transition-delay: 0.5s;
}

.register-btn:hover::before,
.login-link:hover::before {
  width: 100%;
}

.register-btn::after,
.login-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 0;
  width: 100%;
  background-color: #4CAF4F;
  transition: 0.4s ease;
  z-index: -1;
  pointer-events: none;
}

.register-btn:hover::after,
.login-link:hover::after {
  height: 100%;
  transition-delay: 0.4s;
  color: aliceblue;
}

/* Бургер кнопкасы */
.hamburger {
  display: none;
  cursor: pointer;
  margin-left: auto;
  position: relative;
  z-index: 101;
}

.hamburger input {
  display: none;
}

.hamburger svg {
  /* The size of the SVG defines the overall size */
  height: 3em;
  width: 3em;
  /* Define the transition for transforming the SVG */
  transition: transform 600ms cubic-bezier(0.4, 0, 0.2, 1);
}

.line {
  fill: none;
  stroke: #000000;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 3;
  /* Define the transition for transforming the Stroke */
  transition: stroke-dasharray 600ms cubic-bezier(0.4, 0, 0.2, 1),
              stroke-dashoffset 600ms cubic-bezier(0.4, 0, 0.2, 1);
}

.line-top-bottom {
  stroke-dasharray: 12 63;
}

.hamburger input:checked + svg,
.hamburger.is-active svg {
  transform: rotate(-45deg);
}

.hamburger input:checked + svg .line-top-bottom,
.hamburger.is-active svg .line-top-bottom {
  stroke-dasharray: 20 300;
  stroke-dashoffset: -32.42;
}

/* Мобильді панель */
.mobile-panel {
  display: none;
  position: fixed;
  top: 72px;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--surface);
  padding: 2rem 1.5rem;
  overflow-y: auto;
  z-index: 99;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.user-info-mobile {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border-radius: 0.75rem;
  background: rgba(16, 185, 129, 0.08);
  margin-bottom: 0.5rem;
}

.user-name-mobile {
  font-weight: 600;
  color: #064e3b;
}

.user-email-mobile {
  font-size: 0.9rem;
  color: #065f46;
}

.mobile-link {
  font-size: 1.1rem;
  color: var(--text-dark);
  padding: 1rem;
  border-radius: 0.75rem;
  font-family: Arial, Helvetica, sans-serif;
  transition: background 0.2s ease;
}

.mobile-link:hover {
  background: rgba(0, 0, 0, 0.06);
}

.mobile-link.is-active {
  background: rgba(0, 0, 0, 0.08);
  font-weight: 600;
}

.mobile-logout {
  background: rgba(248, 113, 113, 0.15);
  color: #b91c1c;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.mobile-logout:hover {
  background: rgba(248, 113, 113, 0.3);
}


.mobile-register-btn,
.mobile-login-link {
  font-size: 17px;
  background: transparent;
  border: none;
  padding: 0.8em 1.4em;
  color: #000000;
  position: relative;
  transition: 0.5s ease;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
  margin-top: 1rem;
  border-radius: 0.75rem;
  width: 100%;
}

.mobile-register-btn::before,
.mobile-login-link::before {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 2px;
  width: 0;
  background-color: #4CAF4F;
  transition: 0.5s ease;
}

.mobile-register-btn:hover,
.mobile-login-link:hover {
  color: #FFFFFF;
  transition-delay: 0.5s;
}

.mobile-register-btn:hover::before,
.mobile-login-link:hover::before {
  width: 100%;
}

.mobile-register-btn::after,
.mobile-login-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  height: 0;
  width: 100%;
  background-color: #4CAF4F;
  transition: 0.4s ease;
  z-index: -1;
}

.mobile-register-btn:hover::after,
.mobile-login-link:hover::after {
  height: 100%;
  transition-delay: 0.4s;
  color: aliceblue;
}

@media (max-width: 1024px) {
  .primary-nav {
    gap: 10px;
    margin-right: 10px;
  }

  .header-actions {
    gap: 10px;
  }
}

@media (max-width: 855px) {
  .header-content {
    gap: 1rem;
  }

  .primary-nav,
  .header-actions {
    display: none;
  }

  .hamburger {
    display: block;
  }

  .mobile-panel {
    display: block;
  }
}

/* Анимация */
.slide-fade-enter-active {
  animation: slideIn 0.3s ease-out;
}

.slide-fade-leave-active {
  animation: slideOut 0.3s ease-in;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}
</style>
