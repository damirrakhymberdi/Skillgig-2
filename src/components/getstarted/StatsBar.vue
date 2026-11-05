<template>
  <div class="stats-bar">
    <div v-if="loading" class="container stats-status" aria-live="polite">
      Loading platform stats...
    </div>
    <div v-else-if="statsError" class="container stats-status stats-error" role="status">
      {{ statsError }}
    </div>
    <div v-else class="container stats-content">
      <span class="stat-item">
        <strong>{{ stats.totalQuestions.toLocaleString() }}</strong> questions asked
      </span>
      <span class="separator">•</span>
      <span class="stat-item">
        <strong>{{ stats.totalExperts }}</strong> IT specialists
      </span>
      <span class="separator">•</span>
      <span class="stat-item">
        <strong>{{ stats.successRate }}%</strong> questions resolved
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchPlatformStats } from '@/services/statsService'

const stats = ref({
  totalQuestions: 0,
  totalExperts: 0,
  successRate: 0
})

const loading = ref(false)
const statsError = ref('')

const loadStats = async () => {
  loading.value = true
  statsError.value = ''
  try {
    stats.value = await fetchPlatformStats()
  } catch (error) {
    console.error('Error loading stats:', error)
    statsError.value = 'Platform stats are unavailable until the backend is running.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.stats-bar {
  background-color: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 1rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.stats-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  font-size: 0.95rem;
  color: #6b7280;
}

.stats-status {
  text-align: center;
  color: #6b7280;
  font-size: 0.9rem;
}

.stats-error {
  color: #8b5a19;
}

.stat-item strong {
  color: #111827;
  font-weight: 600;
}

.separator {
  color: #d1d5db;
}

@media (max-width: 768px) {
  .stats-content {
    flex-direction: column;
    gap: 0.5rem;
  }

  .separator {
    display: none;
  }
}
</style>
