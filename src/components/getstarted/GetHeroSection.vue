<template>
  <section class="hero-section">
    <div class="hero-overlay"></div>
    <div class="container">
      <div class="hero-inner centered">
        <div class="hero-copy">
          <h1 class="hero-title">Find any IT questions</h1>
          <p class="hero-subtitle">
            Discover and explore tech questions from developers like you.
          </p>
        </div>
        <form class="hero-actions" role="search" @submit.prevent="handleSearch">
          <div class="search-box">
            <input
              v-model="searchQuery"
              type="search"
              placeholder="Search IT questions"
              aria-label="Search IT questions"
            >
          </div>
          <button type="submit" class="search-button" :disabled="!searchQuery.trim()">
            Search
          </button>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  const search = searchQuery.value.trim()
  if (search) {
    router.push({ 
      path: '/questions',
      query: { search }
    })
  }
}
</script>

<style scoped>
.hero-section {
  position: relative;
  color: white;
  padding: 8rem 1.5rem 3rem;
  margin-top: 0;
  overflow: hidden;
  background-image: linear-gradient(120deg, rgba(0,0,0,0.65), rgba(0,0,0,0.35)), url('@/assets/images/Hero Section.png');
  background-size: cover;
  background-position: center;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.08), transparent 35%),
              radial-gradient(circle at 80% 0%, rgba(255,255,255,0.1), transparent 30%);
  pointer-events: none;
}

.container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  z-index: 1;
}

.hero-inner {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  align-items: center;
  justify-items: center;
}

.hero-inner.centered .hero-copy {
  text-align: center;
}

.eyebrow {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 999px;
  font-size: 0.9rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  line-height: 1.25;
}

.hero-subtitle {
  font-size: 1.4rem;
  opacity: 0.9;
  margin-bottom: 1.75rem;
  max-width: 560px;
}

.hero-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.search-box {
  position: relative;
  width: 100%;
  max-width: 560px;
}

.search-box input {
  width: 100%;
  padding: 0.95rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  font-size: 1rem;
  outline: none;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  backdrop-filter: blur(6px);
}

.search-box input::placeholder {
  color: #e5e7eb;
}

.search-button {
  border: 0;
  border-radius: 10px;
  padding: 0.95rem 1.4rem;
  background: #42b883;
  color: #10281c;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.search-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.search-box input:focus-visible,
.search-button:focus-visible {
  outline: 3px solid #fff;
  outline-offset: 3px;
}

@media (max-width: 900px) {
  .hero-inner {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-actions {
    flex-direction: column;
  }

  .search-box,
  .search-button {
    width: 100%;
  }
  .hero-title {
    font-size: 1.9rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .hero-section {
    padding: 4rem 1rem 3rem;
  }
}
</style>

