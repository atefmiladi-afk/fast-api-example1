import type { ReactNode } from "react"
import { Navigate, Route, Routes } from "react-router-dom"
import { getToken } from "@/lib/api"
import { CategoryPage } from "@/pages/CategoryPage"
import { LearnPage } from "@/pages/LearnPage"
import { LoginPage } from "@/pages/LoginPage"
import { RegisterPage } from "@/pages/RegisterPage"

function Protected({ children }: { children: ReactNode }) {
  if (!getToken()) return <Navigate to="/login" replace />
  return children
}

function Guest({ children }: { children: ReactNode }) {
  if (getToken()) return <Navigate to="/learn" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/learn" replace />} />
      <Route
        path="/login"
        element={
          <Guest>
            <LoginPage />
          </Guest>
        }
      />
      <Route
        path="/register"
        element={
          <Guest>
            <RegisterPage />
          </Guest>
        }
      />
      <Route
        path="/learn"
        element={
          <Protected>
            <LearnPage />
          </Protected>
        }
      />
      <Route
        path="/learn/:slug"
        element={
          <Protected>
            <CategoryPage />
          </Protected>
        }
      />
      <Route path="*" element={<Navigate to="/learn" replace />} />
    </Routes>
  )
}
