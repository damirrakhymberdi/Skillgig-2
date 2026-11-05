<template>
  <section class="who-section">
    <div class="background-image" :style="{ backgroundImage: `url(${heroImage3})` }">
      <div class="content-overlay">
      <!-- Правый верхний блок - For experts -->
      <div class="text-block top-right">
        <h3 class="block-title">For experts</h3>
        <p class="block-subtitle">Want to:</p>
        <ul class="block-list">
          <li>Build portfolio</li>
          <li>Gain experience</li>
          <li>Help community</li>
          <li>Build a reputation through resolved questions</li>
          <li>Learn by teaching</li>
        </ul>
      </div>

      <!-- Левый нижний блок - For clients -->
      <div class="text-block bottom-left">
        <h3 class="block-title">For clients</h3>
        <p class="block-subtitle">Need help with:</p>
        <ul class="block-list">
          <li>Web bugs</li>
          <li>Mobile issues</li>
          <li>Design questions</li>
          <li>Backend problems</li>
          <li>DevOps setup</li>
        </ul>
      </div>
    </div>
    </div>
  </section>
</template>

<script setup>
// Импорт изображения
import heroImage3 from '@/assets/images/damirrn.png'

</script>

<style scoped>
.who-section {
  width: 100%;
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-family: Arial, Helvetica, sans-serif;
  background-color: #F5F7FA;
}

.background-image {
  position: relative;
  width: 95%;
  height: 90vh;
  max-width: 1500px;
  margin: 0 auto;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: 3rem 3rem;
  z-index: 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 0rem;
  pointer-events: none;
}

.content-overlay > * {
  pointer-events: all;
}

.text-block {
  background: transparent;
  padding: 0rem;
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.top-right {
  grid-column: 2;
  grid-row: 1;
  align-self: start;
  justify-self: end;
  max-width: 450px;
  text-align: end;
}

.bottom-left {
  grid-column: 1;
  grid-row: 2;
  align-self: end;
  justify-self: start;
  max-width: 450px;
}

.block-title {
  font-size: 2rem;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0;
  line-height: 1;
}

.block-subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  color: #FFFFFF;
  margin: 0;
}

.block-list {
  list-style: none;
  padding: 0;
  margin: 0;
  color: #FFFFFF;
  font-size: 1rem;
  line-height: 1.3;
}

.block-list li {
  margin-bottom: 0.2rem;
  padding-left: 0;
}

.block-button {
  background: transparent;
  color: #FFFFFF;
  border: none;
  padding: 0.8rem 1.5rem;
  font-weight: 600;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  margin-top: 0.2rem;
  font-family: Arial, Helvetica, sans-serif;
  text-shadow: 0 0 0 rgba(255, 255, 255, 0);
}

.top-right .block-button {
  align-self: flex-end;
}

.bottom-left .block-button {
  align-self: flex-start;
}

.block-button:hover {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 
               0 0 20px rgba(255, 255, 255, 0.6),
               0 0 30px rgba(255, 255, 255, 0.4);
}

/* Адаптивность */
@media (max-width: 968px) {
  .content-overlay {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
    gap: 1rem;
  }

  .top-right {
    grid-column: 1;
    grid-row: 1;
    align-self: start;
    justify-self: center;
    max-width: 100%;
    text-align: center;
  }

  .bottom-left {
    grid-column: 1;
    grid-row: 2;
    align-self: start;
    justify-self: center;
    max-width: 100%;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .content-overlay {
    padding: 3rem 1.5rem;
  }

  .text-block {
    padding: 1.5rem;
    text-align: center;
  }

  .top-right {
    text-align: center;
  }

  .bottom-left {
    text-align: center;
  }

  .block-title {
    font-size: 2.5rem;
  }

  .block-subtitle {
    font-size: 1.6rem;
  }

  .block-list {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .who-section {
    min-height: 500px;
  }

  .content-overlay {
    padding: 2rem 1rem;
    gap: 1rem;
  }

  .text-block {
    padding: 1.25rem;
  }

  .block-title {
    font-size: 2.5rem;
  }

  .block-subtitle {
    font-size: 1.6rem;
  }

  .block-list {
    font-size: 1.1rem;
  }
}
</style>
