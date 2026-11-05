import { apiGet, apiPost } from './api'

const buildMessagesPath = (questionId, partnerId) => {
  if (!questionId || !partnerId) {
    throw new Error('Question and chat partner are required')
  }

  const query = new URLSearchParams({ partner_id: partnerId })
  return `/chat/questions/${encodeURIComponent(questionId)}/messages?${query}`
}

const normalizeMessage = (message = {}) => ({
  id: message.id,
  questionId: message.questionId ?? message.question_id,
  senderId: message.senderId ?? message.sender_id,
  recipientId: message.recipientId ?? message.recipient_id,
  text: message.text ?? '',
  createdAt: message.createdAt ?? message.created_at
})

export const fetchChatMessages = async (questionId, partnerId) => {
  const messages = await apiGet(buildMessagesPath(questionId, partnerId))
  return Array.isArray(messages) ? messages.map(normalizeMessage) : []
}

export const sendChatMessage = async (questionId, partnerId, text) => {
  const message = await apiPost(
    buildMessagesPath(questionId, partnerId),
    { text }
  )
  return normalizeMessage(message)
}
