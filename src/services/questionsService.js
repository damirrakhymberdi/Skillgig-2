import { apiGet, apiPost, apiPut, apiDelete } from './api'

const DEFAULT_LIST_LIMIT = 20

const toArray = (value) => {
  if (!value) {
    return []
  }

  if (Array.isArray(value)) {
    return value.filter(Boolean)
  }

  if (typeof value === 'string') {
    try {
      const parsed = JSON.parse(value)
      if (Array.isArray(parsed)) {
        return parsed.filter(Boolean)
      }
    } catch {
      return value
        .split(',')
        .map((entry) => entry.trim())
        .filter(Boolean)
    }
  }

  return []
}

const normalizeProfile = (rawProfile = null) => {
  if (!rawProfile) {
    return null
  }

  return {
    fullName: rawProfile.full_name ?? rawProfile.fullName ?? null,
    bio: rawProfile.bio ?? '',
    primaryRole: rawProfile.primary_role ?? rawProfile.primaryRole ?? '',
    skills: toArray(rawProfile.skills),
    githubUrl: rawProfile.github_url ?? rawProfile.githubUrl ?? '',
    linkedinUrl: rawProfile.linkedin_url ?? rawProfile.linkedinUrl ?? '',
    portfolioUrl: rawProfile.portfolio_url ?? rawProfile.portfolioUrl ?? '',
    experienceYears:
      rawProfile.experience_years ?? rawProfile.experienceYears ?? 0,
    averageRating:
      rawProfile.average_rating ?? rawProfile.averageRating ?? 0,
    answersCount:
      rawProfile.answers_count ?? rawProfile.answersCount ?? 0,
    resolvedQuestions:
      rawProfile.resolved_questions ?? rawProfile.resolvedQuestions ?? 0
  }
}

const buildQuery = (params = {}) => {
  const qs = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return
    }
    if (Array.isArray(value)) {
      value.forEach((entry) => qs.append(key, entry))
    } else {
      qs.append(key, String(value))
    }
  })
  const queryString = qs.toString()
  return queryString ? `?${queryString}` : ''
}

const normalizeDateValue = (value) => {
  if (!value) {
    return null
  }

  if (value instanceof Date) {
    return value.toISOString()
  }

  if (typeof value === 'number') {
    const dateFromNumber = new Date(value)
    return Number.isNaN(dateFromNumber.getTime())
      ? null
      : dateFromNumber.toISOString()
  }

  if (typeof value === 'string') {
    const hasTimezone = /[zZ]|[+\-]\d{2}:?\d{2}$/.test(value)
    const normalizedString = hasTimezone ? value : `${value}Z`
    const parsed = new Date(normalizedString)
    if (!Number.isNaN(parsed.getTime())) {
      return parsed.toISOString()
    }
  }

  return null
}

const splitDescriptionAndCodeExample = (description = '', explicitCodeExample = null) => {
  if (explicitCodeExample) {
    return { cleanDescription: description, codeExample: explicitCodeExample }
  }

  const marker = /Code example:\s*/i
  if (!description || !marker.test(description)) {
    return { cleanDescription: description, codeExample: null }
  }

  const [before, ...afterParts] = description.split(marker)
  const extractedCode = afterParts.join('Code example:').trim()
  const cleanDescription = before.trimEnd()

  return {
    cleanDescription: cleanDescription || description,
    codeExample: extractedCode || null
  }
}

const normalizeQuestion = (item) => {
  if (!item) {
    return null
  }

  const { cleanDescription, codeExample } = splitDescriptionAndCodeExample(
    item.description ?? '',
    item.code_example ?? item.codeExample ?? null
  )

  return {
    id: item.id ?? item.question_id ?? crypto.randomUUID?.() ?? String(Math.random()),
    title: item.title ?? 'Атауы жоқ',
    description: cleanDescription ?? '',
    codeExample,
    category: item.category ?? 'General',
    difficulty: item.difficulty ?? null,
    tags: item.tags ?? [],
    links: item.links ?? [],
    codeLink:
      item.code_link ??
      item.codeLink ??
      (Array.isArray(item.links) && item.links.length ? item.links[0] : null),
    deadline: normalizeDateValue(item.deadline),
    status: item.status ?? 'draft',
    acceptedAnswerId:
      item.accepted_answer_id ?? item.acceptedAnswerId ?? null,
    clientId: item.client_id ?? item.clientId ?? item.user_id ?? null,
    clientName:
      item.client_name ?? item.clientName ?? item.clientId ?? 'Аноним',
    clientRole: item.client_role ?? item.clientRole ?? '',
    clientProfile: normalizeProfile(
      item.client_profile ?? item.clientProfile ?? null
    ),
    createdAt:
      normalizeDateValue(item.created_at ?? item.createdAt) ??
      new Date().toISOString(),
    updatedAt: normalizeDateValue(item.updated_at ?? item.updatedAt),
    answersCount: item.answers_count ?? item.answersCount ?? 0,
    isSolved:
      item.status === 'resolved' ||
      item.status === 'closed' ||
      Boolean(item.accepted_answer_id ?? item.acceptedAnswerId)
  }
}

