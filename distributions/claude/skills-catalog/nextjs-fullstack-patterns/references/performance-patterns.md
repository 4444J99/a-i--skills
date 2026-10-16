# Next.js Performance Optimization

Techniques for fast load times, efficient rendering, and optimal Core Web Vitals.

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |

## Server Components (Reduce Client JS)

Keep components on the server by default. Only add `'use client'` when needed.

```tsx
// Server Component: zero JS shipped to client
async function ProductList() {
  const products = await db.product.findMany();
  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name} - ${p.price}</li>)}
    </ul>
  );
}

// Push 'use client' to the leaf
// Bad: entire page is a client component
// Good: only the interactive piece is client
import { AddToCartButton } from './AddToCartButton'; // 'use client'

async function ProductPage({ params }) {
  const product = await getProduct(params.id);
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />
    </div>
  );
}
```

## Image Optimization

```tsx
import Image from 'next/image';

// Always specify dimensions to prevent layout shift
<Image
  src="/hero.jpg"
  alt="Hero banner"
  width={1200}
  height={600}
  priority          // LCP image: preload
  placeholder="blur" // Show blurred preview while loading
  blurDataURL="data:image/jpeg;base64,..."
/>

// Responsive images
<Image
  src="/photo.jpg"
  alt="Photo"
  fill
  sizes="(max-width: 768px) 100vw, 50vw"
  className="object-cover"
/>
```

| Prop | When to Use |
|------|-------------|
| `priority` | Above-the-fold LCP image |
| `loading="lazy"` | Default for below-fold images |
| `placeholder="blur"` | Improve perceived load time |
| `sizes` | With `fill` or responsive layouts |

## Font Optimization

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',     // Prevent invisible text
  variable: '--font-inter',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

`next/font` self-hosts fonts, eliminating external network requests.

## Dynamic Imports

```typescript
import dynamic from 'next/dynamic';

// Heavy component: only load when rendered
const Chart = dynamic(() => import('@/components/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,  // Skip SSR for browser-only libraries
});

// Conditional import
const AdminPanel = dynamic(() => import('@/components/AdminPanel'));

function Dashboard({ isAdmin }) {
  return (
    <div>
      <Stats />
      {isAdmin && <AdminPanel />}
    </div>
  );
}
```

## Streaming and Suspense

```tsx
import { Suspense } from 'react';

// Shell renders immediately; slow parts stream in
export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <QuickStats />  {/* Fast: renders with shell */}

      <Suspense fallback={<RevenueChartSkeleton />}>
        <RevenueChart />  {/* Slow: streams when ready */}
      </Suspense>

      <Suspense fallback={<ActivityFeedSkeleton />}>
        <ActivityFeed />
      </Suspense>
    </div>
  );
}
```

## Caching Strategy

### Fetch Caching

```typescript
// Static: cached indefinitely (default in Server Components)
const data = await fetch('https://api.example.com/config');

// Revalidate every 60 seconds (ISR)
const data = await fetch('https://api.example.com/posts', {
  next: { revalidate: 60 },
});

// No cache: always fresh
const data = await fetch('https://api.example.com/user', {
  cache: 'no-store',
});

// Tag-based revalidation
const data = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] },
});

// Revalidate on demand (in a Server Action)
revalidateTag('posts');
```

### React `cache()` for Deduplication

```typescript
import { cache } from 'react';

// Called in multiple components but runs only once per request
export const getUser = cache(async (id: string) => {
  return db.user.findUnique({ where: { id } });
});
```

## Route Segment Config

```typescript
// Force dynamic rendering
export const dynamic = 'force-dynamic';

// Or force static
export const dynamic = 'force-static';

// Revalidation interval
export const revalidate = 3600; // 1 hour

// Runtime
export const runtime = 'edge'; // or 'nodejs'
```

## Bundle Analysis

```bash
npm install -D @next/bundle-analyzer
```

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({ /* config */ });
```

```bash
ANALYZE=true npm run build
```

Common fixes:

| Issue | Solution |
|-------|----------|
| Large library in client bundle | Dynamic import with `ssr: false` |
| Moment.js (300kb) | Switch to dayjs (2kb) or date-fns |
| Icon library (full import) | Import specific icons: `from 'lucide-react/icons/X'` |
| Unused dependencies | `npx depcheck` to find and remove |

## Parallel Data Fetching

```tsx
// Bad: sequential (waterfall)
const user = await getUser(id);
const posts = await getPosts(id);

// Good: parallel
const [user, posts] = await Promise.all([
  getUser(id),
  getPosts(id),
]);
```

## Metadata for Performance

```typescript
// Preconnect to external origins
export const metadata = {
  other: {
    'link': [
      { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
      { rel: 'dns-prefetch', href: 'https://api.analytics.com' },
    ],
  },
};
```

## Measurement

- **Vercel Speed Insights**: Real user monitoring built in
- **PageSpeed Insights**: Lab + field data from Google
- **Chrome DevTools**: Performance tab for detailed traces
- **`next/web-vitals`**: Report CWV from your app

```typescript
// app/layout.tsx
export function reportWebVitals(metric) {
  console.log(metric); // or send to analytics
}
```
