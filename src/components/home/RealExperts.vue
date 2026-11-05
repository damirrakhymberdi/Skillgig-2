<template>
  <section class="real-experts-section">
    <div class="section-container">
      <div class="section-content">
        <div class="text-content">
          <h2 class="main-title">
            <span class="purple-text">Get</span> IT Help<br>
            <span class="purple-text">from</span> Real Experts
          </h2>
          <p class="subtitle">
            Get practical help from the community and share what you know.
          </p>
        </div>

        <p v-if="loading" class="stats-message" aria-live="polite">
          Loading live platform stats…
        </p>
        <p v-else-if="statsError" class="stats-message stats-error" role="status">
          Live platform stats are unavailable while the backend is offline.
        </p>
        <div v-else class="stats-grid">
          <div class="stat-item">
            <img src="@/assets/images/logos/Vector (7).png" alt="Questions asked" class="stat-icon">
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalQuestions.toLocaleString() }}</div>
              <div class="stat-label">Questions asked</div>
            </div>
          </div>
          
          <div class="stat-item">
            <img src="@/assets/images/logos/Vector (8).png" alt="Active experts" class="stat-icon">
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalExperts.toLocaleString() }}</div>
              <div class="stat-label">Expert profiles</div>
            </div>
          </div>
          
          <div class="stat-item">
            <img src="@/assets/images/logos/Vector (9).png" alt="Resolved question rate" class="stat-icon">
            <div class="stat-content">
              <div class="stat-number">{{ stats.successRate }}%</div>
              <div class="stat-label">Questions resolved</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { fetchPlatformStats } from '@/services/statsService'

const stats = ref({ totalQuestions: 0, totalExperts: 0, successRate: 0 })
const loading = ref(true)
const statsError = ref(false)

onMounted(async () => {
  try {
    stats.value = await fetchPlatformStats()
  } catch (error) {
    console.error('Could not load live platform stats:', error)
    statsError.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.real-experts-section {
  width: 100%;
  position: relative;
  background-color: #F5F7FA;
  padding: 2rem 0rem;
  min-height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Arial, Helvetica, sans-serif;
}

.section-container {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 0 5rem;
  position: relative;
}

.section-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.text-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.main-title {
  font-size: 2.7rem;
  font-weight: 700;
  color: #111111;
  margin: 0;
  line-height: 1.2;
  width: 90%;
}

.main-title .purple-text {
  color: #4CAF4F;
}

.subtitle {
  font-size: 1.25rem;
  font-weight: 400;
  color: #4CAF4F;
  margin: 0;
  line-height: 1.4;
}

.subtitle-break {
  display: none;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.4rem;
  width: 100%;
  justify-items: center;
}

.stats-message {
  align-self: center;
  color: #52645a;
  font-size: 1rem;
  line-height: 1.6;
}

.stats-error {
  color: #8b5a19;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: transparent;
}

.stat-icon {
  width: 48px;
  height: 48px;
  object-fit: contain;
  flex-shrink: 0;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  flex: 1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #111111;
  line-height: 1;
}

.stat-label {
  font-size: 1rem;
  font-weight: 400;
  color: #4D4D4D;
  line-height: 1.4;
}

/* Адаптивность */
@media (max-width: 968px) {
  .section-content {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .text-content {
    order: 1;
    text-align: center;
  }

  .stats-grid {
    order: 2;
  }

  .main-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .section-container {
    padding: 0 5rem;
  }

  .real-experts-section {
    padding: 3rem 0;
  }

  .section-content {
    gap: 2rem;
  }

  .main-title {
    font-size: 2.5rem;
  }

  .subtitle {
    font-size: 1.1rem;
    margin-right: 40px;
  }

  .subtitle-break {
    display: inline;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    justify-items: center;
  }

  .stat-item {
    justify-content: center;
    max-width: 300px;
    width: 50%;
  }

  .stat-number {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .section-container {
    padding: 0 0rem;
  }

  .real-experts-section {
    padding: 3rem 0;
  }

  .main-title {
    font-size: 2.45rem;
    margin-left: 10px;
  }

  .subtitle {
    font-size: 1rem;
    margin-left: 10px;
  }

  .stat-item {
    padding: 1rem;
  }

  .stat-number {
    font-size: 1.75rem;
  }

  .stat-label {
    font-size: 0.9rem;
  }
}
</style>

