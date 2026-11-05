<template>
  <section class="what-skill-section">
    <div class="section-border-top"></div>
    <div class="section-border-bottom"></div>
    
    <div class="section-container">
      <div class="section-content">
        <div class="illustration-wrapper">
          <img src="@/assets/images/Frame 35.png" alt="SkillGig illustration" class="illustration-img">
        </div>
        
        <div class="text-content">
          <h2 class="section-title">What is SkillGig</h2>
          <p class="intro-text">SkillGig is a platform where people can get help with any IT problem.</p>
          <p class="description-text">
            It connects two groups: <strong>Clients</strong> - people who have issues in their IT projects (web, mobile, design, backend, DevOps, etc.). <strong>IT specialists</strong> - developers and designers who can share possible solutions. The goal is to help people work through IT project issues and create a place for knowledge sharing and mutual support.
          </p>
          <RouterLink to="/about" class="learn-more-btn">Learn More</RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.what-skill-section {
  width: 100%;
  position: relative;
  background-color: #FFFFFF;
  padding: 0;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-family: Arial, Helvetica, sans-serif;
}

/* Тонкие зеленые полоски сверху и снизу */
.section-border-top,
.section-border-bottom {
  display: none;
}

.section-container {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 1rem 5rem;
  position: relative;
  z-index: 2;
}

.section-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
}

.illustration-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 4rem;
}

.illustration-img {
  width: 80%;
  max-width: 500px;
  height: auto;
  object-fit: contain;
}

.text-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 700;
  color: #111111;
  margin: 0;
  line-height: 1.2;
}

.intro-text {
  font-size: 1.25rem;
  font-weight: 400;
  color: #111111;
  margin: 0;
  line-height: 1.4;
}

.description-text {
  font-size: 1rem;
  font-weight: 400;
  color: #111111;
  margin: 0;
  line-height: 1.5;
}

.description-text strong {
  font-weight: 600;
  color: #111111;
}

.learn-more-btn {
  display: inline-block;
  padding: 0.75rem 2.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  border-radius: 8px;
  background-color: #4CAF4F;
  color: #FFFFFF;
  text-decoration: none;
  transition: all 0.3s ease;
  align-self: flex-start;
  margin-top: 1rem;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  font-family: Arial, Helvetica, sans-serif;
}

.learn-more-btn:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

/* Адаптивность */
@media (max-width: 968px) {
  .section-content {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .illustration-wrapper {
    order: 1;
  }

  .text-content {
    order: 2;
  }

  .section-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .section-container {
    padding: 3rem 1.5rem;
  }

  .section-content {
    gap: 2rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .intro-text {
    font-size: 1.1rem;
  }

  .description-text {
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .section-container {
    padding: 2rem 1rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .intro-text {
    font-size: 1rem;
  }

  .description-text {
    font-size: 0.9rem;
  }

  .learn-more-btn {
    padding: 0.875rem 2rem;
    font-size: 1rem;
    width: 100%;
    text-align: center;
  }
}
</style>

