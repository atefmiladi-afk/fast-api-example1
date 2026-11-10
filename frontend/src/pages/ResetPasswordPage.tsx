import { type FormEvent, useState } from "react"
import { Link, useSearchParams } from "react-router-dom"
import { AuthLayout } from "@/components/AuthLayout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { resetPassword } from "@/lib/api"

export function ResetPasswordPage() {
  const [params] = useSearchParams()
  const token = params.get("token") || ""
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError("")
    setMessage("")
    setLoading(true)
    try {
      const data = await resetPassword(token, password)
      setMessage(data.message)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Reset failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout>
      <Card className="w-full max-w-md">
        <CardHeader>
          <p className="text-xs uppercase tracking-[0.25em] text-muted-foreground">Neues Passwort</p>
          <CardTitle className="font-[Fraunces] text-3xl">Choose a new password</CardTitle>
          <CardDescription>Use the link from your email to set a new password.</CardDescription>
        </CardHeader>
        <CardContent>
          {!token ? (
            <p className="text-sm text-destructive">Missing reset token. Request a new link from the login page.</p>
          ) : (
            <form className="space-y-4" onSubmit={onSubmit}>
              <div className="space-y-2">
                <Label htmlFor="password">New password</Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  minLength={6}
                  required
                />
              </div>
              {error ? <p className="text-sm text-destructive">{error}</p> : null}
              {message ? <p className="text-sm text-primary">{message}</p> : null}
              <Button className="w-full" type="submit" disabled={loading}>
                {loading ? "Updating..." : "Update password"}
              </Button>
            </form>
          )}
          <p className="mt-4 text-center text-sm text-muted-foreground">
            <Link to="/login" className="text-primary underline-offset-4 hover:underline">
              Back to sign in
            </Link>
          </p>
        </CardContent>
      </Card>
    </AuthLayout>
  )
}
