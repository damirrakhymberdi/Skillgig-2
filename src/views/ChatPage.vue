<template>
  <div class="chat-page">
    <div class="chat-container">
      <!-- Chat Header -->
      <div class="chat-header">
        <button class="btn-back" @click="handleBack">
          ← Артқа
        </button>
        <div class="chat-partner-info">
          <div class="partner-avatar">
            {{ partnerName?.charAt(0) || 'U' }}
          </div>
          <div class="partner-details">
            <h2 class="partner-name">{{ partnerName }}</h2>
            <p class="partner-role">{{ isExpert ? 'Эксперт' : 'Клиент' }}</p>
          </div>
        </div>
      </div>

      <!-- Сұрақ ақпараты -->
      <div class="question-info">
        <h3 class="question-title">{{ questionTitle }}</h3>
      </div>

      <p v-if="errorMessage" class="chat-error" role="alert">
        {{ errorMessage }}
      </p>

      <!-- Messages -->
      <div class="messages-container" ref="messagesContainer">
        <div v-if="loading" class="loading-messages">
          Жүктелуде...
        </div>
        
        <div v-else class="messages-list">
          <p v-if="messages.length === 0 && !errorMessage" class="empty-messages">
            Әзірге хабарлама жоқ. Әңгімені баста.
          </p>
          <div
            v-for="message in messages"
            :key="message.id"
            class="message"
            :class="{ 'message-own': message.isOwn, 'message-other': !message.isOwn }"
          >
            <div class="message-avatar" v-if="!message.isOwn">
              {{ partnerName?.charAt(0) || 'U' }}
            </div>
            
            <div class="message-content">
              <div class="message-text">{{ message.text }}</div>
              <div class="message-time">{{ formatTime(message.createdAt) }}</div>
            </div>

            <div class="message-avatar" v-if="message.isOwn">
              {{ currentUserName?.charAt(0) || 'M' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Message Input -->
      <div class="message-input-container">
        <p v-if="sendError" class="chat-error" role="alert">{{ sendError }}</p>
        <form @submit.prevent="handleSendMessage" class="message-form">
          <textarea
            id="chat-message"
            v-model="messageText"
            class="message-input"
            placeholder="Хабарлама жазу..."
            aria-label="Хабарлама мәтіні"
            maxlength="5000"
            rows="1"
            @keydown.enter.exact.prevent="handleSendMessage"
            :disabled="Boolean(errorMessage) || sending"
            ref="messageInputRef"
          ></textarea>
          <button
            type="submit"
            class="btn-send"
            :disabled="!messageText.trim() || sending || Boolean(errorMessage)"
          >
            {{ sending ? 'Жіберілуде…' : 'Жіберу' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { fetchQuestionById } from '@/services/questionsService'
import { fetchUserById } from '@/services/userservice'
import { fetchChatMessages, sendChatMessage } from '@/services/chatService'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const questionId = String(route.params.questionId || '')
const partnerId = computed(() => {
  const partner = route.query.partner
  return Array.isArray(partner) ? partner[0] || '' : partner || ''
})
const loading = ref(false)
const messages = ref([])
const messageText = ref('')
const partnerName = ref('')
const questionTitle = ref('')
const isExpert = ref(false)
const errorMessage = ref('')
const sendError = ref('')
const sending = ref(false)
const currentUserName = computed(() => {
  const user = authStore.user
  return user?.name || [user?.firstName, user?.lastName].filter(Boolean).join(' ') || 'Мен'
})

const messagesContainer = ref(null)
const messageInputRef = ref(null)

const loadMessages = async ({ initial = false } = {}) => {
  if (initial) loading.value = true
  try {
    const latest = await fetchChatMessages(questionId, partnerId.value)
    const previousLastId = messages.value.at(-1)?.id
    messages.value = latest.map((message) => ({
      ...message,
      isOwn: message.senderId === authStore.user?.id
    }))
    if (initial || messages.value.at(-1)?.id !== previousLastId) {
      await nextTick()
      scrollToBottom()
    }
  } catch (error) {
    if (initial) throw error
    console.error('Could not refresh chat messages:', error)
  } finally {
    if (initial) loading.value = false
  }
}

// Хабарлама жіберу
const handleSendMessage = async () => {
  const text = messageText.value.trim()
  if (!text || sending.value || !partnerId.value) return

  sending.value = true
  sendError.value = ''
  try {
    const message = await sendChatMessage(questionId, partnerId.value, text)
    messages.value.push({ ...message, isOwn: true })
    messageText.value = ''
    await nextTick()
    adjustTextareaHeight()
    scrollToBottom()
  } catch (error) {
    console.error('Error sending message:', error)
    sendError.value = error?.message || 'Хабарламаны жіберу мүмкін болмады.'
  } finally {
    sending.value = false
  }
}

// Textarea биіктігін автоматты түрде реттеу
const adjustTextareaHeight = () => {
  if (messageInputRef.value) {
    messageInputRef.value.style.height = 'auto'
    messageInputRef.value.style.height = messageInputRef.value.scrollHeight + 'px'
  }
}

// Скроллды төменге жылжыту
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Уақытты форматтау
const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInMs = now - date
  const diffInMinutes = Math.floor(diffInMs / (1000 * 60))
  
  if (diffInMinutes < 1) return 'just now'
  if (diffInMinutes < 60) return `${diffInMinutes} min ago`
  
  const diffInHours = Math.floor(diffInMinutes / 60)
  if (diffInHours < 24) return `${diffInHours} h ago`
  
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

// Артқа бату
const handleBack = () => {
  router.back()
}

// Хабарламаларды автоматты түрде жаңарту (polling)
let pollingInterval = null

const startPolling = () => {
  pollingInterval = setInterval(() => loadMessages(), 5000)
}

const stopPolling = () => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

// Textarea биіктігін реттеу
watch(() => messageText.value, () => {
  nextTick(() => {
    adjustTextareaHeight()
  })
})

onMounted(async () => {
  loading.value = true
  try {
    if (!partnerId.value) {
      throw new Error('Әңгімелесушіні сұрақ бетінен таңдаңыз.')
    }
    if (!authStore.getIsAuthenticated) {
      throw new Error('Чатқа кіру үшін аккаунтыңызға кіріңіз.')
    }

    await authStore.hydrateUser()
    if (!authStore.user?.id) {
      throw new Error('Пайдаланушыны анықтай алмадық. Қайта кіріп көріңіз.')
    }

    const [question, partner] = await Promise.all([
      fetchQuestionById(questionId),
      fetchUserById(partnerId.value)
    ])
    if (!question || !partner) {
      throw new Error('Сұрақ немесе әңгімелесуші табылмады.')
    }

    questionTitle.value = question.title
    partnerName.value = partner.name || partner.username || 'Пайдаланушы'
    isExpert.value = partner.role === 'expert'
    await loadMessages({ initial: true })
    adjustTextareaHeight()
    startPolling()
  } catch (error) {
    console.error('Could not open chat:', error)
    errorMessage.value = error?.status === 403
      ? 'Бұл сұрақтағы әңгімеге қатысуға рұқсатыңыз жоқ.'
      : error?.message || 'Чатты жүктеу мүмкін болмады. Қайта көріңіз.'
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.chat-page {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding-top: 80px;
  display: flex;
  flex-direction: column;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 80px);
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

/* Chat Header */
.chat-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background-color: white;
}

.btn-back {
  padding: 0.5rem;
  background: none;
  border: none;
  color: #6b7280;
  font-size: 1rem;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-back:hover {
  color: #111827;
}

.chat-partner-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.partner-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1rem;
}

.partner-details {
  flex: 1;
}

.partner-name {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.partner-role {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0;
}

/* Question Info */
.question-info {
  padding: 0.75rem 1.5rem;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.question-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

/* Messages Container */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #f9fafb;
}

.loading-messages {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.chat-error {
  margin: 0.75rem 1.5rem;
  color: #8b3d32;
  font-size: 0.9rem;
}

.empty-messages {
  margin: auto;
  color: #6b7280;
  text-align: center;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Message */
.message {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  max-width: 70%;
}

.message-own {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-other {
  align-self: flex-start;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #16834b;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.message-text {
  padding: 0.75rem 1rem;
  border-radius: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.5;
}

.message-own .message-text {
  background: #16834b;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-other .message-text {
  background-color: white;
  color: #111827;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 0.75rem;
  color: #9ca3af;
  padding: 0 0.5rem;
}

/* Message Input */
.message-input-container {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  background-color: white;
}

.message-form {
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
}

.message-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-family: inherit;
  color: #111827;
  resize: none;
  max-height: 120px;
  overflow-y: auto;
  transition: border-color 0.2s;
}

.message-input:focus {
  outline: none;
  border-color: #16834b;
  box-shadow: 0 0 0 3px rgba(22, 131, 75, 0.12);
}

.message-input::placeholder {
  color: #9ca3af;
}

.btn-send {
  padding: 0.75rem 1.5rem;
  background: #16834b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-send:hover:not(:disabled) {
  transform: translateY(-1px);
  background: #116b3d;
  box-shadow: 0 4px 12px rgba(22, 131, 75, 0.2);
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .chat-page {
    padding-top: 0;
  }

  .chat-container {
    height: 100vh;
    border-radius: 0;
  }

  .message {
    max-width: 85%;
  }
}
</style>

