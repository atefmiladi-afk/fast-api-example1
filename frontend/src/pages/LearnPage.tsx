import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { clearSession, fetchCategories, getStoredUser, type Category } from "@/lib/api"

export function LearnPage() {
  const navigate = useNavigate()
  const user = getStoredUser()
  const [categories, setCategories] = useState<Category[]>([])
  const [error, setError] = useState("")

  useEffect(() => {
    fetchCategories()
      .then(setCategories)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load"))
  }, [])

  function logout() {
    clearSession()
    navigate("/login")
  }

  return (
    <div className="min-h-screen">
      <header className="border-b bg-card/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-muted-foreground">Deutsch Lernen</p>
            <h1 className="font-[Fraunces] text-2xl">Choose a category</h1>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-muted-foreground sm:inline">{user?.username}</span>
            <Button variant="outline" size="sm" onClick={logout}>
              <LogOut className="size-4" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">
        {error ? <p className="mb-6 text-sm text-destructive">{error}</p> : null}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((cat) => {
            const pct = cat.word_count ? Math.round((cat.learned_count / cat.word_count) * 100) : 0
            return (
              <Link key={cat.slug} to={`/learn/${cat.slug}`} className="group">
                <Card className="overflow-hidden transition-transform group-hover:-translate-y-1">
                  <div className="relative h-40 overflow-hidden">
                    <img src={cat.image_url} alt={cat.name_en} className="h-full w-full object-cover transition-transform group-hover:scale-105" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/55 to-transparent" />
                    <div className="absolute bottom-3 left-4 text-white">
                      <p className="text-xs uppercase tracking-widest">{cat.name_en}</p>
                      <h2 className="font-[Fraunces] text-2xl">{cat.name_de}</h2>
                    </div>
                  </div>
                  <CardContent className="space-y-3 pt-4">
                    <p className="text-sm text-muted-foreground">{cat.description}</p>
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>
                        {cat.learned_count}/{cat.word_count} learned
                      </span>
                      <span>{pct}%</span>
                    </div>
                    <Progress value={pct} />
                  </CardContent>
                </Card>
              </Link>
            )
          })}
        </div>
      </main>
    </div>
  )
}
