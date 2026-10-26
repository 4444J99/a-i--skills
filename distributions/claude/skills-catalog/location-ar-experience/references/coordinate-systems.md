# Geospatial Coordinate Systems

## Coordinate Systems Overview

### WGS84 (GPS Standard)

```
Latitude:  -90° to +90° (South to North)
Longitude: -180° to +180° (West to East)
Altitude:  meters above WGS84 ellipsoid
```

### ECEF (Earth-Centered, Earth-Fixed)

```
X: Through equator at prime meridian (0°, 0°)
Y: Through equator at 90° East
Z: Through North Pole

Origin: Earth's center of mass
```

### ENU (East-North-Up)

```
Local tangent plane coordinate system:
X: East
Y: North
Z: Up

Origin: Chosen reference point on Earth's surface
```

## Conversions

### WGS84 to ECEF

```python
import math

def wgs84_to_ecef(lat, lon, alt):
    """
    Convert WGS84 to ECEF coordinates

    lat, lon: degrees
    alt: meters above ellipsoid
    Returns: (x, y, z) in meters
    """
    # WGS84 ellipsoid parameters
    a = 6378137.0  # Semi-major axis (meters)
    f = 1 / 298.257223563  # Flattening
    e2 = f * (2 - f)  # Eccentricity squared

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    # Radius of curvature in prime vertical
    N = a / math.sqrt(1 - e2 * math.sin(lat_rad)**2)

    x = (N + alt) * math.cos(lat_rad) * math.cos(lon_rad)
    y = (N + alt) * math.cos(lat_rad) * math.sin(lon_rad)
    z = (N * (1 - e2) + alt) * math.sin(lat_rad)

    return (x, y, z)
```

### ECEF to WGS84

```python
def ecef_to_wgs84(x, y, z):
    """
    Convert ECEF to WGS84 coordinates

    x, y, z: meters
    Returns: (lat, lon, alt) - lat/lon in degrees, alt in meters
    """
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = f * (2 - f)

    lon = math.atan2(y, x)

    # Iterative calculation for latitude
    p = math.sqrt(x**2 + y**2)
    lat = math.atan2(z, p * (1 - e2))

    for _ in range(10):
        N = a / math.sqrt(1 - e2 * math.sin(lat)**2)
        lat = math.atan2(z + e2 * N * math.sin(lat), p)

    # Altitude
    N = a / math.sqrt(1 - e2 * math.sin(lat)**2)
    alt = p / math.cos(lat) - N

    return (math.degrees(lat), math.degrees(lon), alt)
```

### WGS84 to ENU

```python
def wgs84_to_enu(lat, lon, alt, origin_lat, origin_lon, origin_alt):
    """
    Convert WGS84 to local ENU coordinates

    Returns: (east, north, up) in meters relative to origin
    """
    # Convert both points to ECEF
    x, y, z = wgs84_to_ecef(lat, lon, alt)
    x0, y0, z0 = wgs84_to_ecef(origin_lat, origin_lon, origin_alt)

    # Vector from origin to point
    dx = x - x0
    dy = y - y0
    dz = z - z0

    # Rotation matrix
    lat0_rad = math.radians(origin_lat)
    lon0_rad = math.radians(origin_lon)

    # ENU = R * ECEF_diff
    east = -math.sin(lon0_rad) * dx + math.cos(lon0_rad) * dy
    north = (-math.sin(lat0_rad) * math.cos(lon0_rad) * dx
             - math.sin(lat0_rad) * math.sin(lon0_rad) * dy
             + math.cos(lat0_rad) * dz)
    up = (math.cos(lat0_rad) * math.cos(lon0_rad) * dx
          + math.cos(lat0_rad) * math.sin(lon0_rad) * dy
          + math.sin(lat0_rad) * dz)

    return (east, north, up)
```

### ENU to WGS84

```python
def enu_to_wgs84(east, north, up, origin_lat, origin_lon, origin_alt):
    """
    Convert local ENU to WGS84 coordinates
    """
    # Convert origin to ECEF
    x0, y0, z0 = wgs84_to_ecef(origin_lat, origin_lon, origin_alt)

    lat0_rad = math.radians(origin_lat)
    lon0_rad = math.radians(origin_lon)

    # Inverse rotation: ECEF_diff = R^T * ENU
    dx = (-math.sin(lon0_rad) * east
          - math.sin(lat0_rad) * math.cos(lon0_rad) * north
          + math.cos(lat0_rad) * math.cos(lon0_rad) * up)
    dy = (math.cos(lon0_rad) * east
          - math.sin(lat0_rad) * math.sin(lon0_rad) * north
          + math.cos(lat0_rad) * math.sin(lon0_rad) * up)
    dz = math.cos(lat0_rad) * north + math.sin(lat0_rad) * up

    # Add to origin
    x = x0 + dx
    y = y0 + dy
    z = z0 + dz

    return ecef_to_wgs84(x, y, z)
```

## Distance Calculations

### Haversine Formula

```python
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate great-circle distance between two points

    Returns: distance in meters
    """
    R = 6371000  # Earth radius in meters

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c
```

### Bearing Calculation

```python
def bearing(lat1, lon1, lat2, lon2):
    """
    Calculate initial bearing from point 1 to point 2

    Returns: bearing in degrees (0-360, clockwise from north)
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlon) * math.cos(lat2_rad)
    y = (math.cos(lat1_rad) * math.sin(lat2_rad) -
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))

    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360) % 360
```

### Destination Point

```python
def destination_point(lat, lon, bearing, distance):
    """
    Calculate destination point given start, bearing, and distance

    bearing: degrees
    distance: meters
    Returns: (lat, lon) in degrees
    """
    R = 6371000

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    bearing_rad = math.radians(bearing)
    d = distance / R

    lat2 = math.asin(
        math.sin(lat_rad) * math.cos(d) +
        math.cos(lat_rad) * math.sin(d) * math.cos(bearing_rad)
    )

    lon2 = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(d) * math.cos(lat_rad),
        math.cos(d) - math.sin(lat_rad) * math.sin(lat2)
    )

    return (math.degrees(lat2), math.degrees(lon2))
```

## AR Coordinate Mapping

### Simple Planar Projection (Small Areas)

```python
def simple_geo_to_ar(lat, lon, origin_lat, origin_lon):
    """
    Simple conversion for small areas (<10km)
    Assumes flat Earth (introduces error at large distances)
    """
    # Meters per degree at origin latitude
    lat_scale = 111320  # Approximately constant
    lon_scale = 111320 * math.cos(math.radians(origin_lat))

    x = (lon - origin_lon) * lon_scale  # East (AR positive X)
    z = (lat - origin_lat) * lat_scale  # North (AR negative Z typically)

    return (x, 0, -z)  # Y is up, Z is forward (negative)
```

### With Altitude

```python
def geo_to_ar_3d(lat, lon, alt, origin_lat, origin_lon, origin_alt):
    """
    Full 3D conversion using ENU
    """
    east, north, up = wgs84_to_enu(
        lat, lon, alt,
        origin_lat, origin_lon, origin_alt
    )

    # Map to AR coordinate system
    # Typically: X=East, Y=Up, Z=-North (forward)
    return (east, up, -north)
```

## Common Pitfalls

1. **Longitude wraparound**: -180° and 180° are the same location
2. **Altitude reference**: WGS84 ellipsoid ≠ sea level
3. **Large distances**: Planar approximations fail
4. **Heading vs bearing**: Heading from compass, bearing calculated
5. **Coordinate order**: Some APIs use (lat, lon), others (lon, lat)
