# Rust Systems Design Patterns

Common patterns for systems programming in Rust.

## Ownership Patterns

### Builder Pattern

```rust
#[derive(Default)]
pub struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
}

impl ServerConfig {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = host.into();
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }

    pub fn max_connections(mut self, max: usize) -> Self {
        self.max_connections = max;
        self
    }

    pub fn build(self) -> Server {
        Server::new(self)
    }
}

// Usage
let server = ServerConfig::new()
    .host("localhost")
    .port(8080)
    .max_connections(100)
    .build();
```

### Newtype Pattern

```rust
// Wrapper type for type safety
pub struct UserId(u64);
pub struct OrderId(u64);

impl UserId {
    pub fn new(id: u64) -> Self {
        UserId(id)
    }

    pub fn inner(&self) -> u64 {
        self.0
    }
}

// Can't accidentally pass OrderId where UserId expected
fn get_user(id: UserId) -> User { ... }
```

### RAII (Resource Acquisition Is Initialization)

```rust
use std::fs::File;
use std::io::{self, Write};

struct TempFile {
    path: String,
    file: File,
}

impl TempFile {
    fn new(path: &str) -> io::Result<Self> {
        let file = File::create(path)?;
        Ok(TempFile {
            path: path.to_string(),
            file,
        })
    }
}

impl Drop for TempFile {
    fn drop(&mut self) {
        // Cleanup on scope exit
        let _ = std::fs::remove_file(&self.path);
    }
}
```

## Error Handling

### Custom Error Type

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, AppError>;
```

### Error Context

```rust
use anyhow::{Context, Result};

fn read_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context(format!("Failed to read config file: {}", path))?;

    let config: Config = toml::from_str(&content)
        .context("Failed to parse config")?;

    Ok(config)
}
```

## Async Patterns

### Async Trait

```rust
use async_trait::async_trait;

#[async_trait]
pub trait Repository {
    async fn find(&self, id: u64) -> Result<Option<Entity>>;
    async fn save(&self, entity: &Entity) -> Result<()>;
}

#[async_trait]
impl Repository for PostgresRepository {
    async fn find(&self, id: u64) -> Result<Option<Entity>> {
        // Implementation
    }

    async fn save(&self, entity: &Entity) -> Result<()> {
        // Implementation
    }
}
```

### Channel Communication

```rust
use tokio::sync::mpsc;

#[derive(Debug)]
enum Message {
    Process(String),
    Shutdown,
}

async fn worker(mut rx: mpsc::Receiver<Message>) {
    while let Some(msg) = rx.recv().await {
        match msg {
            Message::Process(data) => {
                println!("Processing: {}", data);
            }
            Message::Shutdown => {
                println!("Shutting down");
                break;
            }
        }
    }
}

#[tokio::main]
async fn main() {
    let (tx, rx) = mpsc::channel(100);

    let worker_handle = tokio::spawn(worker(rx));

    tx.send(Message::Process("Hello".into())).await.unwrap();
    tx.send(Message::Shutdown).await.unwrap();

    worker_handle.await.unwrap();
}
```

## Concurrency Patterns

### Arc + Mutex for Shared State

```rust
use std::sync::{Arc, Mutex};
use std::thread;

struct Counter {
    value: Mutex<u64>,
}

impl Counter {
    fn new() -> Self {
        Counter { value: Mutex::new(0) }
    }

    fn increment(&self) {
        let mut value = self.value.lock().unwrap();
        *value += 1;
    }

    fn get(&self) -> u64 {
        *self.value.lock().unwrap()
    }
}

let counter = Arc::new(Counter::new());
let handles: Vec<_> = (0..10).map(|_| {
    let counter = Arc::clone(&counter);
    thread::spawn(move || {
        counter.increment();
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}
```

### RwLock for Read-Heavy Workloads

```rust
use std::sync::RwLock;

struct Cache<T> {
    data: RwLock<HashMap<String, T>>,
}

impl<T: Clone> Cache<T> {
    fn get(&self, key: &str) -> Option<T> {
        let data = self.data.read().unwrap();
        data.get(key).cloned()
    }

    fn insert(&self, key: String, value: T) {
        let mut data = self.data.write().unwrap();
        data.insert(key, value);
    }
}
```

## Iterator Patterns

### Custom Iterator

```rust
struct Counter {
    count: usize,
    max: usize,
}

impl Iterator for Counter {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < self.max {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}

// Usage
for i in Counter { count: 0, max: 5 } {
    println!("{}", i);
}
```

### Iterator Combinators

```rust
let numbers = vec![1, 2, 3, 4, 5];

let result: Vec<_> = numbers
    .iter()
    .filter(|&n| n % 2 == 0)
    .map(|n| n * 2)
    .collect();

// Parallel with rayon
use rayon::prelude::*;

let result: Vec<_> = numbers
    .par_iter()
    .filter(|&n| n % 2 == 0)
    .map(|n| n * 2)
    .collect();
```

## Memory Patterns

### Zero-Copy Parsing

```rust
use nom::{bytes::complete::tag, IResult};

fn parse_header(input: &[u8]) -> IResult<&[u8], &[u8]> {
    tag(b"HEADER:")(input)
}

// Returns slices into original data, no allocation
```

### Arena Allocation

```rust
use bumpalo::Bump;

fn process_with_arena() {
    let arena = Bump::new();

    // All allocations freed when arena dropped
    let data = arena.alloc_slice_copy(&[1, 2, 3, 4, 5]);
    let string = arena.alloc_str("hello");
}
```

## Testing Patterns

### Property-Based Testing

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reverse_reverse(s in ".*") {
        let reversed: String = s.chars().rev().collect();
        let double_reversed: String = reversed.chars().rev().collect();
        assert_eq!(s, double_reversed);
    }
}
```

### Mock with Trait

```rust
#[cfg(test)]
mod tests {
    use super::*;

    struct MockRepository {
        users: Vec<User>,
    }

    impl Repository for MockRepository {
        fn find(&self, id: u64) -> Option<&User> {
            self.users.iter().find(|u| u.id == id)
        }
    }

    #[test]
    fn test_find_user() {
        let repo = MockRepository {
            users: vec![User { id: 1, name: "Test".into() }],
        };
        assert!(repo.find(1).is_some());
    }
}
```
