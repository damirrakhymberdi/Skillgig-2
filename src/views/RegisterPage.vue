<template>
  <div class="register-page">
    <!-- Левая часть с изображением -->
    <div class="register-left">
      <img :src="registerImage" alt="Background" class="register-image">
      
      <!-- Логотип в верхнем левом углу -->
      <div class="logo-overlay">
        <RouterLink to="/" class="logo-link">
          SkillGig
        </RouterLink>
      </div>
      
      <!-- Текст поверх изображения -->
      <div class="text-overlay">
        <h1 class="overlay-title">Let's build from here</h1>
        <p class="overlay-subtitle">
          Building the future of IT collaboration through community-driven knowledge sharing
        </p>
      </div>
      
      <!-- Подпись внизу -->
      <div class="attribution-overlay">
        <p class="attribution-text">
          Uploaded on February 20, 2025 by Damir Rakhymberdi
        </p>
      </div>
    </div>

    <!-- Правая часть с формой -->
    <div class="register-right">
      <div class="register-form-container">
        <h2 class="form-title">Join SkillGig</h2>
        <p class="login-link-text">
          Already have an account? 
          <RouterLink to="/login" class="login-link">Login</RouterLink>
        </p>

        <p v-if="errorMessage" class="status-text error">
          {{ errorMessage }}
        </p>

        <form class="register-form" @submit.prevent="handleSubmit">
          <!-- Имя и фамилия в одну строку -->
          <div class="name-row">
            <div class="form-group">
              <input
                type="text"
                id="firstName"
                v-model="formData.firstName"
                placeholder="First name"
                class="form-input"
                autocomplete="given-name"
                required
              />
            </div>
            <div class="form-group">
              <input
                type="text"
                id="lastName"
                v-model="formData.lastName"
                placeholder="Last name"
                class="form-input"
                autocomplete="family-name"
                required
              />
            </div>
          </div>

          <!-- Email -->
          <div class="form-group">
            <input
              type="email"
              id="email"
              v-model="formData.email"
              placeholder="Email"
              class="form-input"
                autocomplete="email"
              required
            />
          </div>

          <!-- Username -->
          <div class="form-group">
            <input
              type="text"
              id="username"
              v-model="formData.username"
              placeholder="Username"
              class="form-input"
                minlength="3"
                maxlength="30"
                pattern="[A-Za-z0-9_]+"
                autocomplete="username"
              required
            />
            <p class="input-hint">(only letters, numbers and underscores)</p>
          </div>

          <div class="form-group">
            <label class="input-label" for="role">Account type</label>
            <select id="role" v-model="formData.role" class="form-input">
              <option value="client">I want to ask questions</option>
              <option value="expert">I want to answer as an IT specialist</option>
            </select>
            <p class="input-hint">You can update your expert details in profile settings.</p>
          </div>

          <!-- Password -->
          <div class="form-group">
            <input
              type="password"
              id="password"
              v-model="formData.password"
              placeholder="Password"
              class="form-input"
                minlength="8"
                maxlength="72"
                autocomplete="new-password"
              required
            />
            <p class="input-hint">(min. 8 char)</p>
          </div>

          <!-- Кнопка Join -->
          <button type="submit" class="join-button" :disabled="isSubmitting">
            {{ isSubmitting ? 'Создаем...' : 'Join' }}
          </button>

          <p class="terms-text">
            Questions and answers you post may be visible to other users. Do not include private or sensitive information.
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import registerImage from '@/assets/images/registerimage.jpg'
import { registerUser, loginUser } from '@/services/authservice'
import { useAuthStore } from '@/stores/useAuthStore'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  firstName: '',
  lastName: '',
  email: '',
  username: '',
  password: '',
  role: 'client'
})

const isSubmitting = ref(false)
const errorMessage = ref('')

const normalizeField = (value) => value?.trim() ?? ''

