# ARKit Location Anchoring

## Location Anchors (iOS 14+)

### Setup

```swift
import ARKit
import CoreLocation

class LocationARViewController: UIViewController, ARSessionDelegate {
    var arView: ARView!
    var locationManager: CLLocationManager!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Setup AR
        arView = ARView(frame: view.bounds)
        view.addSubview(arView)
        arView.session.delegate = self

        // Setup location
        locationManager = CLLocationManager()
        locationManager.requestWhenInUseAuthorization()

        // Configure AR session with geo tracking
        let config = ARGeoTrackingConfiguration()
        arView.session.run(config)
    }
}
```

### Check Availability

```swift
func checkGeoTrackingAvailability() {
    ARGeoTrackingConfiguration.checkAvailability { available, error in
        if let error = error {
            print("Geo tracking error: \(error)")
            return
        }

        if available {
            print("Geo tracking available")
        } else {
            print("Geo tracking not available")
        }
    }
}

// Check at specific location
func checkAvailabilityAtLocation(coordinate: CLLocationCoordinate2D) {
    ARGeoTrackingConfiguration.checkAvailability(at: coordinate) { available, error in
        // Handle result
    }
}
```

### Creating Geo Anchors

```swift
func createGeoAnchor(
    latitude: CLLocationDegrees,
    longitude: CLLocationDegrees,
    altitude: CLLocationDistance? = nil
) -> ARGeoAnchor {

    let coordinate = CLLocationCoordinate2D(
        latitude: latitude,
        longitude: longitude
    )

    if let altitude = altitude {
        return ARGeoAnchor(coordinate: coordinate, altitude: altitude)
    } else {
        // Use altitude from device's current location
        return ARGeoAnchor(coordinate: coordinate)
    }
}

// Add to session
func placeGeoAnchor(at coordinate: CLLocationCoordinate2D) {
    let anchor = ARGeoAnchor(coordinate: coordinate)
    arView.session.add(anchor: anchor)

    // Create visual content
    let entity = ModelEntity(mesh: .generateSphere(radius: 0.5))
    entity.position = [0, 0.5, 0]

    let anchorEntity = AnchorEntity(anchor: anchor)
    anchorEntity.addChild(entity)
    arView.scene.addAnchor(anchorEntity)
}
```

### Geo Tracking State

```swift
func session(_ session: ARSession, didChange geoTrackingStatus: ARGeoTrackingStatus) {
    switch geoTrackingStatus.state {
    case .notAvailable:
        showMessage("Geo tracking not available")

    case .initializing:
        showMessage("Initializing...")

    case .localizing:
        showMessage("Localizing...")

    case .localized:
        showMessage("Localized!")

    @unknown default:
        break
    }

    // Check accuracy
    switch geoTrackingStatus.accuracy {
    case .undetermined:
        break
    case .low:
        showMessage("Low accuracy - move to open area")
    case .medium:
        showMessage("Medium accuracy")
    case .high:
        showMessage("High accuracy")
    @unknown default:
        break
    }

    // Check state reason
    if let reason = geoTrackingStatus.stateReason {
        switch reason {
        case .notAvailableAtLocation:
            showMessage("Geo tracking not available here")
        case .needLocationPermissions:
            showMessage("Location permission required")
        case .devicePointedTooLow:
            showMessage("Point device forward")
        case .worldTrackingUnstable:
            showMessage("Move more slowly")
        @unknown default:
            break
        }
    }
}
```

### Altitude Options

```swift
// Automatic altitude (terrain-relative)
let anchor = ARGeoAnchor(coordinate: coordinate)

// Specific altitude (meters above sea level)
let anchor = ARGeoAnchor(
    coordinate: coordinate,
    altitude: 100.0
)

// Altitude relative to ground level
// (Requires ARKit to have terrain data)
let anchor = ARGeoAnchor(
    coordinate: coordinate,
    altitudeSource: .coarse  // or .precise, .user
)
```

