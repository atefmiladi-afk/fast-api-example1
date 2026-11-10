const TOKEN_KEY = "deutsch_token"
const USER_KEY = "deutsch_user"

export type User = {
  id: number
  username: string
  email: string
  created_at: string
}

export type Word = {
  id: number
  german: string
  article: string
  english: string
  example_de: string
  example_en: string
  image_url: string
  audio_hint: string
  learned: boolean
}

export type Category = {
  id: number
  slug: string
  name_de: string
  name_en: string
  description: string
  emoji: string
  color: string
  image_url: string
  word_count: number
  learned_count: number
}

export type CategoryDetail = Category & { words: Word[] }

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function getStoredUser(): User | null {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as User
  } catch {
    return null
  }
}

export function setSession(token: string, user: User) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken()
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  }
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(path, { ...options, headers })
  if (!res.ok) {
    let message = "Request failed"
    try {
      const body = await res.json()
      message = body.detail || message
    } catch {
      /* ignore */
    }
    throw new Error(message)
  }
  return res.json() as Promise<T>
}

export function register(username: string, email: string, password: string) {
  return request<{ access_token: string; user: User }>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  })
}

export function login(username: string, password: string) {
  return request<{ access_token: string; user: User }>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  })
}

export function fetchCategories() {
  return request<Category[]>("/api/categories")
}

export function fetchCategory(slug: string) {
  return request<CategoryDetail>(`/api/categories/${slug}`)
}

export function updateProgress(wordId: number, learned: boolean) {
  return request<{ word_id: number; learned: boolean }>(`/api/progress/${wordId}`, {
    method: "PUT",
    body: JSON.stringify({ learned }),
  })
}
