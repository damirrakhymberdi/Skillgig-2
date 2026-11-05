<template>
  <div class="changing-profile-page">
    <div class="container">
      <button class="back-link" @click="handleBack">
        ← Back to profile
      </button>

      <div v-if="loading" class="state-card">
        Loading...
      </div>

      <div v-else-if="!profile || !authStore.getIsAuthenticated" class="state-card warning">
        Please log in to edit your profile.
      </div>

      <div v-else class="content-grid">
        <section class="card profile-card">
          <div class="card-header">
            <div>
              <p class="section-label">User</p>
              <h2 class="section-title">
                {{ form.nickname || fallbackNickname }}
              </h2>
            </div>
            <span class="accepted-pill">{{ acceptedAnswers }} accepted</span>
          </div>

          <label class="input-label" for="nickname">Nickname</label>
          <input
            id="nickname"
            v-model="form.nickname"
            type="text"
            class="text-input"
            placeholder="Enter a nickname"
            maxlength="60"
          />
          <p class="input-hint">This nickname is shown on the site.</p>

          <label class="input-label" for="bio">Biography</label>
          <textarea
            id="bio"
            v-model="form.bio"
            class="text-area"
            rows="4"
            placeholder="Tell us a bit about yourself..."
          ></textarea>
        </section>

        <section class="card stats-card">
          <h3 class="section-title">Answer activity</h3>
          <div class="stats-grid">
            <div class="stat-card">
              <span class="stat-label">Accepted rate</span>
              <span class="stat-value">{{ successRate }}%</span>
              <span class="stat-hint">Accepted answers / all answers</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">Answered</span>
              <span class="stat-value">{{ answeredQuestions }}</span>
              <span class="stat-hint">Total answers</span>
            </div>
            <div class="stat-card">
              <span class="stat-label">Accepted answers</span>
              <span class="stat-value">{{ acceptedAnswers }}</span>
              <span class="stat-hint">Accepted answers</span>
            </div>
          </div>
        </section>

        <section class="card identity-card">
          <h3 class="section-title">Who are you?</h3>
          <p class="section-subtitle">You can select multiple roles</p>
          <div class="tag-options">
            <button
              v-for="option in whoOptions"
              :key="option"
              type="button"
              class="tag-option"
              :class="{ selected: whoTags.includes(option) }"
              @click="toggleWhoOption(option)"
            >
              {{ option }}
            </button>
          </div>
        </section>

        <section class="card skills-card">
          <h3 class="section-title">Skills & Tools</h3>
          <p class="section-subtitle">
            Example: Flutter, Performance, ListView
          </p>

          <div class="skill-input-group">
            <input
              v-model="skillInput"
              type="text"
              class="text-input"
              placeholder="New skill"
              @keydown.enter.prevent="handleSkillInput"
              @keydown="handleSkillKeydown"
              @blur="handleSkillInput"
            />
            <button class="add-skill-btn" type="button" @click="handleSkillInput">
              Add
            </button>
          </div>

          <div class="skills-tags" v-if="skillTags.length">
            <span
              v-for="(skill, index) in skillTags"
              :key="`${skill}-${index}`"
              class="skill-tag"
            >
              {{ skill }}
              <button
                type="button"
                class="remove-tag"
                @click="removeSkill(index)"
                  aria-label="Remove skill"
              >
                ×
              </button>
            </span>
          </div>

          <p v-else class="empty-message">
            No skills yet. Add them using the input above.
          </p>
        </section>

        <div class="card actions-card">
          <div class="status-message" v-if="statusMessage" :class="statusType">
            {{ statusMessage }}
          </div>
          <div class="actions">
            <button class="btn-secondary" type="button" @click="resetForm" :disabled="isSaving">
              Cancel
            </button>
            <button class="btn-primary" type="button" @click="handleSave" :disabled="isSaving">
              <span v-if="!isSaving">Save</span>
              <span v-else>Saving...</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/useAuthStore'
import { updateExpertProfile } from '@/services/userservice'

const router = useRouter()
const authStore = useAuthStore()
const { user: storeUser } = storeToRefs(authStore)

const loading = ref(false)
const isSaving = ref(false)
const statusMessage = ref('')
const statusType = ref('success')

const form = ref({
  nickname: '',
  bio: ''
})

const defaultSkills = ['Flutter', 'Performance', 'ListView']
const whoOptions = [
  'Mobile Development',
  'Web Frontend',
  'Web Backend',
  'Fullstack',
  'DevOps',
  'UI/UX Design',
  'AI / ML',
  'Product / PM'
]

const whoTags = ref([])
const skillTags = ref([...defaultSkills])
const skillInput = ref('')

const profile = computed(() => storeUser.value)
const expertProfile = computed(() => profile.value?.expertProfile ?? null)

const fallbackNickname = computed(() => {
  return (
    profile.value?.name ||
    profile.value?.username ||
    profile.value?.email ||
    'My profile'
  )
})

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

const hydrateProfile = async () => {
  if (!authStore.getIsAuthenticated || profile.value) {
    return
  }

  loading.value = true
  try {
    await authStore.hydrateUser()
  } catch (error) {
    console.error('ChangingProfile hydrate error:', error)
    statusMessage.value = 'Could not load profile data.'
    statusType.value = 'error'
  } finally {
    loading.value = false
  }
}

const syncFormWithProfile = () => {
  if (!profile.value) {
    return
  }

  form.value.nickname = profile.value.name || profile.value.username || ''
  form.value.bio = expertProfile.value?.bio || ''
  if (expertProfile.value?.primaryRole) {
    whoTags.value = expertProfile.value.primaryRole
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean)
  } else {
    whoTags.value = []
  }

  if (expertProfile.value?.skills?.length) {
    skillTags.value = [...expertProfile.value.skills]
  } else {
    skillTags.value = [...defaultSkills]
  }
}

