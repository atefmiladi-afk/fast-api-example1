import { useEffect, useState } from "react"
import { Link, useSearchParams } from "react-router-dom"
import { AuthLayout } from "@/components/AuthLayout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { resendVerification, verifyEmail } from "@/lib/api"

export function VerifyEmailPage() {
  const [params] = useSearchParams()
  const token = params.get("token") || ""
  const [status, setStatus] = useState(token ? "verifying" : "idle")
  const [message, setMessage] = useState("")
  const [email, setEmail] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!token) return
    verifyEmail(token)
      .then((data) => {
        setStatus("ok")
        setMessage(data.message)
      })
      .catch((err) => {
        setStatus("error")
        setMessage(err instanceof Error ? err.message : "Verification failed")
      })
  }, [token])

  async function onResend() {
    setLoading(true)
    try {
      const data = await resendVerification(email)
      setMessage(data.message)
      setStatus("ok")
    } catch (err) {
      setStatus("error")
      setMessage(err instanceof Error ? err.message : "Request failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout>
      <Card className="w-full max-w-md">
        <CardHeader>
          <p className="text-xs uppercase tracking-[0.25em] text-muted-foreground">E-Mail bestatigen</p>
          <CardTitle className="font-[Fraunces] text-3xl">Verify email</CardTitle>
          <CardDescription>Confirm your address to activate the account.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {status === "verifying" ? <p className="text-sm text-muted-foreground">Verifying...</p> : null}
          {message ? (
            <p className={`text-sm ${status === "error" ? "text-destructive" : "text-primary"}`}>{message}</p>
          ) : null}
          <div className="space-y-2">
            <Label htmlFor="email">Resend verification</Label>
            <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@email.com" />
            <Button className="w-full" type="button" onClick={onResend} disabled={loading || !email}>
              {loading ? "Sending..." : "Send new link"}
            </Button>
          </div>
          <p className="text-center text-sm text-muted-foreground">
            <Link to="/login" className="text-primary underline-offset-4 hover:underline">
              Back to sign in
            </Link>
          </p>
        </CardContent>
      </Card>
    </AuthLayout>
  )
}
