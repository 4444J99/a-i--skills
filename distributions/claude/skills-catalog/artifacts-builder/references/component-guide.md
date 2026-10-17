# Artifacts Builder Component Guide

Available components and usage patterns for Claude.ai artifacts.

## Project Structure

After initialization:

```
my-artifact/
├── index.html          # Entry point (required for bundling)
├── src/
│   ├── main.tsx        # React entry point
│   ├── App.tsx         # Main component
│   └── components/     # Your components
├── components/
│   └── ui/             # shadcn/ui components (40+ pre-installed)
├── lib/
│   └── utils.ts        # cn() utility for class merging
├── tailwind.config.js
├── vite.config.ts
└── package.json
```

## Available shadcn/ui Components

All pre-installed and ready to use:

### Layout
- `Accordion` - Collapsible content sections
- `Card` - Container with header, content, footer
- `Collapsible` - Show/hide content
- `Resizable` - Resizable panels
- `ScrollArea` - Custom scrollbar styling
- `Separator` - Visual divider
- `Sheet` - Side drawer panel
- `Tabs` - Tabbed content

### Forms
- `Button` - Primary action element
- `Checkbox` - Boolean input
- `Input` - Text input
- `Label` - Form field label
- `RadioGroup` - Single selection
- `Select` - Dropdown selection
- `Slider` - Range input
- `Switch` - Toggle
- `Textarea` - Multi-line input

### Feedback
- `Alert` - Important messages
- `AlertDialog` - Confirmation dialogs
- `Badge` - Status indicators
- `Progress` - Loading progress
- `Skeleton` - Loading placeholder
- `Toast/Sonner` - Notifications
- `Tooltip` - Hover information

### Navigation
- `Breadcrumb` - Navigation trail
- `Command` - Command palette (⌘K)
- `ContextMenu` - Right-click menu
- `DropdownMenu` - Action menu
- `Menubar` - App menu bar
- `NavigationMenu` - Site navigation

### Data Display
- `Avatar` - User/entity image
- `Calendar` - Date picker
- `DataTable` - Sortable/filterable table
- `HoverCard` - Popup on hover
- `Popover` - Floating content
- `Table` - Data table

## Import Pattern

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
```

## Common Patterns

### Card with Form

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function SettingsCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Settings</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input id="name" placeholder="Enter name" />
        </div>
        <Button>Save Changes</Button>
      </CardContent>
    </Card>
  )
}
```

### Data Table with Actions

```tsx
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"

export function UserTable({ users }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
          <TableHead>Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {users.map(user => (
          <TableRow key={user.id}>
            <TableCell>{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell>
              <Button variant="ghost" size="sm">Edit</Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### Tabs with Content

```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function SettingsTabs() {
  return (
    <Tabs defaultValue="general">
      <TabsList>
        <TabsTrigger value="general">General</TabsTrigger>
        <TabsTrigger value="security">Security</TabsTrigger>
      </TabsList>
      <TabsContent value="general">
        General settings content
      </TabsContent>
      <TabsContent value="security">
        Security settings content
      </TabsContent>
    </Tabs>
  )
}
```

## Styling Tips

### Avoid "AI Slop"

```tsx
// ❌ Don't
<div className="flex items-center justify-center bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-8">
  <h1 className="text-4xl font-bold text-white text-center">Welcome!</h1>
</div>

// ✅ Do
<div className="max-w-2xl mx-auto p-6">
  <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
</div>
```

### Use the cn() Utility

```tsx
import { cn } from "@/lib/utils"

<Button className={cn(
  "w-full",
  isLoading && "opacity-50 cursor-not-allowed"
)}>
  Submit
</Button>
```

## Bundling Notes

The `bundle-artifact.sh` script:

1. Builds with Parcel (supports path aliases via `.parcelrc`)
2. Inlines all CSS and JS into single HTML
3. Creates `bundle.html` ready for Claude artifacts

Requirements:
- `index.html` must exist in project root
- React app must mount to an element in index.html
