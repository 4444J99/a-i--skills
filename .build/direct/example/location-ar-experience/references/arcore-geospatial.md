# ARCore Geospatial API Guide

## Overview

The ARCore Geospatial API enables AR experiences anchored to real-world locations using Google's Visual Positioning System (VPS).

## Setup

### Dependencies (Android)

```gradle
dependencies {
    implementation 'com.google.ar:core:1.40.0'
}
```

### Permissions

```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.INTERNET" />
```

### Session Configuration

```kotlin
val config = Config(session)
config.geospatialMode = Config.GeospatialMode.ENABLED
session.configure(config)
```

## Geospatial Pose

### Getting Current Pose

```kotlin
val earth = session.earth
if (earth?.trackingState == TrackingState.TRACKING) {
    val pose = earth.cameraGeospatialPose

    // Geographic position
    val latitude = pose.latitude
    val longitude = pose.longitude
    val altitude = pose.altitude

    // Heading (compass direction)
    val heading = pose.heading

    // Accuracy estimates
    val horizontalAccuracy = pose.horizontalAccuracy  // meters
    val verticalAccuracy = pose.verticalAccuracy      // meters
    val headingAccuracy = pose.headingAccuracy        // degrees
}
```

### Accuracy Thresholds

```kotlin
fun isAccurateEnough(pose: GeospatialPose): Boolean {
    return pose.horizontalAccuracy < 10 &&    // Within 10m
           pose.verticalAccuracy < 10 &&      // Within 10m
           pose.headingAccuracy < 25          // Within 25 degrees
}
```

## Creating Anchors

### Standard Geospatial Anchor

```kotlin
fun createGeospatialAnchor(
    earth: Earth,
    latitude: Double,
    longitude: Double,
    altitude: Double,
    heading: Float
): Anchor? {
    // Check tracking state
    if (earth.trackingState != TrackingState.TRACKING) {
        return null
    }

    // Create rotation quaternion from heading
    val quaternion = Quaternion.axisAngle(
        Vector3(0f, 1f, 0f),
        Math.toRadians(heading.toDouble()).toFloat()
    )

    return earth.createAnchor(
        latitude, longitude, altitude,
        quaternion.x, quaternion.y, quaternion.z, quaternion.w
    )
}
```

### Terrain Anchor

Automatically finds correct altitude:

```kotlin
fun createTerrainAnchor(
    earth: Earth,
    latitude: Double,
    longitude: Double,
    heading: Float,
    callback: (Anchor?) -> Unit
) {
    val quaternion = Quaternion.axisAngle(
        Vector3(0f, 1f, 0f),
        Math.toRadians(heading.toDouble()).toFloat()
    )

    earth.resolveAnchorOnTerrainAsync(
        latitude, longitude,
        0.0,  // Altitude above terrain
        quaternion.x, quaternion.y, quaternion.z, quaternion.w
    ) { anchor, state ->
        when (state) {
            Anchor.TerrainAnchorState.SUCCESS -> callback(anchor)
            Anchor.TerrainAnchorState.ERROR_NOT_AUTHORIZED -> {
                Log.e("AR", "Geospatial API not authorized")
                callback(null)
            }
            Anchor.TerrainAnchorState.ERROR_INTERNAL -> {
                Log.e("AR", "Internal error creating terrain anchor")
                callback(null)
            }
            else -> callback(null)
        }
    }
}
```

### Rooftop Anchor

For placing content on building rooftops:

```kotlin
earth.resolveAnchorOnRooftopAsync(
    latitude, longitude,
    0.0,  // Altitude above rooftop
    quaternion.x, quaternion.y, quaternion.z, quaternion.w
) { anchor, state ->
    // Handle result
}
```

## Streetscape Geometry

Access building and terrain geometry:

```kotlin
val config = Config(session)
config.streetscapeGeometryMode = Config.StreetscapeGeometryMode.ENABLED
session.configure(config)

// In frame update
for (geometry in frame.getUpdatedTrackables(StreetscapeGeometry::class.java)) {
    when (geometry.type) {
        StreetscapeGeometry.Type.BUILDING -> {
            // Building mesh
            val mesh = geometry.meshes[0]
        }
        StreetscapeGeometry.Type.TERRAIN -> {
            // Terrain mesh
        }
    }
}
```

## VPS Availability

Check if VPS is available at location:

```kotlin
fun checkVpsAvailability(latitude: Double, longitude: Double) {
    session.checkVpsAvailabilityAsync(latitude, longitude) { availability ->
        when (availability) {
            VpsAvailability.AVAILABLE -> {
                // VPS supported at this location
            }
            VpsAvailability.UNAVAILABLE -> {
                // VPS not supported, use GPS-only
            }
            VpsAvailability.ERROR_NETWORK_CONNECTION -> {
                // Network error
            }
            else -> {
                // Unknown
            }
        }
    }
}
```

## Best Practices

### Battery and Performance

```kotlin
class GeospatialSessionManager {
    private var isGeospatialActive = false

    fun enableGeospatial() {
        val config = session.config
        config.geospatialMode = Config.GeospatialMode.ENABLED
        session.configure(config)
        isGeospatialActive = true
    }

    fun disableGeospatial() {
        // Disable when not needed to save battery
        val config = session.config
        config.geospatialMode = Config.GeospatialMode.DISABLED
        session.configure(config)
        isGeospatialActive = false
    }

    fun onAppBackground() {
        // Always disable when app is backgrounded
        disableGeospatial()
    }
}
```

### Anchor Persistence

```kotlin
// Save anchor
fun saveAnchor(anchor: Anchor): String {
    return """
        {
            "latitude": ${anchor.geospatialPose.latitude},
            "longitude": ${anchor.geospatialPose.longitude},
            "altitude": ${anchor.geospatialPose.altitude},
            "heading": ${anchor.geospatialPose.heading}
        }
    """.trimIndent()
}

// Restore anchor
fun restoreAnchor(json: String, earth: Earth): Anchor? {
    val data = JSONObject(json)
    return createGeospatialAnchor(
        earth,
        data.getDouble("latitude"),
        data.getDouble("longitude"),
        data.getDouble("altitude"),
        data.getDouble("heading").toFloat()
    )
}
```

### Error Handling

```kotlin
sealed class GeospatialError {
    object NotSupported : GeospatialError()
    object NotAuthorized : GeospatialError()
    object NotTracking : GeospatialError()
    object InsufficientAccuracy : GeospatialError()
    data class AnchorFailed(val reason: String) : GeospatialError()
}

fun handleGeospatialError(error: GeospatialError) {
    when (error) {
        GeospatialError.NotSupported -> showMessage("AR not supported on this device")
        GeospatialError.NotAuthorized -> showMessage("Please enable location services")
        GeospatialError.NotTracking -> showMessage("Move your phone to improve tracking")
        GeospatialError.InsufficientAccuracy -> showMessage("Move to an open area")
        is GeospatialError.AnchorFailed -> showMessage("Could not place AR content: ${error.reason}")
    }
}
```

## Debugging

### Geospatial Debug Info

```kotlin
fun getDebugInfo(earth: Earth): String {
    val pose = earth.cameraGeospatialPose
    return """
        State: ${earth.trackingState}
        Lat: ${pose.latitude}
        Lng: ${pose.longitude}
        Alt: ${pose.altitude}
        Heading: ${pose.heading}
        H Accuracy: ${pose.horizontalAccuracy}m
        V Accuracy: ${pose.verticalAccuracy}m
        Heading Accuracy: ${pose.headingAccuracy}°
    """.trimIndent()
}
```
