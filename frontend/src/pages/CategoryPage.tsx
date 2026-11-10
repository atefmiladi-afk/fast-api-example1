import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import { ArrowLeft, Check, Volume2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { fetchCategory, updateProgress, type CategoryDetail, type Word } from "@/lib/api"

export function CategoryPage() {
  const { slug } = useParams()
  const [category, setCategory] = useState<CategoryDetail | null>(null)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!slug) return
    fetchCategory(slug)
      .then(setCategory)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load"))
  }, [slug])

  async function toggleLearned(word: Word) {
    const next = !word.learned
    await updateProgress(word.id, next)
    setCategory((prev) => {
      if (!prev) return prev
      const words = prev.words.map((w) => (w.id === word.id ? { ...w, learned: next } : w))
      return {
        ...prev,
        words,
        learned_count: words.filter((w) => w.learned).length,
      }
    })
  }

  function speak(text: string) {
    if (!window.speechSynthesis) return
    const utter = new SpeechSynthesisUtterance(text)
    utter.lang = "de-DE"
    window.speechSynthesis.cancel()
    window.speechSynthesis.speak(utter)
  }

  const pct = category?.word_count ? Math.round((category.learned_count / category.word_count) * 100) : 0

  return (
    <div className="min-h-screen">
      <header className="border-b bg-card/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center gap-4 px-6 py-4">
          <Button variant="outline" size="icon" asChild>
            <Link to="/learn">
              <ArrowLeft className="size-4" />
            </Link>
          </Button>
          <div className="flex-1">
            <p className="text-xs uppercase tracking-[0.25em] text-muted-foreground">{category?.name_en}</p>
            <h1 className="font-[Fraunces] text-2xl">{category?.name_de ?? "Loading..."}</h1>
          </div>
          <div className="hidden w-48 sm:block">
            <Progress value={pct} />
            <p className="mt-1 text-right text-xs text-muted-foreground">{pct}% learned</p>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">
        {error ? <p className="mb-6 text-sm text-destructive">{error}</p> : null}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {category?.words.map((word) => (
            <Card key={word.id} className="overflow-hidden">
              <div className="relative h-48">
                <img src={word.image_url} alt={word.english} className="h-full w-full object-cover" />
                {word.article ? (
                  <span className="absolute left-3 top-3 rounded-full bg-black/60 px-3 py-1 text-xs uppercase tracking-wide text-white">
                    {word.article}
                  </span>
                ) : null}
              </div>
              <div className="space-y-3 p-5">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="font-[Fraunces] text-2xl">
                      {word.article ? `${word.article} ` : ""}
                      {word.german}
                    </h2>
                    <p className="text-sm text-muted-foreground">{word.english}</p>
                  </div>
                  <Button variant="outline" size="icon" onClick={() => speak(word.german)} type="button">
                    <Volume2 className="size-4" />
                  </Button>
                </div>
                <p className="text-sm italic text-muted-foreground">
                  {word.example_de}
                  <span className="block not-italic">{word.example_en}</span>
                </p>
                <Button
                  className="w-full"
                  variant={word.learned ? "secondary" : "default"}
                  onClick={() => toggleLearned(word)}
                >
                  <Check className="size-4" />
                  {word.learned ? "Learned" : "Mark as learned"}
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </main>
    </div>
  )
}
