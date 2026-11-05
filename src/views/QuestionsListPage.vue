<template>
  <div class="questions-list-page">
    <div class="main-content">
      <div class="container">
        <div class="stats-wrapper">
          <StatsBar />
        </div>

        <div class="header-card">
          <div class="section-header">
            <h1>All questions</h1>
            <div class="search-inline">
              <svg class="search-icon" width="18" height="18" viewBox="0 0 20 20" fill="none">
                <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM19 19l-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Search questions..."
                @keyup.enter="handleSearch"
              />
            </div>
            <div class="header-actions">
              <div class="header-filters"> 
                <select v-model="sortBy" class="filter-select" @change="handleSortSelect">
                  <option value="newest">Newest</option>
                  <option value="oldest">Oldest</option>
                  <option value="most-answered">Most answers</option>
                  <option value="least-answered">Fewest answers</option>
                </select>
              </div>
              <button class="btn-ask-question" @click="handleAskQuestion">
                Ask Question
              </button>
            </div>
          </div>
        </div>

        <div class="content-grid">
          <div class="sidebar-sticky">
            <CategoriesSidebar
              @change="handleCategoryChange"
            />
          </div>

          <main class="questions-section">
            <div class="questions-scroll">
            <QuestionsList
              :hide-filters="true"
              :external-sort="sortBy"
              :category="selectedCategory"
              :search-query="searchQuery"
              @update:sort="handleSortSelect"
            />
            </div>
          </main>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CategoriesSidebar from '@/components/getstarted/CategoriesSidebar.vue'
import QuestionsList from '@/components/getstarted/QuestionsList.vue'
import StatsBar from '@/components/getstarted/StatsBar.vue'

const router = useRouter()
const route = useRoute()
const sortBy = ref('newest')
const searchQuery = ref(
  Array.isArray(route.query.search)
    ? route.query.search[0] || ''
    : route.query.search || ''
)
const selectedCategory = ref(
  Array.isArray(route.query.category)
    ? route.query.category[0] || ''
    : route.query.category || ''
)

watch(
  () => route.query.search,
  (value) => {
    searchQuery.value = Array.isArray(value) ? value[0] || '' : value || ''
  }
)

watch(
  () => route.query.category,
  (value) => {
    selectedCategory.value = Array.isArray(value) ? value[0] || '' : value || ''
  }
)

const handleAskQuestion = () => {
  router.push('/ask')
}

const handleSearch = () => {
  const search = searchQuery.value.trim()
  router.push({
    path: '/questions',
    query: { ...route.query, search: search || undefined }
  })
}

const handleSortSelect = (eventOrValue) => {
  const value = typeof eventOrValue === 'string' ? eventOrValue : eventOrValue?.target?.value
  if (value) {
    sortBy.value = value
  }
}

const handleCategoryChange = (val) => {
  selectedCategory.value = val || ''
}
</script>

<style scoped>
.questions-list-page {
  min-height: 100vh;
  background-color: #f6f8f6;
  padding: 88px 1.25rem 2rem;
}

.main-content {
  padding: 0 0 2rem;
}

.container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0;
}

.stats-wrapper {
  padding: 0 0 1rem;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(230px, 280px) minmax(0, 1fr);
  gap: 1rem;
  align-items: start;
}

.questions-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.questions-scroll {
  max-height: none;
  overflow: visible;
  padding: 0;
}

.header-card {
  background: white;
  border: 1px solid #e5eae6;
  border-radius: 14px;
  padding: 0.85rem 1.15rem;
  margin-bottom: 1rem;
  position: sticky;
  top: 78px;
  z-index: 5;
  box-shadow: 0 8px 24px rgba(26, 42, 31, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-inline {
  position: relative;
  flex: 1 1 320px;
  max-width: 420px;
}

.search-inline input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #111827;
  background: #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.search-inline input::placeholder {
  color: #9ca3af;
}

.search-inline .search-icon {
  position: absolute;
  left: 0.9rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  pointer-events: none;
}

.header-filters {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hero-inline {
  max-width: 420px;
  width: 100%;
  flex: 1 1 320px;
}

.hero-inline :deep(.hero-section) {
  padding: 0;
  margin: 0;
}

.hero-inline :deep(.container) {
  max-width: none;
  padding: 0;
}

.hero-inline :deep(.hero-inner) {
  justify-items: center;
}

.hero-inline :deep(.hero-title) {
  font-size: 1.6rem;
}

.sidebar-sticky {
  position: sticky;
  top: 96px;
  align-self: start;
}

.filter-label {
  font-size: 0.9rem;
  color: #374151;
  font-weight: 600;
  white-space: nowrap;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.btn-ask-question {
  padding: 0.75rem 1.5rem;
  background-color: #16834b;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.btn-ask-question:hover {
  background-color: #116b3d;
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.25);
}

/* Фильтрлер */
.filters-bar {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

.filter-select {
  padding: .75rem 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 0.875rem;
  color: #111827;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
}

/* Сұрақтар тізімі */
.loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  color: #6b7280;
}

.empty-state p {
  font-size: 1rem;
  margin-bottom: 1rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.sentinel {
  height: 1px;
  width: 100%;
}

.sentinel.is-loading {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .questions-list-page {
    padding: 82px 0.875rem 1.5rem;
  }

  .content-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .header-card {
    top: 70px;
    margin: 0 0 0.75rem;
    padding: 0.9rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-inline {
    flex: none;
    width: 100%;
    max-width: none;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem 0.75rem;
  }

  .btn-ask-question {
    width: 100%;
  }
}

</style>

