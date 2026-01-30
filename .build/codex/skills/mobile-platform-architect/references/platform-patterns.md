# Mobile Platform Patterns

Architecture patterns for iOS, Android, and cross-platform development.

## Architecture Patterns

### MVVM (Model-View-ViewModel)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    View     │ ←── │  ViewModel  │ ←── │    Model    │
│   (UI)      │     │  (Logic)    │     │   (Data)    │
└─────────────┘     └─────────────┘     └─────────────┘
     │                    │
     │    Data Binding    │
     └────────────────────┘
```

**Swift/iOS:**
```swift
class UserViewModel: ObservableObject {
    @Published var user: User?
    @Published var isLoading = false

    func fetchUser(id: String) {
        isLoading = true
        userService.fetch(id: id) { [weak self] result in
            self?.isLoading = false
            self?.user = result
        }
    }
}

struct UserView: View {
    @StateObject var viewModel = UserViewModel()

    var body: some View {
        if viewModel.isLoading {
            ProgressView()
        } else {
            Text(viewModel.user?.name ?? "")
        }
    }
}
```

**Kotlin/Android:**
```kotlin
class UserViewModel(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    fun fetchUser(id: String) {
        viewModelScope.launch {
            _isLoading.value = true
            _user.value = userRepository.getUser(id)
            _isLoading.value = false
        }
    }
}
```

### Clean Architecture

```
┌─────────────────────────────────────────┐
│           Presentation Layer             │
│    (ViewModels, Controllers, Views)      │
├─────────────────────────────────────────┤
│             Domain Layer                 │
│      (Use Cases, Entities, Repos)        │
├─────────────────────────────────────────┤
│              Data Layer                  │
│   (API, Database, Repository Impl)       │
└─────────────────────────────────────────┘
```

**Dependency Rule:** Dependencies point inward only.

## Navigation Patterns

### Coordinator Pattern (iOS)

```swift
protocol Coordinator {
    var navigationController: UINavigationController { get }
    func start()
}

class AppCoordinator: Coordinator {
    var navigationController: UINavigationController

    init(navigationController: UINavigationController) {
        self.navigationController = navigationController
    }

    func start() {
        let loginVC = LoginViewController()
        loginVC.coordinator = self
        navigationController.pushViewController(loginVC, animated: false)
    }

    func showHome() {
        let homeVC = HomeViewController()
        navigationController.pushViewController(homeVC, animated: true)
    }
}
```

### Navigation Component (Android)

```kotlin
// nav_graph.xml
<navigation xmlns:android="..."
    app:startDestination="@id/loginFragment">

    <fragment
        android:id="@+id/loginFragment"
        android:name="com.app.LoginFragment">
        <action
            android:id="@+id/action_login_to_home"
            app:destination="@id/homeFragment" />
    </fragment>

    <fragment
        android:id="@+id/homeFragment"
        android:name="com.app.HomeFragment" />
</navigation>

// Usage
findNavController().navigate(R.id.action_login_to_home)
```

## State Management

### Redux-like (React Native)

```typescript
// Store
interface AppState {
    user: User | null;
    isLoading: boolean;
}

// Actions
type Action =
    | { type: 'SET_USER'; payload: User }
    | { type: 'SET_LOADING'; payload: boolean }
    | { type: 'LOGOUT' };

// Reducer
function appReducer(state: AppState, action: Action): AppState {
    switch (action.type) {
        case 'SET_USER':
            return { ...state, user: action.payload };
        case 'SET_LOADING':
            return { ...state, isLoading: action.payload };
        case 'LOGOUT':
            return { user: null, isLoading: false };
    }
}
```

### Combine (iOS)

```swift
class Store: ObservableObject {
    @Published var user: User?
    @Published var isLoading = false

    private var cancellables = Set<AnyCancellable>()

    func fetchUser() {
        isLoading = true
        userService.fetchUser()
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { [weak self] _ in
                    self?.isLoading = false
                },
                receiveValue: { [weak self] user in
                    self?.user = user
                }
            )
            .store(in: &cancellables)
    }
}
```

## Networking Patterns

### Repository Pattern

```kotlin
interface UserRepository {
    suspend fun getUser(id: String): User
    suspend fun updateUser(user: User): Result<Unit>
}

class UserRepositoryImpl(
    private val api: UserApi,
    private val cache: UserCache
) : UserRepository {

    override suspend fun getUser(id: String): User {
        // Try cache first
        cache.getUser(id)?.let { return it }

        // Fetch from API
        val user = api.getUser(id)
        cache.saveUser(user)
        return user
    }
}
```

## Offline-First Patterns

### Cache Strategy

```
Request → Check Cache → Valid? → Return cached
              ↓ No
        Fetch from API → Update cache → Return fresh
```

### Sync Queue

```swift
class SyncManager {
    private var pendingOperations: [Operation] = []

    func enqueue(_ operation: Operation) {
        pendingOperations.append(operation)
        persistQueue()
        attemptSync()
    }

    func attemptSync() {
        guard isOnline else { return }

        for operation in pendingOperations {
            do {
                try await execute(operation)
                remove(operation)
            } catch {
                break // Stop on first failure
            }
        }
    }
}
```

## Platform-Specific Considerations

### iOS

| Concern | Solution |
|---------|----------|
| Memory | Use weak references, ARC |
| Threading | Main for UI, background for work |
| Persistence | CoreData, SwiftData, UserDefaults |
| Keychain | Secure credential storage |

### Android

| Concern | Solution |
|---------|----------|
| Lifecycle | ViewModel, SavedStateHandle |
| Background | WorkManager for deferred work |
| Persistence | Room database |
| Config changes | Proper state restoration |

### Cross-Platform

| Framework | Strengths |
|-----------|-----------|
| React Native | JS ecosystem, hot reload |
| Flutter | Performance, custom UI |
| Kotlin Multiplatform | Shared business logic |

## Testing Patterns

### Unit Testing ViewModels

```kotlin
@Test
fun `fetchUser updates state correctly`() = runTest {
    // Given
    val fakeRepository = FakeUserRepository(User("1", "John"))
    val viewModel = UserViewModel(fakeRepository)

    // When
    viewModel.fetchUser("1")

    // Then
    assertEquals(User("1", "John"), viewModel.user.value)
    assertEquals(false, viewModel.isLoading.value)
}
```

### UI Testing

```swift
func testLoginFlow() {
    let app = XCUIApplication()
    app.launch()

    app.textFields["email"].tap()
    app.textFields["email"].typeText("test@example.com")

    app.secureTextFields["password"].tap()
    app.secureTextFields["password"].typeText("password123")

    app.buttons["Login"].tap()

    XCTAssert(app.staticTexts["Welcome"].waitForExistence(timeout: 5))
}
```
