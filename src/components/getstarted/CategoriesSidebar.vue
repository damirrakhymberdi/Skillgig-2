<template>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="categories-widget">
        <h3>Categories</h3>
        <div class="select-wrapper">
          <select
            v-model="selectedCategory"
            class="category-select"
            @change="handleCategoryChange"
            :disabled="categoriesLoading && categories.length === 0"
          >
            <option value="">All categories</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.name"
            >
              {{ category.icon }} {{ category.name }}
            </option>
          </select>
          <span class="select-caret">▾</span>
        </div>
      </div>

      <div class="my-blocks">
        <button class="my-box" @click="goToMyQuestions">
          <span class="box-label">My questions</span>
        </button>
        <button class="my-box" @click="goToMyAnswers">
          <span class="box-label">My answers</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchCategories } from '@/services/categoryService'

const props = defineProps({
  disableNavigation: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['change'])

const router = useRouter()
const route = useRoute()

const selectedCategory = ref(route.query.category ?? '')

const fallbackCategories = [
  { id: 'web', name: 'Web Development', icon: '🌐' },
  { id: 'mobile', name: 'Mobile Development', icon: '📱' },
  { id: 'uiux', name: 'UI/UX Design', icon: '🎨' },
  { id: 'backend', name: 'Backend/Database', icon: '💾' },
  { id: 'ai_ml', name: 'AI/ML', icon: '🤖' },
  { id: 'devops', name: 'DevOps', icon: '🔧' },
  { id: 'gamedev', name: 'Game Development', icon: '🎮' },
  { id: 'security', name: 'Security/Blockchain', icon: '🔐' }
]

const categories = ref([...fallbackCategories])
const categoriesLoading = ref(false)
const loadCategories = async () => {
  categoriesLoading.value = true
  try {
    const remoteCategories = await fetchCategories()
    if (remoteCategories.length) {
      categories.value = remoteCategories.map((category) => ({
        ...category,
        icon: category.icon || fallbackCategories.find(
          (fallback) =>
            fallback.name.toLowerCase() === category.name?.toLowerCase()
        )?.icon || '📁'
      }))
    } else {
      categories.value = [...fallbackCategories]
    }
  } catch (error) {
    console.error('Error loading categories:', error)
    categories.value = [...fallbackCategories]
  } finally {
    categoriesLoading.value = false
  }
}


const handleCategoryChange = () => {
  emit('change', selectedCategory.value || '')
  if (props.disableNavigation) {
    return
  }
  router.push({
    path: '/questions',
    query: {
      ...route.query,
      category: selectedCategory.value || undefined
    }
  })
}

const goToMyQuestions = () => {
  router.push({
    name: 'profile',
    query: { tab: 'my-questions' }
  })
}

const goToMyAnswers = () => {
  router.push({
    name: 'profile',
    query: { tab: 'my-answers' }
  })
}

watch(
  () => route.query.category,
  (newValue) => {
    selectedCategory.value = newValue || ''
    emit('change', selectedCategory.value || '')
  }
)

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.sidebar {
  position: sticky;
  top: 80px;
  height: fit-content;
}

.sidebar-card {
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  border-right: none;
  border-bottom: none;
  border-left: none;
  
}

.categories-widget h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.75rem;
}

.select-wrapper {
  position: relative;
}

.category-select {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.625rem 2.5rem 0.625rem 0.75rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: #374151;
  appearance: none;
  background-color: #f9fafb;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.category-select:focus {
  border-color: #4CAF4F;
  box-shadow: 0 0 0 3px rgba(76, 175, 79, 0.15);
  outline: none;
}

.select-caret {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: #6b7280;
  font-size: 0.875rem;
}

.my-blocks {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.my-box {
  width: 100%;
  padding: 0.875rem;
  border-radius: 0;
  border: 1px solid #d1d5db;
  background: linear-gradient(135deg, rgba(76, 175, 79, 0.08), rgba(102, 126, 234, 0.08));
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
  font-weight: 600;
  color: #111827;
}

.my-box:hover {
  transform: translateY(-2px);
  border-color: #4CAF4F;
  box-shadow: 0 6px 18px rgba(76, 175, 79, 0.15);
}

.box-label {
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

@media (max-width: 768px) {
  .sidebar {
    position: static;
  }
}
</style>

