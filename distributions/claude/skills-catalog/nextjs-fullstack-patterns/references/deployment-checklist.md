# Next.js Production Deployment Checklist

Pre-launch and ongoing checklist for deploying Next.js applications to production.

## Pre-Deployment

### Build Validation

- [ ] `npm run build` completes without errors or warnings
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] Linting passes (`npm run lint`)
- [ ] All tests pass (`npm test`)
- [ ] Build output size is reasonable (check `.next/` size)

### Environment Variables

- [ ] All required env vars documented in `.env.example`
- [ ] Production values set in hosting platform (not committed)
- [ ] Validate env vars at startup with Zod:

```typescript
// lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  NEXTAUTH_URL: z.string().url(),
  NEXT_PUBLIC_APP_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);
```

- [ ] `NEXT_PUBLIC_*` vars are safe to expose to the browser
- [ ] No secrets in `NEXT_PUBLIC_*` variables

### Database

- [ ] Migrations applied (`npx prisma migrate deploy`)
- [ ] Connection pooling configured (e.g., PgBouncer, Neon pooler)
- [ ] Database backups enabled and tested
- [ ] Indexes on frequently queried columns

## Security

### Headers

Configure in `next.config.js`:

```javascript
const securityHeaders = [
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-XSS-Protection', value: '1; mode=block' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  {
    key: 'Content-Security-Policy',
    value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
  },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
];

module.exports = {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }];
  },
};
```

### Authentication & Authorization

- [ ] Auth middleware protects private routes
- [ ] CSRF protection enabled for mutations
- [ ] Session tokens are HttpOnly, Secure, SameSite=Lax
- [ ] Rate limiting on auth endpoints

### Data Validation

- [ ] Server Actions validate all inputs (never trust the client)
- [ ] API routes validate request bodies
- [ ] SQL injection prevented (use parameterized queries / ORM)

## Performance

- [ ] Images use `next/image` with width/height or fill
- [ ] Fonts loaded with `next/font` (no layout shift)
- [ ] Bundle analyzed (`npx @next/bundle-analyzer`)
- [ ] No unnecessary `'use client'` directives
- [ ] Dynamic imports for heavy components:

```typescript
const HeavyChart = dynamic(() => import('./Chart'), { ssr: false });
```

- [ ] Appropriate caching headers on API routes
- [ ] Static pages use ISR where possible

## SEO & Metadata

- [ ] Root layout has `<html lang="en">`
- [ ] Every page exports `metadata` or `generateMetadata`
- [ ] Open Graph and Twitter card meta tags set
- [ ] `robots.txt` exists (`app/robots.ts`)
- [ ] `sitemap.xml` generated (`app/sitemap.ts`)
- [ ] Canonical URLs configured

```typescript
// app/sitemap.ts
export default async function sitemap() {
  const posts = await getPosts();
  return [
    { url: 'https://myapp.com', lastModified: new Date() },
    ...posts.map(post => ({
      url: `https://myapp.com/posts/${post.slug}`,
      lastModified: post.updatedAt,
    })),
  ];
}
```

## Monitoring & Error Handling

- [ ] Error tracking configured (Sentry, LogRocket, etc.)
- [ ] Custom error pages: `app/error.tsx`, `app/not-found.tsx`, `app/global-error.tsx`
- [ ] Health check endpoint at `/api/health`
- [ ] Uptime monitoring configured
- [ ] Analytics installed (Vercel Analytics, Plausible, etc.)

## Deployment Platform

### Vercel

- [ ] Framework preset set to "Next.js"
- [ ] Environment variables configured per environment
- [ ] Custom domain added with SSL
- [ ] Preview deployments enabled for PRs
- [ ] Vercel Speed Insights enabled

### Self-Hosted (Docker)

- [ ] Multi-stage Dockerfile with `next start` as CMD
- [ ] `output: 'standalone'` in `next.config.js`
- [ ] `HOSTNAME=0.0.0.0` set for container networking
- [ ] Reverse proxy (nginx/caddy) configured with SSL

```javascript
// next.config.js (for Docker)
module.exports = {
  output: 'standalone',
};
```

## Post-Deployment

- [ ] Smoke test critical user flows manually
- [ ] Verify external service integrations (payments, email, etc.)
- [ ] Check Core Web Vitals in Chrome DevTools or PageSpeed Insights
- [ ] Confirm error tracking is receiving events
- [ ] Verify redirects and rewrites work correctly
- [ ] Test on mobile devices and slow networks

## Rollback Plan

- [ ] Previous deployment is one click away (Vercel: promote previous)
- [ ] Database migrations are backward-compatible
- [ ] Feature flags for risky features (`process.env.FEATURE_X_ENABLED`)
- [ ] Runbook documented for incident response