const toggleWhoOption = (option) => {
  const index = whoTags.value.indexOf(option)
  if (index >= 0) {
    whoTags.value.splice(index, 1)
  } else {
    whoTags.value.push(option)
  }
}

const addSkill = (skillText) => {
  const skill = skillText.trim()
  if (skill && !skillTags.value.includes(skill)) {
    skillTags.value.push(skill)
  }
}

const handleSkillInput = () => {
  if (!skillInput.value) return
  const raw = skillInput.value.split(',').map((item) => item.trim()).filter(Boolean)
  raw.forEach(addSkill)
  skillInput.value = ''
}

const handleSkillKeydown = (event) => {
  if (event.key === ',' || event.key === 'Enter') {
    event.preventDefault()
    handleSkillInput()
  }
}

const removeSkill = (index) => {
  skillTags.value.splice(index, 1)
}

const resetForm = () => {
  syncFormWithProfile()
  statusMessage.value = ''
}

const handleSave = async () => {
  if (!profile.value) {
    return
  }

  isSaving.value = true
  statusMessage.value = ''

  const headers = authStore.authHeader
    ? { Authorization: authStore.authHeader }
    : undefined

  try {
    const updatedProfile = await updateExpertProfile(
      {
        fullName: form.value.nickname || fallbackNickname.value,
        bio: form.value.bio,
        primaryRole:
          whoTags.value.length > 0
            ? whoTags.value.join(', ')
            : expertProfile.value?.primaryRole || '',
        skills: skillTags.value,
        githubUrl: expertProfile.value?.githubUrl || '',
        linkedinUrl: expertProfile.value?.linkedinUrl || '',
        portfolioUrl: expertProfile.value?.portfolioUrl || '',
        experienceYears: expertProfile.value?.experienceYears || 0
      },
      headers ? { headers } : undefined
    )

    const updatedUser = {
      ...profile.value,
      name: form.value.nickname || fallbackNickname.value,
      expertProfile: updatedProfile
    }

    authStore.updateUser(updatedUser)
    await authStore.hydrateUser({ force: true }).catch(() => {})
    statusMessage.value = 'Profile updated successfully.'
    statusType.value = 'success'

    await router.push({
      path: '/profile',
      query: {
        tab: 'info',
        refreshedAt: Date.now().toString()
      }
    })
  } catch (error) {
    console.error('Profile update error:', error)
    statusMessage.value = error?.message || 'Something went wrong while saving.'
    statusType.value = 'error'
  } finally {
    isSaving.value = false
  }
}

const handleBack = () => {
  const target = profile.value?.id ? `/profile/${profile.value.id}` : '/profile'
  router.push(target)
}

watch(profile, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue) {
    syncFormWithProfile()
  }
}, { immediate: true })

onMounted(async () => {
  await hydrateProfile()
  syncFormWithProfile()
})
</script>

<style scoped>
.changing-profile-page {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding-top: 100px;
  padding-bottom: 4rem;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.back-link {
  align-self: flex-start;
  background: none;
  border: none;
  font-size: 0.95rem;
  color: #4b5563;
  cursor: pointer;
  padding: 0.25rem 0;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.card {
  background-color: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-card {
  grid-column: span 2;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-label {
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.08em;
  color: #9ca3af;
  margin-bottom: 0.25rem;
}

.section-title {
  margin: 0;
  font-size: 1.4rem;
  color: #111827;
}

.section-subtitle {
  margin: 0;
  font-size: 0.9rem;
  color: #6b7280;
}

.accepted-pill {
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  background: #ecfdf5;
  color: #047857;
  font-weight: 600;
  font-size: 0.9rem;
}

.input-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
}

.text-input,
.text-area {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.text-input:focus,
.text-area:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.15);
}

.input-hint {
  margin: 0;
  font-size: 0.8rem;
  color: #9ca3af;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}

.stat-card {
  border: 1px solid #f1f5f9;
  border-radius: 12px;
  padding: 1rem;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.stat-hint {
  font-size: 0.85rem;
  color: #6b7280;
}

.tag-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-option {
  border: 1px solid #d1d5db;
  border-radius: 999px;
  padding: 0.4rem 0.9rem;
  background: #fff;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.tag-option.selected {
  background: #ecfdf5;
  border-color: #34d399;
  color: #047857;
  font-weight: 600;
}

.skill-input-group {
  display: flex;
  gap: 0.75rem;
}

.skill-input-group .text-input {
  flex: 1;
}

.add-skill-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  border: none;
  background: #4caf50;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.add-skill-btn:hover {
  background: #43a047;
}

.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.8rem;
  border-radius: 999px;
  background: #eef2ff;
  color: #4c1d95;
  font-size: 0.85rem;
}

.remove-tag {
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
  font-size: 1rem;
  line-height: 1;
}

.empty-message {
  margin: 0;
  font-size: 0.9rem;
  color: #9ca3af;
}

.state-card {
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  text-align: center;
  background: white;
  color: #374151;
}

.state-card.warning {
  border-color: #fdba74;
  background: #fff7ed;
  color: #9a3412;
}

.actions-card {
  grid-column: span 2;
  gap: 1rem;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  border: 1px solid transparent;
  font-weight: 600;
  cursor: pointer;
  min-width: 150px;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #4caf4f, #2f9e44);
  color: white;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f8fafc;
  border-color: #e2e8f0;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.status-message {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.95rem;
}

.status-message.success {
  background: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.status-message.error {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

@media (max-width: 768px) {
  .profile-card,
  .actions-card {
    grid-column: span 1;
  }

  .skill-input-group {
    flex-direction: column;
  }

  .add-skill-btn {
    width: 100%;
  }
}
</style>

