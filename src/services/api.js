const DEFAULT_BASE_URL = import.meta.env.DEV
    ? 'http://localhost:8000/api/v1'
    : '/api/v1'
const AUTH_STORAGE_KEY = 'skillgig_auth'
const normalizeTokenType = (type) => {
    if (!type) {
        return null
    }

    if (typeof type === 'string' && type.toLowerCase() === 'bearer') {
        return 'Bearer'
    }

    return type
}

const normalizeBaseUrl = (url) => {
    if (!url) return DEFAULT_BASE_URL
    return url.endsWith('/') ? url.slice(0, -1) : url
}

const API_BASE_URL = normalizeBaseUrl(import.meta.env.VITE_API_URL)

const buildUrl = (path) => {
    if (!path) throw new Error('API path is required')
    if (path.startsWith('http://') || path.startsWith('https://')) {
        return path
    }
    return `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`
}

const parseResponse = async (response) => {
    if (response.status === 204) {
        return null
    }

    const text = await response.text()
    if (!text) {
        return null
    }

    try {
        return JSON.parse(text)
    } catch {
        return text
    }
}

const isSerializableObject = (value) => {
    if (!value || typeof value !== 'object') {
        return false
    }

    if (value instanceof FormData) {
        return false
    }

    if (typeof URLSearchParams !== 'undefined' && value instanceof URLSearchParams) {
        return false
    }

    if (typeof Blob !== 'undefined' && value instanceof Blob) {
        return false
    }

    return true
}

const getStoredAuthHeader = () => {
    if (typeof window === 'undefined') {
        return null
    }

    try {
        const raw = window.localStorage.getItem(AUTH_STORAGE_KEY)
        if (!raw) {
            return null
        }

        const parsed = JSON.parse(raw)
        if (parsed?.accessToken) {
            const tokenType = normalizeTokenType(
                parsed?.tokenType ||
                parsed?.token_type ||
                (parsed?.accessToken ? 'Bearer' : null)
            )
            if (tokenType) {
                return `${tokenType} ${parsed.accessToken}`
            }
        }

        if (parsed?.token) {
            return `Bearer ${parsed.token}`
        }

        return null
    } catch {
        return null
    }
}

const request = async (path, options = {}) => {
    const url = buildUrl(path)
    const { headers, body, ...rest } = options
    const shouldSerializeBody = isSerializableObject(body)

    const defaultHeaders = {
        Accept: 'application/json',
        ...(shouldSerializeBody ? { 'Content-Type': 'application/json' } : {})
    }

    const authHeader =
        headers?.Authorization || headers?.authorization || getStoredAuthHeader()

    const mergedHeaders = {
        ...defaultHeaders,
        ...headers
    }

    if (authHeader && !mergedHeaders.Authorization) {
        mergedHeaders.Authorization = authHeader
    }

    const init = {
        headers: mergedHeaders,
        body: shouldSerializeBody ? JSON.stringify(body) : body,
        ...rest
    }

    const response = await fetch(url, init)
    const payload = await parseResponse(response)

    if (!response.ok) {
        const message =
            (payload && payload.detail) ||
            (payload && payload.message) ||
            response.statusText ||
            'API request failed'
        const error = new Error(message)
        error.status = response.status
        error.payload = payload
        throw error
    }

    return payload
}

export const apiGet = (path, options) =>
    request(path, { method: 'GET', ...options })

export const apiPost = (path, body, options) =>
    request(path, { method: 'POST', body, ...options })

export const apiPatch = (path, body, options) =>
    request(path, { method: 'PATCH', body, ...options })

export const apiPut = (path, body, options) =>
    request(path, { method: 'PUT', body, ...options })

export const apiDelete = (path, options) =>
    request(path, { method: 'DELETE', ...options })

export const apiBaseUrl = API_BASE_URL

export default {
    get: apiGet,
    post: apiPost,
    patch: apiPatch,
    put: apiPut,
    delete: apiDelete
}