const normalizeAnswer = (item) => {
  if (!item) {
    return null
  }

  return {
    id: item.id ?? item.answer_id ?? crypto.randomUUID?.() ?? String(Math.random()),
    questionId: item.questionId ?? item.question_id ?? null,
    questionTitle: item.questionTitle ?? item.question_title ?? null,
    authorId: item.authorId ?? item.author_id ?? null,
    authorAnswersCount:
      item.author_answers_count ?? item.authorAnswersCount ?? null,
    authorRole: item.authorRole ?? item.author_role ?? '',
    authorProfile: normalizeProfile(
      item.authorProfile ?? item.author_profile ?? null
    ),
    answerText: item.answerText ?? item.answer_text ?? '',
    codeExample: item.codeExample ?? item.code_example ?? null,
    links: Array.isArray(item.links) ? item.links : [],
    expertName: item.expertName ?? 'Аноним',
    expertRating: Number(item.expertRating ?? 0),
    isAccepted: Boolean(item.isAccepted ?? item.is_accepted),
    createdAt:
      normalizeDateValue(item.created_at ?? item.createdAt) ??
      new Date().toISOString()
  }
}

export const fetchRecentQuestions = async ({ limit = 5, status = 'published' } = {}) => {
  const query = buildQuery({
    limit,
    status_filter: status
  })

  const data = await apiGet(`/questions/${query}`)

  if (Array.isArray(data)) {
    return data.map(normalizeQuestion).filter(Boolean)
  }

  if (Array.isArray(data?.items)) {
    return data.items.map(normalizeQuestion).filter(Boolean)
  }

  return []
}

export const fetchQuestions = async ({
  limit = DEFAULT_LIST_LIMIT,
  offset = 0,
  category,
  difficulty,
  search,
  sortBy,
  tags,
  status = 'published'
} = {}) => {
  const query = buildQuery({
    limit,
    offset,
    category,
    difficulty,
    search,
    sort_by: sortBy,
    status_filter: status,
    tags
  })

  const data = await apiGet(`/questions/${query}`)

  const items = Array.isArray(data?.items) ? data.items : Array.isArray(data) ? data : []

  return {
    total: data?.total ?? items.length,
    items: items.map(normalizeQuestion).filter(Boolean)
  }
}

export const fetchQuestionById = async (questionId) => {
  if (!questionId) {
    throw new Error('Question ID қажет')
  }
  const data = await apiGet(`/questions/${questionId}`)
  return normalizeQuestion(data)
}

export const createQuestion = async (payload) => {
  if (!payload?.title || !payload?.description || !payload?.category) {
    throw new Error('Title, description және category қажет')
  }

  const response = await apiPost('/questions/', payload)
  return normalizeQuestion(response)
}

export const updateQuestion = async (questionId, payload, options = {}) => {
  if (!questionId) {
    throw new Error('Question ID қажет')
  }
  const response = await apiPut(`/questions/${questionId}`, payload, options)
  return normalizeQuestion(response)
}

export const deleteQuestion = async (questionId) => {
  if (!questionId) {
    throw new Error('Question ID қажет')
  }
  return apiDelete(`/questions/${questionId}`)
}

export const fetchQuestionAnswers = async (questionId) => {
  if (!questionId) {
    throw new Error('Question ID қажет')
  }
  const data = await apiGet(`/questions/${questionId}/answers`)
  if (!Array.isArray(data)) {
    return []
  }
  return data.map(normalizeAnswer).filter(Boolean)
}

export const createAnswer = async (questionId, payload) => {
  if (!questionId) {
    throw new Error('Question ID қажет')
  }
  if (!payload?.answerText) {
    throw new Error('Answer text қажет')
  }
  const response = await apiPost(`/questions/${questionId}/answers`, {
    answerText: payload.answerText,
    codeExample: payload.codeExample,
    links: Array.isArray(payload.links) ? payload.links : [],
  })
  return normalizeAnswer(response)
}

export const updateAnswer = async (questionId, answerId, payload) => {
  if (!questionId || !answerId) {
    throw new Error('Question ID және Answer ID қажет')
  }
  const response = await apiPut(`/questions/${questionId}/answers/${answerId}`, {
    answerText: payload.answerText,
    codeExample: payload.codeExample,
    links: Array.isArray(payload.links) ? payload.links : undefined,
  })
  return normalizeAnswer(response)
}

export const deleteAnswer = async (questionId, answerId) => {
  if (!questionId || !answerId) {
    throw new Error('Question ID және Answer ID қажет')
  }
  return apiDelete(`/questions/${questionId}/answers/${answerId}`)
}

export const verifyAnswer = async (questionId, answerId, isCorrect) => {
  if (!questionId || !answerId) {
    throw new Error('Question ID және Answer ID қажет')
  }
  const response = await apiPost(
    `/questions/${questionId}/answers/${answerId}/verify`,
    {
      isCorrect: Boolean(isCorrect)
    }
  )
  return normalizeAnswer(response)
}

export const fetchMyQuestions = async () => {
  const data = await apiGet('/users/me/questions')
  if (!Array.isArray(data)) {
    return []
  }
  return data.map(normalizeQuestion).filter(Boolean)
}

export const fetchMyAnswers = async () => {
  const data = await apiGet('/users/me/answers')
  if (!Array.isArray(data)) {
    return []
  }
  return data.map(normalizeAnswer).filter(Boolean)
}


