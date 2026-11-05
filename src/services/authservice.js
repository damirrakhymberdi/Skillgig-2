import { apiPost } from './api'

const DEFAULT_ROLE = 'client'

const compactObject = (obj = {}) =>
  Object.entries(obj).reduce((acc, [key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      acc[key] = value
    }
    return acc
  }, {})

const coerceNumber = (value, fallback = 0) => {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : fallback
}

export const normalizeUser = (rawUser, fallback = {}) => {
  if (!rawUser && !fallback) {
    return null
  }

  const source = rawUser || {}
  const firstName =
    source.first_name ?? source.firstName ?? fallback.firstName ?? ''
  const lastName =
    source.last_name ?? source.lastName ?? fallback.lastName ?? ''
  const derivedName = source.name ?? (
    [firstName, lastName].filter(Boolean).join(' ') ||
    fallback.name ||
    ''
  )

  return {
    id: source.id ?? source.user_id ?? fallback.id ?? null,
    email: source.email ?? fallback.email ?? '',
    username: source.username ?? source.login ?? fallback.username ?? '',
    firstName,
    lastName,
    name: derivedName,
    role: source.role ?? fallback.role ?? DEFAULT_ROLE,
    expertProfile:
      source.expert_profile ?? source.expertProfile ?? fallback.expertProfile ?? null,
    avatar: source.avatar ?? source.image ?? fallback.avatar ?? null,
    answersCount: coerceNumber(
      source.answers_count ??
        source.answersCount ??
        fallback.answersCount ??
        0
    )
  }
}

export const normalizeAuthResponse = (payload = {}, fallbackUser = {}) => {
  const accessToken =
    payload.access_token ?? payload.token ?? payload.accessToken ?? null
  const refreshToken =
    payload.refresh_token ?? payload.refreshToken ?? null
  const tokenType =
    payload.token_type ?? payload.tokenType ?? (accessToken ? 'Bearer' : null)
  const expiresIn = payload.expires_in ?? payload.expiresIn ?? null
  const userPayload = payload.user ?? payload.profile ?? null

  return {
    accessToken,
    refreshToken,
    tokenType,
    expiresIn,
    user: normalizeUser(userPayload, fallbackUser),
    raw: payload
  }
}

export const registerUser = async (formData) => {
  if (!formData?.email) {
    throw new Error('Email қажет')
  }

  if (!formData?.password) {
    throw new Error('Пароль қажет')
  }

  const body = compactObject({
    email: formData.email,
    password: formData.password,
    role: formData.role || DEFAULT_ROLE,
    username: formData.username,
    firstName: formData.firstName,
    lastName: formData.lastName
  })

  const response = await apiPost('/auth/register', body)

  return {
    user: normalizeUser(response?.user, {
      email: formData.email,
      username: formData.username,
      firstName: formData.firstName,
      lastName: formData.lastName,
      role: body.role
    }),
    raw: response
  }
}

export const loginUser = async ({
  email,
  username,
  password,
  scope = '',
  grantType = 'password',
  clientId,
  clientSecret
}) => {
  const identifier = username || email

  if (!identifier) {
    throw new Error('Email немесе username қажет')
  }

  if (!password) {
    throw new Error('Пароль қажет')
  }

  const form = new URLSearchParams()
  form.append('username', identifier)
  form.append('password', password)
  form.append('grant_type', grantType)

  if (scope) {
    form.append('scope', scope)
  }

  if (clientId) {
    form.append('client_id', clientId)
  }

  if (clientSecret) {
    form.append('client_secret', clientSecret)
  }

  const response = await apiPost('/auth/login', form, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })

  return normalizeAuthResponse(response, {
    email,
    username
  })
}

export const refreshAuthToken = async (refreshToken) => {
  if (!refreshToken) {
    throw new Error('Refresh token қажет')
  }

  const response = await apiPost('/auth/refresh', {
    refresh_token: refreshToken
  })

  return normalizeAuthResponse(response)
}

