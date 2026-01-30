# Next.js Patterns Reference

Common patterns for Next.js App Router applications.

## Data Fetching

### Server Components (Default)

```tsx
// app/users/page.tsx
async function UsersPage() {
  // Fetch directly in component - no useEffect needed
  const users = await db.user.findMany();

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Client Components

```tsx
'use client';

import { useState, useEffect } from 'react';

function SearchResults({ query }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetch(`/api/search?q=${query}`)
      .then(res => res.json())
      .then(setResults);
  }, [query]);

  return <ul>{results.map(r => <li key={r.id}>{r.title}</li>)}</ul>;
}
```

### When to Use Each

| Use Server Component | Use Client Component |
|---------------------|---------------------|
| Fetch data | useState, useEffect |
| Access backend resources | Event listeners |
| Keep secrets server-side | Browser APIs |
| Reduce client bundle | Interactivity |

## Route Handlers

### API Routes

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

### Dynamic Routes

```typescript
// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id }
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}
```

## Server Actions

### Form Actions

```tsx
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.post.create({
    data: { title, content }
  });

  revalidatePath('/posts');
}

// app/posts/new/page.tsx
import { createPost } from '@/app/actions';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### With useFormState

```tsx
'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { createPost } from '@/app/actions';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button disabled={pending}>
      {pending ? 'Creating...' : 'Create'}
    </button>
  );
}

export function CreatePostForm() {
  const [state, action] = useFormState(createPost, { error: null });

  return (
    <form action={action}>
      {state.error && <p className="error">{state.error}</p>}
      <input name="title" required />
      <SubmitButton />
    </form>
  );
}
```

## Caching & Revalidation

### Static Generation

```tsx
// Page is static by default
export default async function BlogPage() {
  const posts = await getPosts(); // Cached at build time
  return <PostList posts={posts} />;
}
```

### On-Demand Revalidation

```tsx
// In Server Action or Route Handler
import { revalidatePath, revalidateTag } from 'next/cache';

// Revalidate specific path
revalidatePath('/posts');

// Revalidate by tag
revalidateTag('posts');

// In fetch
const posts = await fetch('/api/posts', {
  next: { tags: ['posts'] }
});
```

### Time-Based Revalidation

```tsx
const posts = await fetch('/api/posts', {
  next: { revalidate: 60 } // Revalidate every 60 seconds
});
```

## Layouts & Templates

### Root Layout

```tsx
// app/layout.tsx
export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

### Nested Layouts

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <div className="dashboard">
      <Sidebar />
      <div className="content">{children}</div>
    </div>
  );
}
```

## Loading & Error States

### Loading UI

```tsx
// app/posts/loading.tsx
export default function Loading() {
  return <PostsSkeleton />;
}
```

### Error Handling

```tsx
// app/posts/error.tsx
'use client';

export default function Error({
  error,
  reset
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Not Found

```tsx
// app/posts/[id]/not-found.tsx
export default function NotFound() {
  return <div>Post not found</div>;
}

// In page.tsx
import { notFound } from 'next/navigation';

export default async function PostPage({ params }) {
  const post = await getPost(params.id);
  if (!post) notFound();
  return <Post post={post} />;
}
```

## Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token'); // allow-secret
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');
  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
};
```

## File Conventions

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI |
| `layout.tsx` | Shared layout |
| `loading.tsx` | Loading UI |
| `error.tsx` | Error UI |
| `not-found.tsx` | 404 UI |
| `route.ts` | API endpoint |
| `template.tsx` | Re-rendered layout |
| `default.tsx` | Parallel route fallback |
