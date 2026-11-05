<template>
  <footer class="main-footer">
    <div class="footer-container">
      <div class="footer-top">
        <div class="footer-left">
          <h1 class="footer-logo">SkillGig</h1>
        </div>

        <div class="footer-right">
          <div class="footer-company">
            <h4 class="footer-section-title">Company</h4>
            <nav class="footer-links">
              <RouterLink to="/" class="footer-link">Home</RouterLink>
              <RouterLink to="/about" class="footer-link">About</RouterLink>
              <RouterLink to="/faq" class="footer-link">FAQ</RouterLink>
              <RouterLink to="/get-started" class="footer-link">Get Started</RouterLink>
            </nav>
          </div>

          <div class="footer-contact-section">
            <h4 class="footer-section-title">Contact</h4>
            <div class="footer-contact-info">
              <p class="footer-contact-item">
                <span class="contact-label">Phone:</span>
                <a href="tel:87766031092" class="contact-link">8776 603 10 92</a>
              </p>
              <p class="footer-contact-item">
                <span class="contact-label">Email:</span>
                <a href="mailto:damirrakhymberdi662@gmail.com" class="contact-link">damirrakhymberdi662@gmail.com</a>
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p class="footer-copyright">© {{ currentYear }} SkillGig. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const currentYear = new Date().getFullYear()
</script>

<style scoped>
.main-footer {
  background: #000000;
  color: #fff;
  margin: 0;
  padding-top: 4rem;
  padding-bottom: 2rem;
  font-family: Arial, Helvetica, sans-serif;
}

.footer-container {
  max-width: 1350px;
  margin: 0 auto;
  padding: 0 3rem;
}

.footer-top {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 6rem;
  margin-bottom: 3rem;
  align-items: start;
}

.footer-left {
  display: flex;
  flex-direction: column;
}

.footer-logo {
  font-size: 48px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
  margin: 0;
}

.footer-right {
  display: flex;
  gap: 5rem;
  justify-content: space-between;
  align-items: start;
}

.footer-company {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
}

.footer-section-title {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin: 0;
  margin-bottom: 0.5rem;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-link {
  font-size: 16px;
  color: #cccccc;
  text-decoration: none;
  transition: color 0.3s ease;
  line-height: 1.5;
}

.footer-link:hover {
  color: #fff;
}

.footer-contact-section {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  flex: 1;
}

.footer-contact-info {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.footer-contact-item {
  font-size: 16px;
  color: #cccccc;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  line-height: 1.5;
}

.contact-label {
  font-weight: 700;
  color: #fff;
  font-size: 16px;
}

.contact-link {
  color: #cccccc;
  text-decoration: none;
  transition: color 0.3s ease;
}

.contact-link:hover {
  color: #fff;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  padding-top: 2rem;
  text-align: center;
  margin-top: 1rem;
}

.footer-copyright {
  font-size: 14px;
  color: #999999;
  margin: 0;
}

/* Адаптивность */
@media (max-width: 968px) {
  .footer-top {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .footer-right {
    justify-content: flex-start;
    gap: 4rem;
  }
}

@media (max-width: 768px) {
  .main-footer {
    padding-top: 3rem;
    padding-bottom: 1.5rem;
  }

  .footer-container {
    padding: 0 2rem;
  }

  .footer-top {
    gap: 2.5rem;
  }

  .footer-right {
    flex-direction: column;
    gap: 2.5rem;
  }

  .footer-logo {
    font-size: 40px;
  }

  .footer-section-title {
    font-size: 18px;
  }

  .footer-link,
  .footer-contact-item {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .main-footer {
    padding-top: 2.5rem;
    padding-bottom: 1.5rem;
  }

  .footer-container {
    padding: 0 1.5rem;
  }

  .footer-top {
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .footer-right {
    gap: 2rem;
  }

  .footer-logo {
    font-size: 36px;
  }

  .footer-company {
    gap: 1.25rem;
  }

  .footer-contact-section {
    gap: 1.5rem;
  }

  .footer-contact-info {
    gap: 1rem;
  }

  .footer-bottom {
    padding-top: 1.5rem;
  }

  .footer-copyright {
    font-size: 13px;
  }
}
</style>
