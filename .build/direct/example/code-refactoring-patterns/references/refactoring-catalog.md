# Refactoring Catalog

Common refactoring patterns with before/after examples.

## Extract Method

**When**: Code block does one thing and can be named.

```typescript
// Before
function printInvoice(invoice) {
  console.log("--- Invoice ---");
  let total = 0;
  for (const item of invoice.items) {
    total += item.price * item.quantity;
  }
  console.log(`Total: $${total}`);
}

// After
function printInvoice(invoice) {
  console.log("--- Invoice ---");
  const total = calculateTotal(invoice.items);
  console.log(`Total: $${total}`);
}

function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

## Extract Variable

**When**: Complex expression is hard to understand.

```typescript
// Before
if (user.age >= 18 && user.country === 'US' && user.hasValidId && !user.isBanned) {
  allowAccess();
}

// After
const isAdult = user.age >= 18;
const isFromUS = user.country === 'US';
const hasRequiredDocuments = user.hasValidId;
const isInGoodStanding = !user.isBanned;

if (isAdult && isFromUS && hasRequiredDocuments && isInGoodStanding) {
  allowAccess();
}
```

## Replace Conditional with Polymorphism

**When**: Switch/if statements select behavior based on type.

```typescript
// Before
function calculatePay(employee) {
  switch (employee.type) {
    case 'hourly':
      return employee.hours * employee.rate;
    case 'salaried':
      return employee.salary / 12;
    case 'commission':
      return employee.sales * employee.commissionRate;
  }
}

// After
class HourlyEmployee {
  calculatePay() {
    return this.hours * this.rate;
  }
}

class SalariedEmployee {
  calculatePay() {
    return this.salary / 12;
  }
}

class CommissionEmployee {
  calculatePay() {
    return this.sales * this.commissionRate;
  }
}
```

## Replace Magic Number with Constant

**When**: Numbers have meaning that isn't obvious.

```typescript
// Before
if (temperature > 100) {
  shutdown();
}

// After
const MAX_SAFE_TEMPERATURE = 100;
if (temperature > MAX_SAFE_TEMPERATURE) {
  shutdown();
}
```

## Introduce Parameter Object

**When**: Multiple parameters travel together.

```typescript
// Before
function searchEvents(startDate, endDate, minPrice, maxPrice, category) {
  // ...
}

// After
interface EventSearchParams {
  dateRange: { start: Date; end: Date };
  priceRange: { min: number; max: number };
  category?: string;
}

function searchEvents(params: EventSearchParams) {
  // ...
}
```

## Replace Nested Conditionals with Guard Clauses

**When**: Deep nesting makes flow hard to follow.

```typescript
// Before
function processPayment(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.paymentMethod) {
        if (order.paymentMethod.isValid) {
          return charge(order);
        } else {
          return { error: 'Invalid payment method' };
        }
      } else {
        return { error: 'No payment method' };
      }
    } else {
      return { error: 'Empty order' };
    }
  } else {
    return { error: 'No order' };
  }
}

// After
function processPayment(order) {
  if (!order) return { error: 'No order' };
  if (order.items.length === 0) return { error: 'Empty order' };
  if (!order.paymentMethod) return { error: 'No payment method' };
  if (!order.paymentMethod.isValid) return { error: 'Invalid payment method' };

  return charge(order);
}
```

## Decompose Conditional

**When**: Complex condition is hard to understand.

```typescript
// Before
if (date.before(SUMMER_START) || date.after(SUMMER_END)) {
  charge = quantity * winterRate + winterServiceCharge;
} else {
  charge = quantity * summerRate;
}

// After
function isWinter(date) {
  return date.before(SUMMER_START) || date.after(SUMMER_END);
}

function winterCharge(quantity) {
  return quantity * winterRate + winterServiceCharge;
}

function summerCharge(quantity) {
  return quantity * summerRate;
}

charge = isWinter(date) ? winterCharge(quantity) : summerCharge(quantity);
```

## Move Method

**When**: Method uses more features of another class.

```typescript
// Before
class Order {
  getDiscountedPrice() {
    return this.price * (1 - this.customer.getDiscountRate());
  }
}

// After
class Customer {
  getDiscountedPrice(price) {
    return price * (1 - this.getDiscountRate());
  }
}

class Order {
  getDiscountedPrice() {
    return this.customer.getDiscountedPrice(this.price);
  }
}
```

## Replace Constructor with Factory Method

**When**: Need more flexibility in object creation.

```typescript
// Before
const employee = new Employee(type, name, salary);

// After
class Employee {
  static createEngineer(name) {
    return new Employee('engineer', name, 80000);
  }

  static createManager(name) {
    return new Employee('manager', name, 100000);
  }
}

const engineer = Employee.createEngineer('Alice');
```

## Replace Temp with Query

**When**: Temporary variable holds a computation that could be a method.

```typescript
// Before
function calculateTotal() {
  const basePrice = quantity * itemPrice;
  if (basePrice > 1000) {
    return basePrice * 0.95;
  }
  return basePrice;
}

// After
function basePrice() {
  return quantity * itemPrice;
}

function calculateTotal() {
  if (basePrice() > 1000) {
    return basePrice() * 0.95;
  }
  return basePrice();
}
```

## When to Refactor

| Signal | Refactoring |
|--------|-------------|
| Duplicated code | Extract Method |
| Long method | Extract Method, Decompose |
| Long parameter list | Parameter Object |
| Data clumps | Extract Class |
| Feature envy | Move Method |
| Switch statements | Polymorphism |
| Parallel inheritance | Move Method/Field |
| Comments explaining code | Extract Method (name explains) |
| Dead code | Delete it |

## Refactoring Safety

1. **Have tests first** - Don't refactor without tests
2. **Small steps** - One refactoring at a time
3. **Run tests after each change** - Catch breaks early
4. **Commit frequently** - Easy to revert
5. **No behavior changes** - Refactoring changes structure only
