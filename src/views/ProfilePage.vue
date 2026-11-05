<template>
  <div class="profile-page">
    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="loading">
        Loading...
      </div>

      <div v-else-if="errorMessage" class="error-state">
        {{ errorMessage }}
      </div>

      <!-- Профиль мазмұны -->
      <div v-else-if="profile" class="profile-content">
        <div class="profile-layout">
          <div class="profile-left">
            <!-- Профиль Header -->
            <div class="profile-header">
              <div class="profile-summary">
                <p v-if="displayRole" class="profile-role role-top">{{ displayRole }}</p>
                <img
                  v-if="profileImage"
                  :src="profileImage"
                  alt="Profile"
                  class="profile-photo"
                />
                <div class="profile-actions" v-if="isOwnProfile">
                  <button class="btn-edit-profile" @click="handleEditProfile">
                    Edit profile
                  </button>
                </div>
              </div>
            </div>

            <div v-if="expertProfile" class="expert-summary">
              <div class="metric-card">
                <span class="metric-label">Resolved questions</span>
                <span class="metric-value">{{ expertProfile.resolvedQuestions || 0 }}</span>
              </div>
            </div>
          </div>

          <div class="profile-right">
            <div class="tab-shell">
              <!-- Таб мазмұны -->
              <div class="tab-content">
                <!-- Сұрақтарым -->
                <div v-if="activeTab === 'questions'" class="tab-panel">
                  <div v-if="questionsLoading" class="tab-loading">
                    Loading...
                  </div>
                  <div v-else-if="userQuestions.length === 0" class="empty-state">
                    <p>You haven't asked any questions yet</p>
                    <button class="btn-primary" @click="handleAskQuestion">
                      Ask your first question
                    </button>
                  </div>
                  
                  <div v-else class="questions-list">
                    <div
                      v-for="question in userQuestions"
                      :key="question.id"
                      class="question-item"
                      @click="handleQuestionClick(question.id)"
                    >
                      <h3 class="question-title">{{ question.title }}</h3>
                      <div class="question-meta">
                        <span>{{ question.answersCount || 0 }} answers</span>
                        <span class="separator">•</span>
                        <span>{{ timeAgo(question.createdAt) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Жауаптарым -->
                <div v-if="activeTab === 'answers'" class="tab-panel">
                  <div v-if="answersLoading" class="tab-loading">
                    Loading...
                  </div>
                  <div v-else-if="userAnswers.length === 0" class="empty-state">
                    <p>You haven't posted any answers yet</p>
                  </div>
                  
                  <div v-else class="answers-list">
                    <div
                      v-for="answer in userAnswers"
                      :key="answer.id"
                      class="answer-item"
                      @click="handleAnswerClick(answer.questionId)"
                    >
                      <h3 class="answer-question-title">
                        {{ answer.questionTitle || 'Question' }}
                      </h3>
                      <p class="answer-preview">{{ truncateText(answer.answerText, 150) }}</p>
                      <div class="answer-meta">
                        <span>{{ timeAgo(answer.createdAt) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Ақпарат -->
                <div v-if="activeTab === 'info'" class="tab-panel">
                  <div class="info-card-group">
                    <div class="info-card">
                      <h3 class="info-card-title">Basic info</h3>
                      <dl class="info-list">
                        <div>
                          <dt>Name</dt>
                          <dd>{{ displayName }}</dd>
                        </div>
                      <div>
                        <dt>Role</dt>
                        <dd>{{ expertProfile?.primaryRole || displayRole || 'Not specified' }}</dd>
                        </div>
                        <div v-if="isOwnProfile && profile.email">
                          <dt>Email</dt>
                          <dd>{{ profile.email }}</dd>
                        </div>
                        <div v-if="joinedDate">
                          <dt>Joined</dt>
                          <dd>{{ joinedDate }}</dd>
                        </div>
                        <div v-if="profile.isActive === false">
                          <dt>Status</dt>
                          <dd>Inactive</dd>
                        </div>
                      <div v-if="expertProfile?.experienceYears">
                          <dt>Experience</dt>
                          <dd>{{ expertProfile.experienceYears }} years</dd>
                        </div>
                      <div v-if="expertProfile?.skills?.length">
                        <dt>Skills & Tools</dt>
                        <dd>
                          <div class="skills-list info-skills">
                            <span
                              v-for="skill in expertProfile.skills"
                              :key="skill"
                              class="skill-tag"
                            >
                              {{ skill }}
                            </span>
                          </div>
                        </dd>
                      </div>
                      </dl>
                    </div>

                    <div class="info-card">
                      <h3 class="info-card-title">Answer activity</h3>
                      <div class="info-stat-grid">
                        <div class="info-stat">
                          <span class="info-stat-label">Answered</span>
                          <span class="info-stat-value">{{ answeredQuestions }}</span>
                        </div>
                        <div class="info-stat">
                          <span class="info-stat-label">Accepted answers</span>
                          <span class="info-stat-value">{{ acceptedAnswers }}</span>
                        </div>
                        <div class="info-stat">
                          <span class="info-stat-label">Accepted rate</span>
                          <span class="info-stat-value">{{ successRate }}%</span>
                        </div>
                      </div>
                    </div>

                    <div class="info-card" v-if="expertProfile?.bio">
                      <h3 class="info-card-title">Biography</h3>
                      <p class="info-text">{{ expertProfile.bio }}</p>
                    </div>

                    <div
                      class="info-card links-card"
                      v-if="
                        safeGithubUrl ||
                        safeLinkedinUrl ||
                        safePortfolioUrl
                      "
                    >
                      <h3 class="info-card-title">Links</h3>
                      <ul class="links-list">
                        <li v-if="safeGithubUrl">
                          <span>GitHub</span>
                          <a
                            :href="safeGithubUrl"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {{ safeGithubUrl }}
                          </a>
                        </li>
                        <li v-if="safeLinkedinUrl">
                          <span>LinkedIn</span>
                          <a
                            :href="safeLinkedinUrl"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {{ safeLinkedinUrl }}
                          </a>
                        </li>
                        <li v-if="safePortfolioUrl">
                          <span>Portfolio</span>
                          <a
                            :href="safePortfolioUrl"
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {{ safePortfolioUrl }}
                          </a>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="isOwnProfile" class="qa-panels">
              <div class="qa-box">
                <div class="qa-title">My questions</div>
                <div v-if="questionsLoading" class="tab-loading">
                  Loading...
                </div>
                <div v-else-if="userQuestions.length === 0" class="empty-state alt-empty">
                  <p>You haven't asked any questions yet</p>
                  <button class="btn-primary" @click="handleAskQuestion">
                    Ask your first question
                  </button>
                </div>
                <div v-else class="qa-list">
                  <div
                    v-for="question in userQuestions"
                    :key="question.id"
                    class="qa-item"
                    @click="handleQuestionClick(question.id)"
                  >
                    <h4 class="qa-item-title">{{ question.title }}</h4>
                    <div class="question-meta">
                      <span>{{ question.answersCount || 0 }} answers</span>
                      <span class="separator">•</span>
                      <span>{{ timeAgo(question.createdAt) }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="qa-box">
                <div class="qa-title">My answers</div>
                <div v-if="answersLoading" class="tab-loading">
                  Loading...
                </div>
                <div v-else-if="userAnswers.length === 0" class="empty-state alt-empty">
                  <p>You haven't posted any answers yet</p>
                </div>
                <div v-else class="qa-list">
                  <div
                    v-for="answer in userAnswers"
                    :key="answer.id"
                    class="qa-item"
                    @click="handleAnswerClick(answer.questionId)"
                  >
                    <h4 class="qa-item-title">
                      {{ answer.questionTitle || 'Question' }}
                    </h4>
                    <p class="qa-item-preview">{{ truncateText(answer.answerText, 120) }}</p>
                    <div class="answer-meta">
                      <span>{{ timeAgo(answer.createdAt) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { fetchMyQuestions, fetchMyAnswers } from '@/services/questionsService'
import { fetchUserById } from '@/services/userservice'
import { parseSkillsParam } from '@/utils/profileFallback'
import { safeExternalUrl } from '@/utils/safeExternalUrl'
import profileImage from '@/assets/images/profile.jpg'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { user: storeUser } = storeToRefs(authStore)

const loading = ref(false)
const errorMessage = ref('')
const activeTab = ref('info')
const userQuestions = ref([])
const userAnswers = ref([])
const questionsLoading = ref(false)
const answersLoading = ref(false)
const remoteProfile = ref(null)

const parseNumber = (value, fallback = 0) => {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : fallback
}

const buildFallbackPublicProfile = () => {
  const getQueryValue = (key) => {
    const value = route.query?.[key]
    if (Array.isArray(value)) {
      return value[0]
    }
    return value
  }

  const query = route.query || {}
  const queryName = getQueryValue('name')
  const queryUserRole = getQueryValue('userRole')
  const queryPrimaryRole = getQueryValue('primaryRole')
  const queryAnswered = getQueryValue('answered')
  const fallbackName =
    typeof queryName === 'string' && queryName.trim().length
      ? queryName
      : 'User'
  const fallbackUserRole =
    (typeof queryUserRole === 'string' && queryUserRole.trim().length
      ? queryUserRole
      : null) ||
    (typeof getQueryValue('role') === 'string' &&
    getQueryValue('role').trim().length
      ? getQueryValue('role')
      : '')
  const fallbackPrimaryRole =
    (typeof queryPrimaryRole === 'string' && queryPrimaryRole.trim().length
      ? queryPrimaryRole
      : null) || fallbackUserRole

  return {
    id: requestedUserId.value || query.id || 'unknown-user',
    name: fallbackName,
    role: fallbackUserRole || 'expert',
    answersCount: parseNumber(queryAnswered, 0),
    expertProfile: {
      fullName: fallbackName,
      bio: getQueryValue('bio') || '',
      primaryRole: fallbackPrimaryRole || '',
      skills: parseSkillsParam(getQueryValue('skills')),
      githubUrl: getQueryValue('github') || '',
      linkedinUrl: getQueryValue('linkedin') || '',
      portfolioUrl: getQueryValue('portfolio') || '',
      experienceYears: parseNumber(getQueryValue('experience'), 0),
      resolvedQuestions: parseNumber(getQueryValue('resolved'), 0)
    }
  }
}

const requestedUserId = computed(() => route.params.id ?? null)
const storeUserId = computed(() => storeUser.value?.id ?? null)
const isMeRoute = computed(() => !requestedUserId.value || requestedUserId.value === 'me')

const isOwnProfile = computed(() => {
  if (isMeRoute.value) {
    return true
  }
  if (!storeUserId.value) {
    return false
  }
  return requestedUserId.value === storeUserId.value
})

const profile = computed(() => {
  if (isOwnProfile.value) {
    return storeUser.value
  }
  return remoteProfile.value
})

const expertProfile = computed(() => profile.value?.expertProfile ?? null)
const safeGithubUrl = computed(() => safeExternalUrl(expertProfile.value?.githubUrl))
const safeLinkedinUrl = computed(() => safeExternalUrl(expertProfile.value?.linkedinUrl))
const safePortfolioUrl = computed(() => safeExternalUrl(expertProfile.value?.portfolioUrl))

const answeredQuestions = computed(() => {
  if (profile.value?.answersCount != null) {
    return profile.value.answersCount
  }
  return expertProfile.value?.resolvedQuestions ?? 0
})

const acceptedAnswers = computed(() => expertProfile.value?.resolvedQuestions ?? 0)

const successRate = computed(() => {
  if (!answeredQuestions.value) {
    return 0
  }
  return Math.round((acceptedAnswers.value / answeredQuestions.value) * 100)
})

const displayName = computed(() => {
  if (expertProfile.value?.fullName) {
    return expertProfile.value.fullName
  }
  return profile.value?.name || profile.value?.email || 'User'
})

const displayRole = computed(() => {
  const role = expertProfile.value?.primaryRole
  if (role) {
    return role
  }
  if (profile.value?.role === 'expert') {
    return 'IT specialist'
  }
  if (profile.value?.role === 'client') {
    return 'Client'
  }
  return ''
})

const joinedDate = computed(() => {
  if (!profile.value?.createdAt) {
    return null
  }
  try {
    return new Date(profile.value.createdAt).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch {
    return profile.value.createdAt
  }
})

const ownTabs = [
  { id: 'questions', label: 'My questions' },
  { id: 'answers', label: 'My answers' },
  { id: 'info', label: 'Info' }
]

const publicTabs = [{ id: 'info', label: 'Info' }]

const tabs = computed(() => (isOwnProfile.value ? ownTabs : publicTabs))

const loadProfile = async (force = false) => {
  loading.value = true
  errorMessage.value = ''

  try {
    if (isOwnProfile.value) {
      remoteProfile.value = null
      if (!authStore.getIsAuthenticated) {
        throw new Error('Please log in to view your profile.')
      }
      await authStore.hydrateUser({ force })
    } else {
      const targetUserId = requestedUserId.value
      if (!targetUserId) {
        throw new Error('User not found.')
      }
      remoteProfile.value = null
      remoteProfile.value = await fetchUserById(targetUserId)
    }
  } catch (error) {
    console.error('Error loading profile:', error)
    if (!isOwnProfile.value) {
      remoteProfile.value = buildFallbackPublicProfile()
      errorMessage.value = ''
    } else {
      errorMessage.value =
        error?.message || 'Something went wrong while loading the profile.'
    }
  } finally {
    loading.value = false
  }
}

// Пайдаланушы сұрақтарын жүктеу
const loadUserQuestions = async () => {
  if (!isOwnProfile.value || !authStore.getIsAuthenticated) {
    userQuestions.value = []
    return
  }
  questionsLoading.value = true
  try {
    const data = await fetchMyQuestions()
    userQuestions.value = data
  } catch (error) {
    console.error('Error loading user questions:', error)
    userQuestions.value = []
  } finally {
    questionsLoading.value = false
  }
}

const loadUserAnswers = async () => {
  if (!isOwnProfile.value || !authStore.getIsAuthenticated) {
    userAnswers.value = []
    return
  }
  answersLoading.value = true
  try {
    const data = await fetchMyAnswers()
    userAnswers.value = data
  } catch (error) {
    console.error('Error loading user answers:', error)
    userAnswers.value = []
  } finally {
    answersLoading.value = false
  }
}

// Таб өзгергенде деректерді жүктеу
const handleTabChange = () => {
  if (!isOwnProfile.value) {
    return
  }
  if (activeTab.value === 'questions') {
    loadUserQuestions()
  } else if (activeTab.value === 'answers') {
    loadUserAnswers()
  }
}

// Профильді өңдеу
const handleEditProfile = () => {
  router.push('/profile/change')
}

// Сұраққа бату
const handleQuestionClick = (questionId) => {
  router.push(`/questions/${questionId}`)
}

// Жауапқа бату
const handleAnswerClick = (questionId) => {
  router.push(`/questions/${questionId}`)
}

// Сұрақ қою
const handleAskQuestion = () => {
  router.push('/ask')
}

// Утилиталар
const timeAgo = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
  
  if (diffInHours < 24) return `${diffInHours} hours ago`
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays === 1) return 'yesterday'
  if (diffInDays < 7) return `${diffInDays} days ago`
  return date.toLocaleDateString('en-US')
}

const truncateText = (text, length) => {
  if (!text) return ''
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

const mapQueryTabToId = (tabValue) => {
  if (tabValue === 'my-answers') {
    return 'answers'
  }
  if (['info', 'questions', 'answers'].includes(tabValue)) {
    return tabValue
  }
  return null
}

const applyTabSelection = (tabValue) => {
  const availableTabs = tabs.value || []
  if (availableTabs.length === 0) {
    activeTab.value = 'info'
    return
  }

  const desired =
    mapQueryTabToId(tabValue) || 'info'

  if (availableTabs.some((tab) => tab.id === desired)) {
    activeTab.value = desired
  } else {
    activeTab.value = availableTabs[0].id
  }
}

onMounted(async () => {
  await loadProfile(!profile.value)
  applyTabSelection(route.query.tab)
  if (isOwnProfile.value && authStore.getIsAuthenticated) {
    await Promise.all([loadUserQuestions(), loadUserAnswers()])
  } else {
    handleTabChange()
  }
})

watch(
  () => activeTab.value,
  () => {
    handleTabChange()
  }
)

watch(
  () => route.query.tab,
  (tab) => {
    applyTabSelection(tab)
  },
  { immediate: true }
)

watch(
  tabs,
  () => {
    applyTabSelection(route.query.tab)
  },
  { immediate: true }
)

watch(
  () => route.params.id,
  async () => {
    applyTabSelection(route.query.tab)
    await loadProfile(true)
  }
)
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: #f8f9fa;
  background-image: url('@/assets/images/bgs/laura-bellin-_dYOffyB5V8-unsplash.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 8rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.75rem;
  background: rgb(255, 255, 255);
  border-radius: 5px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.tab-loading {
  padding: 2rem 0;
  text-align: center;
  color: #6b7280;
  font-weight: 500;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.profile-layout {
  display: flex;
  gap: 0rem;
  min-height: 80vh;
}

.profile-left {
  flex: 0 0 20%;
  display: flex;
  flex-direction: column;
  gap: 0;
  min-height: 80vh;
}

.profile-right {
  flex: 1 1 60%;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
  max-height: 80vh;
  border: 1px solid #e5e7eb;
  
}

/* Profile Header */
.profile-header {
  background-color: white;
  border: 0;
  border-radius: 0;
  padding: .25rem;
  padding-right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: flex-start;
  flex-wrap: wrap;
  flex: 1 1 60%;
  min-height: 0;
}

.profile-summary {
  flex: 1;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}

.profile-label {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin-bottom: 0.35rem;
}

.profile-name {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.profile-role {
  font-size: 1rem;
  color: #4b5563;
  margin: 0.25rem 0 0.5rem 0;
}

.role-top {
  order: -1;
  font-size: 1.05rem;
  font-weight: 600;
  color: #1f2937;
}

.profile-photo {
  width: 100%;
  max-width: none;
  object-fit: cover;
  object-position: center;
}

.separator {
  color: #d1d5db;
}

.profile-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  position: absolute;
  right: 0;
  bottom: 0;
  align-items: flex-end;
}

.btn-edit-profile {
  padding: 0.4rem .9rem;
  background-color: #22c55e;
  border: none;
  border-radius: 6px;
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 38px;
  margin-bottom: 1rem;
  align-self: flex-start;
}

.btn-edit-profile:hover {
  background-color: #16a34a;
}

.expert-summary {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  flex: 1 1 15%;
  min-height: 0;
}

.metric-card {
  background-color: white;
  border: 1px solid #e5e7eb;
  border-left: none;
  border-right: none;
  border-bottom: none;
  border-radius: 0;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0rem;
  height: 80%;
}

.metric-label {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
}

.error-state {
  padding: 2rem;
  text-align: center;
  border: 1px solid #fecaca;
  border-radius: 12px;
  background: #fee2e2;
  color: #b91c1c;
}

.profile-link {
  color: #2563eb;
  text-decoration: underline;
  word-break: break-all;
}

.info-card-group {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.info-card {
  background: rgba(255, 255, 255, 0.96);
  border: none;
  border-radius: 0;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.04);
}

.info-card-title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: #111827;
}

.info-list {
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.75rem;
}

.info-list dt {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #9ca3af;
}

.info-list dd {
  margin: 0.15rem 0 0 0;
  font-size: 0.95rem;
  color: #111827;
}

.info-stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.info-stat {
  background: #f5f7fb;
  border-radius: 0;
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  box-shadow: inset 0 -1px rgba(0, 0, 0, 0.03);
}

.info-stat-label {
  font-size: 0.8rem;
  color: #6b7280;
}

.info-stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
}

.info-text {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
}

.links-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.links-list li {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.links-list span {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #9ca3af;
}

.links-list a {
  color: #2563eb;
  word-break: break-all;
}

@media (max-width: 768px) {
  .info-list {
    grid-template-columns: 1fr;
  }

  .info-stat-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
  padding: 0 1.5rem;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: #6b7280;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: -2px;
}

.tab-btn:hover {
  color: #374151;
}

.tab-btn.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

/* Tab Content */
  

.tab-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tab-shell {
  flex: 0 0 50vh;
  max-height: 50vh;
  min-height: 50vh;
  display: flex;
  flex-direction: column;
  overflow: auto;
  scrollbar-width: auto;
  -ms-overflow-style: auto;
  background-color: #f9fafb;
  padding: 0.25rem;
}

.tab-shell::-webkit-scrollbar {
  width: 10px;
}

.tab-shell::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

.tab-shell::-webkit-scrollbar-track {
  background: transparent;
}

.qa-panels {
  flex: 1 1 auto;
  display: flex;
  gap: 0;
  min-height: 0;
}

.qa-box {
  flex: 1 1 50%;
  background: rgb(246, 246, 246);
  border: 1px solid #e5e7eb;
  border-radius: 0;
  padding: .25rem;
  margin: .25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 0;
  min-height: 0;
}

.qa-box + .qa-box {
  border-left: none;
}

.qa-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.qa-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow: auto;
  max-height: 260px;
  padding-right: 4px;
}

/* Make scrollbars visible inside profile lists (Windows/macOS/Firefox) */
.qa-list {
  scrollbar-width: auto;
  -ms-overflow-style: auto;
  scrollbar-color: #cbd5e1 transparent;
  scrollbar-gutter: stable;
}

.qa-list::-webkit-scrollbar {
  width: 10px;
}

.qa-list::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

.qa-list::-webkit-scrollbar-track {
  background: transparent;
}
.qa-item {
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0;
  background: #f9fafb;
  cursor: pointer;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.qa-item:hover {
  border-color: #d1d5db;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
}

.qa-item-title {
  margin: 0 0 0.4rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.qa-item-preview {
  margin: 0 0 0.4rem 0;
  color: #374151;
  font-size: 0.9375rem;
  line-height: 1.4;
}

.alt-empty {
  background: none;
  border: none;
  padding: 0;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
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
  margin-top: 1rem;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Questions List */
.questions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.question-item {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.question-item:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.question-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.5rem 0;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}

/* Answers List */
.answers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.answer-item {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.answer-item:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.answer-question-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #667eea;
  margin: 0 0 0.5rem 0;
}

.answer-preview {
  font-size: 0.9375rem;
  color: #374151;
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
}

.answer-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.info-skills {
  padding-top: 0.25rem;
}

.skill-tag {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  background-color: #f3f4f6;
  color: #374151;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .profile-actions {
    width: 100%;
  }

  .btn-edit-profile {
    width: 100%;
  }

  .tabs {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
}
</style>

