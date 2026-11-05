<template>
  <div class="questions-list-wrapper">
    <div class="filters-bar" v-if="!hideFilters && !loading && !errorMessage">
      <div class="filter-group">
        <label>Sort by:</label>
        <select v-model="sortBy" class="filter-select" @change="handleSortChange">
          <option value="newest">Newest</option>
          <option value="oldest">Oldest</option>
          <option value="most-answered">Most answers</option>
          <option value="least-answered">Fewest answers</option>
        </select>
      </div>
    </div>

    <div v-if="loading && questions.length === 0" class="loading">
      Loading...
    </div>
    
    <div v-else-if="errorMessage" class="error-state">
      <p>{{ errorMessage }}</p>
      <button class="retry-btn" @click="reload">Retry</button>
    </div>
    
    <div v-else class="questions-section">
      <div class="questions-list">
        <QuestionCard
          v-for="question in questions"
          :key="question.id"
          :question="question"
        />
        <div v-if="questions.length === 0" class="empty-state">
          <p>No questions yet</p>
        </div>
      </div>
      <div
        v-if="hasMore"
        ref="sentinel"
        class="sentinel"
        :class="{ 'is-loading': loading }"
      >
        {{ loading ? 'Loading...' : '' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import QuestionCard from '@/components/getstarted/QuestionCard.vue'
import { fetchQuestions } from '@/services/questionsService'

const props = defineProps({
  hideFilters: {
    type: Boolean,
    default: false
  },
  externalSort: {
    type: String,
    default: ''
  },
  maxItems: {
    type: Number,
    default: null
  },
  category: {
    type: String,
    default: ''
  },
  searchQuery: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:sort'])

const loading = ref(false)
const questions = ref([])
const errorMessage = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const hasMore = ref(true)
const sentinel = ref(null)
let observer = null
let reloadQueued = false
const sortBy = ref(props.externalSort || 'newest')
const PAGE_SIZE = 5

const disconnectObserver = () => {
  if (observer) {
    observer.disconnect()
    observer = null
  }
}

const sortItems = (items) => {
  const sorted = [...items]
  switch (sortBy.value) {
    case 'oldest':
      sorted.sort(
        (a, b) =>
          new Date(a.createdAt || a.created_at || 0) -
          new Date(b.createdAt || b.created_at || 0)
      )
      break
    case 'most-answered':
      sorted.sort(
        (a, b) =>
          (b.answersCount ?? b.answers_count ?? 0) -
          (a.answersCount ?? a.answers_count ?? 0)
      )
      break
    case 'least-answered':
      sorted.sort(
        (a, b) =>
          (a.answersCount ?? a.answers_count ?? 0) -
          (b.answersCount ?? b.answers_count ?? 0)
      )
      break
    case 'newest':
    default:
      sorted.sort(
        (b, a) =>
          new Date(a.createdAt || a.created_at || 0) -
          new Date(b.createdAt || b.created_at || 0)
      )
      break
  }
  return sorted
}

const loadQuestions = async (append = false) => {
  if (loading.value) {
    if (!append) reloadQueued = true
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    const offset = (currentPage.value - 1) * PAGE_SIZE
    const response = await fetchQuestions({
      limit: PAGE_SIZE,
      offset,
      status: 'published',
      category: props.category || undefined,
      search: props.searchQuery.trim() || undefined,
      sortBy: sortBy.value
    })

    let items = Array.isArray(response.items) ? response.items : []
    items = sortItems(items)

    if (append) {
      questions.value = [...questions.value, ...items]
    } else {
      questions.value = items
    }

    if (props.maxItems) {
      const limit = props.maxItems
      if (questions.value.length >= limit) {
        questions.value = questions.value.slice(0, limit)
        hasMore.value = false
        disconnectObserver()
      }
    }

    const backendTotal = response.total
    const computedTotal = append
      ? questions.value.length + items.length
      : items.length
    const total = backendTotal ?? computedTotal
    totalPages.value = Math.max(1, Math.ceil(total / PAGE_SIZE))

    // If backendTotal is unknown, assume there might be more when we received a full page
    const pageFilled = items.length === PAGE_SIZE
    hasMore.value = backendTotal != null
      ? questions.value.length < total
      : pageFilled
  } catch (error) {
    console.error('Сұрақтарды жүктеу қатесі:', error)
    if (!append) {
      questions.value = []
    }
    errorMessage.value = error?.status
      ? 'Сұрақтарды жүктеу мүмкін болмады. Қайта көріңіз.'
      : 'Серверге қосыла алмадық. Backend іске қосулы екенін тексеріп, қайта көріңіз.'
  } finally {
    loading.value = false
    if (reloadQueued) {
      reloadQueued = false
      currentPage.value = 1
      hasMore.value = true
      loadQuestions(false)
    }
  }
}

const loadMore = () => {
  if (!hasMore.value || loading.value) return
  currentPage.value += 1
  loadQuestions(true)
}

const reload = () => {
  currentPage.value = 1
  hasMore.value = true
  loadQuestions(false)
}

const handleSortChange = () => {
  currentPage.value = 1
  emit('update:sort', sortBy.value)
  hasMore.value = true
  loadQuestions(false)
}

watch(
  () => props.externalSort,
  (val) => {
    if (val && val !== sortBy.value) {
      sortBy.value = val
      currentPage.value = 1
      hasMore.value = true
      loadQuestions(false)
    }
  }
)

watch(
  () => props.category,
  () => {
    currentPage.value = 1
    hasMore.value = true
    loadQuestions(false)
  }
)

watch(
  () => props.searchQuery,
  () => {
    currentPage.value = 1
    hasMore.value = true
    loadQuestions(false)
  }
)

const initObserver = () => {
  disconnectObserver()
  if (!sentinel.value) return
  observer = new IntersectionObserver(
    (entries) => {
      const first = entries[0]
      if (first && first.isIntersecting) {
        loadMore()
      }
    },
    {
      root: null,
      rootMargin: '200px 0px 200px 0px',
      threshold: 0.1
    }
  )
  observer.observe(sentinel.value)
}

onMounted(() => {
  loadQuestions(false).then(() => {
    initObserver()
  })
})

onBeforeUnmount(() => {
  disconnectObserver()
})
</script>

<style scoped>
.questions-list-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.filters-bar {
  display: flex;
  justify-content: flex-end;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-select {
  padding: 0.45rem 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0px;
  background-color: white;
  font-size: 0.9rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.questions-section {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.empty-state p {
  font-size: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
}

.page-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background-color: white;
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn:not(:disabled):hover {
  background-color: #f3f4f6;
  border-color: #d1d5db;
}

.page-indicator {
  font-weight: 600;
  color: #4b5563;
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

.error-state {
  padding: 2rem;
  text-align: center;
  color: #b91c1c;
  background-color: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 10px;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  border: none;
  background-color: #4caf4f;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: #43a047;
}
</style>

