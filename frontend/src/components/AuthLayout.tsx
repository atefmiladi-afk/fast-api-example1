import type { ReactNode } from "react"

export function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen grid lg:grid-cols-2">
      <div className="relative hidden lg:block overflow-hidden bg-primary">
        <img
          src="https://images.unsplash.com/photo-1467269204594-9661b134dd2b?auto=format&fit=crop&w=1400&q=80"
          alt="German street"
          className="absolute inset-0 h-full w-full object-cover opacity-50"
        />
        <div className="relative z-10 flex h-full flex-col justify-between p-10 text-primary-foreground">
          <div className="text-sm tracking-[0.3em] uppercase">Deutsch Lernen</div>
          <div>
            <h1 className="font-[Fraunces] text-5xl leading-tight">Lerne Deutsch, ein Wort nach dem anderen.</h1>
            <p className="mt-4 max-w-md text-primary-foreground/85">
              Categories, pictures, and everyday vocabulary — start with Essen, Tiere, Familie, and more.
            </p>
          </div>
        </div>
      </div>
      <div className="flex items-center justify-center p-6 sm:p-10">{children}</div>
    </div>
  )
}