const handleSubmit = async () => {
  if (isSubmitting.value) {
    return
  }

  errorMessage.value = ''
  isSubmitting.value = true

  const payload = {
    firstName: normalizeField(formData.value.firstName),
    lastName: normalizeField(formData.value.lastName),
    email: normalizeField(formData.value.email),
    username: normalizeField(formData.value.username),
    password: formData.value.password,
    role: formData.value.role
  }

  try {
    await registerUser(payload)

    const authData = await loginUser({
      email: payload.email,
      password: payload.password
    })

    authStore.login(authData)
    await authStore.hydrateUser({ force: true })
    router.push('/')
  } catch (error) {
    errorMessage.value =
      error?.payload?.detail ||
      error?.payload?.message ||
      error.message ||
      'Регистрация сәтсіз аяқталды. Қайта көріңіз.'
  } finally {
    isSubmitting.value = false
  }
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.register-page {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

/* Левая часть с изображением */
.register-left {
  position: relative;
  width: 50%;
  height: 100vh;
  overflow: hidden;
}

.register-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  opacity: 0.5;
}

.logo-overlay {
  position: absolute;
  top: 2rem;
  left: 2rem;
  z-index: 10;
}

.logo-link {
  color: #FFFFFF;
  font-size: 1.5rem;
  font-weight: 700;
  text-decoration: none;
  letter-spacing: 0.05em;
  transition: opacity 0.3s ease;
}

.logo-link:hover {
  opacity: 0.8;
}

.text-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  text-align: start;
  width: 84%;
  max-width: 700px;
}

.overlay-title {
  font-size: 3.1rem;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 0 1rem 0;
  line-height: 1.1;
  text-align: start;
}

.overlay-subtitle {
  font-size: 1.3rem;
  color: #FFFFFF;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
  text-align: start;
}

.attribution-overlay {
  position: absolute;
  bottom: 2rem;
  left: 2rem;
  z-index: 10;
}

.attribution-text {
  font-size: 0.875rem;
  color: #FFFFFF;
  margin: 0;
  opacity: 0.9;
}


/* Правая часть с формой */
.register-right {
  width: 70%;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow: hidden;
}

.register-form-container {
  width: 100%;
  max-width: 420px;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1a1a1a;
  text-align: center;
  margin: 0 0 0.5rem 0;
}

.login-link-text {
  text-align: center;
  color: #666666;
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
}

.login-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

/* Social Login Buttons */
.social-login {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.social-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #FFFFFF;
  color: #1a1a1a;
  cursor: pointer;
  transition: all 0.2s ease;
}

.social-button:hover {
  border-color: #c0c0c0;
  background: #fafafa;
}

.social-button svg {
  flex-shrink: 0;
}

/* Divider */
.divider {
  position: relative;
  text-align: center;
  margin: 1rem 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e0e0e0;
}

.divider-text {
  position: relative;
  background: #FFFFFF;
  padding: 0 0.75rem;
  font-size: 0.75rem;
  color: #999999;
}

.status-text {
  font-size: 0.875rem;
  margin: 0.5rem 0 1rem 0;
  text-align: center;
}

.status-text.error {
  color: #e11d48;
}

/* Форма */
.register-form {
  width: 100%;
}

.name-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.form-group {
  margin-bottom: 0.75rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #FFFFFF;
  color: #1a1a1a;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-input::placeholder {
  color: #999999;
}

.input-hint {
  font-size: 0.75rem;
  color: #999999;
  margin: 0.25rem 0 0 0;
}