## World Tracking with GPS

For devices without geo tracking support:

```swift
class GPSARViewController: UIViewController, CLLocationManagerDelegate {
    var arView: ARView!
    var locationManager: CLLocationManager!
    var originLocation: CLLocation?

    func startSession() {
        // Standard AR configuration
        let config = ARWorldTrackingConfiguration()
        config.worldAlignment = .gravityAndHeading
        arView.session.run(config)

        // Start location updates
        locationManager.startUpdatingLocation()
        locationManager.startUpdatingHeading()
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }

        if originLocation == nil {
            // First location becomes AR origin
            originLocation = location
        }

        // Convert geo to AR coordinates
        let arPosition = geoToLocal(
            geo: location.coordinate,
            origin: originLocation!.coordinate
        )

        // Update AR content positions
        updateContentPositions(userARPosition: arPosition)
    }

    func geoToLocal(
        geo: CLLocationCoordinate2D,
        origin: CLLocationCoordinate2D
    ) -> SIMD3<Float> {
        // Meters per degree (approximate)
        let latMeters = 111320.0
        let lonMeters = 111320.0 * cos(origin.latitude * .pi / 180)

        let x = Float((geo.longitude - origin.longitude) * lonMeters)
        let z = Float((geo.latitude - origin.latitude) * latMeters)

        return SIMD3<Float>(x, 0, -z)  // Z is negative forward in ARKit
    }
}
```

## RealityKit Integration

```swift
import RealityKit

func placeModelAtLocation(coordinate: CLLocationCoordinate2D, modelName: String) {
    // Create geo anchor
    let geoAnchor = ARGeoAnchor(coordinate: coordinate)
    arView.session.add(anchor: geoAnchor)

    // Load model
    guard let entity = try? Entity.load(named: modelName) else { return }

    // Create anchor entity linked to geo anchor
    let anchorEntity = AnchorEntity(anchor: geoAnchor)
    anchorEntity.addChild(entity)

    // Add to scene
    arView.scene.addAnchor(anchorEntity)
}

// With custom transform
func placeWithTransform(
    coordinate: CLLocationCoordinate2D,
    scale: Float,
    rotation: Float
) {
    let geoAnchor = ARGeoAnchor(coordinate: coordinate)
    arView.session.add(anchor: geoAnchor)

    let entity = ModelEntity(mesh: .generateBox(size: 1.0))

    // Apply transforms
    entity.scale = SIMD3<Float>(repeating: scale)
    entity.orientation = simd_quatf(angle: rotation, axis: [0, 1, 0])

    let anchorEntity = AnchorEntity(anchor: geoAnchor)
    anchorEntity.addChild(entity)
    arView.scene.addAnchor(anchorEntity)
}
```

## Persistence

```swift
// Save anchors
func saveAnchors() {
    var savedAnchors: [[String: Any]] = []

    for anchor in arView.session.currentFrame?.anchors ?? [] {
        if let geoAnchor = anchor as? ARGeoAnchor {
            savedAnchors.append([
                "latitude": geoAnchor.coordinate.latitude,
                "longitude": geoAnchor.coordinate.longitude,
                "altitude": geoAnchor.altitude ?? 0
            ])
        }
    }

    UserDefaults.standard.set(savedAnchors, forKey: "savedGeoAnchors")
}

// Restore anchors
func restoreAnchors() {
    guard let saved = UserDefaults.standard.array(forKey: "savedGeoAnchors") as? [[String: Any]] else { return }

    for data in saved {
        let coordinate = CLLocationCoordinate2D(
            latitude: data["latitude"] as! Double,
            longitude: data["longitude"] as! Double
        )
        let altitude = data["altitude"] as! Double

        let anchor = ARGeoAnchor(coordinate: coordinate, altitude: altitude)
        arView.session.add(anchor: anchor)
    }
}
```
