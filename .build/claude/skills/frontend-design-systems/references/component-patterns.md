# Frontend Component Patterns

Patterns for building scalable design system components.

## Component Hierarchy

```
Tokens (Design Tokens)
    │
    ▼
Primitives (Base Components)
    │
    ▼
Components (UI Components)
    │
    ▼
Patterns (Component Combinations)
    │
    ▼
Templates (Page Layouts)
```

## Design Tokens

### Token Categories

```css
/* Colors */
--color-primary-500: #3b82f6;
--color-gray-100: #f3f4f6;

/* Typography */
--font-family-sans: 'Inter', sans-serif;
--font-size-base: 1rem;
--line-height-normal: 1.5;

/* Spacing */
--spacing-1: 0.25rem;
--spacing-2: 0.5rem;
--spacing-4: 1rem;

/* Borders */
--radius-sm: 0.25rem;
--radius-md: 0.375rem;

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);

/* Transitions */
--transition-fast: 150ms ease;
```

### Token Usage

```tsx
// Use tokens via CSS custom properties
const Button = styled.button`
  background: var(--color-primary-500);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);
`;
```

## Component API Patterns

### Composition Pattern

```tsx
// Good: Composable components
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Footer</Card.Footer>
</Card>

// Implementation
const Card = ({ children }) => <div className="card">{children}</div>;
Card.Header = ({ children }) => <div className="card-header">{children}</div>;
Card.Body = ({ children }) => <div className="card-body">{children}</div>;
Card.Footer = ({ children }) => <div className="card-footer">{children}</div>;
```

### Slot Pattern

```tsx
// Component with named slots
<Dialog>
  <Dialog.Trigger asChild>
    <Button>Open</Button>
  </Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Title>Are you sure?</Dialog.Title>
    <Dialog.Description>This cannot be undone.</Dialog.Description>
    <Dialog.Close asChild>
      <Button>Cancel</Button>
    </Dialog.Close>
  </Dialog.Content>
</Dialog>
```

### Render Props

```tsx
// Flexible rendering control
<Toggle>
  {({ isOn, toggle }) => (
    <button onClick={toggle}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  )}
</Toggle>
```

### Polymorphic Components

```tsx
// Component can render as different elements
<Button as="a" href="/link">Link Button</Button>
<Button as="button" onClick={handler}>Button</Button>
<Button as={Link} to="/route">Router Link</Button>

// Implementation
interface ButtonProps<C extends React.ElementType = 'button'> {
  as?: C;
  children: React.ReactNode;
}

function Button<C extends React.ElementType = 'button'>({
  as,
  children,
  ...props
}: ButtonProps<C> & React.ComponentPropsWithoutRef<C>) {
  const Component = as || 'button';
  return <Component {...props}>{children}</Component>;
}
```

## Variant Patterns

### Using CVA (Class Variance Authority)

```tsx
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        secondary: 'bg-secondary text-secondary-foreground',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        destructive: 'bg-destructive text-destructive-foreground',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = ({ variant, size, className, ...props }: ButtonProps) => (
  <button className={buttonVariants({ variant, size, className })} {...props} />
);
```

## State Patterns

### Controlled vs Uncontrolled

```tsx
// Controlled: Parent manages state
function ControlledInput({ value, onChange }) {
  return <input value={value} onChange={onChange} />;
}

// Uncontrolled: Component manages state internally
function UncontrolledInput({ defaultValue, onValueChange }) {
  const [value, setValue] = useState(defaultValue);

  const handleChange = (e) => {
    setValue(e.target.value);
    onValueChange?.(e.target.value);
  };

  return <input value={value} onChange={handleChange} />;
}

// Hybrid: Support both modes
function HybridInput({ value, defaultValue, onChange }) {
  const isControlled = value !== undefined;
  const [internalValue, setInternalValue] = useState(defaultValue);

  const currentValue = isControlled ? value : internalValue;

  const handleChange = (e) => {
    if (!isControlled) setInternalValue(e.target.value);
    onChange?.(e.target.value);
  };

  return <input value={currentValue} onChange={handleChange} />;
}
```

## Accessibility Patterns

### Focus Management

```tsx
// Focus trap for modals
function Dialog({ isOpen, children }) {
  const dialogRef = useRef();

  useEffect(() => {
    if (isOpen) {
      const focusable = dialogRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      focusable[0]?.focus();
    }
  }, [isOpen]);

  return (
    <div ref={dialogRef} role="dialog" aria-modal="true">
      {children}
    </div>
  );
}
```

### Keyboard Navigation

```tsx
// Arrow key navigation
function Listbox({ items, onSelect }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex((i) => Math.min(i + 1, items.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex((i) => Math.max(i - 1, 0));
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        onSelect(items[activeIndex]);
        break;
    }
  };

  return (
    <ul role="listbox" onKeyDown={handleKeyDown}>
      {items.map((item, index) => (
        <li
          key={item.id}
          role="option"
          aria-selected={index === activeIndex}
          tabIndex={index === activeIndex ? 0 : -1}
        >
          {item.label}
        </li>
      ))}
    </ul>
  );
}
```

## File Organization

```
components/
├── ui/                    # Primitives
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   └── index.ts
│   └── Input/
│
├── patterns/              # Composed components
│   ├── SearchBar/
│   └── DataTable/
│
└── index.ts               # Public exports
```