/* Кнопка Join */
.join-button {
  width: 100%;
  padding: 0.75rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #FFFFFF;
  background: linear-gradient(to bottom, #1a1a1a, #000000);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-top: 0.25rem;
  margin-bottom: 0.75rem;
}

.join-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.join-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.join-button:active {
  transform: translateY(0);
}

/* Текст про Terms */
.terms-text {
  font-size: 0.75rem;
  color: #666666;
  text-align: center;
  margin: 0;
  line-height: 1.5;
}

/* Адаптивность */
@media (max-width: 968px) {
  .register-page {
    flex-direction: column;
    height: auto;
    min-height: 100vh;
  }

  .register-left {
    width: 100%;
    min-height: 45vh;
    height: 45vh;
  }

  .register-right {
    width: 100%;
    padding: 3rem 1.5rem;
    min-height: auto;
  }

  .register-form-container {
    max-width: 500px;
    margin: 0 auto;
  }

  .overlay-title {
    font-size: 2.5rem;
  }

  .overlay-subtitle {
    font-size: 1.1rem;
  }

  .text-overlay {
    width: 90%;
    max-width: 600px;
  }

  .logo-overlay {
    top: 1.5rem;
    left: 1.5rem;
  }

  .logo-link {
    font-size: 1.4rem;
  }

  .attribution-overlay {
    bottom: 1rem;
    left: 1rem;
  }

  .attribution-text {
    font-size: 0.8rem;
  }

  .form-title {
    font-size: 1.75rem;
  }

  .login-link-text {
    font-size: 0.8125rem;
  }
}

@media (max-width: 768px) {
  .register-left {
    min-height: 40vh;
    height: 40vh;
  }

  .register-right {
    padding: 2.5rem 1.5rem;
  }

  .overlay-title {
    font-size: 2.2rem;
    margin-bottom: 0.75rem;
  }

  .overlay-subtitle {
    font-size: 1rem;
  }

  .text-overlay {
    width: 85%;
    padding: 0 1rem;
  }

  .form-title {
    font-size: 1.625rem;
  }

  .social-button {
    padding: 0.6875rem 1rem;
    font-size: 0.8125rem;
  }

  .form-input {
    padding: 0.6875rem 0.9375rem;
    font-size: 0.9375rem;
  }

  .join-button {
    padding: 0.6875rem;
    font-size: 0.9375rem;
  }
}

@media (max-width: 640px) {
  .register-left {
    min-height: 35vh;
    height: 35vh;
  }

  .register-right {
    padding: 2rem 1rem;
  }

  .text-overlay {
    width: 90%;
    padding: 0 0.75rem;
  }
  
  .attribution-overlay {
    bottom: 0.75rem;
    left: 0.75rem;
  }

  .attribution-text {
    font-size: 0.7rem;
  }

  .logo-overlay {
    top: 1rem;
    left: 1rem;
  }

  .logo-link {
    font-size: 1.25rem;
  }

  .overlay-title {
    font-size: 1.875rem;
    margin-bottom: 0.5rem;
  }

  .overlay-subtitle {
    font-size: 0.875rem;
    line-height: 1.5;
  }

  .form-title {
    font-size: 1.5rem;
    margin-bottom: 0.375rem;
  }

  .login-link-text {
    font-size: 0.75rem;
    margin-bottom: 0.875rem;
  }

  .social-login {
    gap: 0.625rem;
    margin-bottom: 0.875rem;
  }

  .social-button {
    padding: 0.625rem 0.875rem;
    font-size: 0.75rem;
  }

  .divider {
    margin: 0.875rem 0;
  }

  .divider-text {
    font-size: 0.7rem;
  }

  .name-row {
    grid-template-columns: 1fr;
    gap: 0.625rem;
    margin-bottom: 0.625rem;
  }

  .form-group {
    margin-bottom: 0.625rem;
  }

  .form-input {
    padding: 0.625rem 0.875rem;
    font-size: 0.875rem;
  }

  .input-hint {
    font-size: 0.7rem;
    margin-top: 0.2rem;
  }

  .join-button {
    padding: 0.625rem;
    font-size: 0.875rem;
    margin-top: 0.5rem;
    margin-bottom: 0.625rem;
  }

  .terms-text {
    font-size: 0.7rem;
    line-height: 1.4;
  }

  .register-form-container {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .register-left {
    min-height: 30vh;
    height: 30vh;
  }

  .register-right {
    padding: 1.5rem 0.75rem;
  }

  .overlay-title {
    font-size: 1.625rem;
  }

  .overlay-subtitle {
    font-size: 0.8125rem;
  }

  .logo-link {
    font-size: 1.125rem;
  }

  .attribution-text {
    font-size: 0.65rem;
  }

  .form-title {
    font-size: 1.375rem;
  }

  .social-button {
    font-size: 0.7rem;
    padding: 0.5625rem 0.75rem;
  }

  .social-button svg {
    width: 16px;
    height: 16px;
  }

  .form-input {
    padding: 0.5625rem 0.75rem;
    font-size: 0.8125rem;
  }
}
</style>
