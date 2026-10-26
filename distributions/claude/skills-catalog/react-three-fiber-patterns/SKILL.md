---
name: react-three-fiber-patterns
description: Build interactive 3D experiences in React using react-three-fiber (R3F), drei helpers, and shader integration. Covers scene composition, performance optimization, and animation patterns. Triggers on R3F development, React + Three.js, or declarative 3D scene requests.
license: MIT
complexity: advanced
time_to_learn: 30min
tags:
  - react-three-fiber
  - threejs
  - 3d
  - webgl
  - react
governance_phases: [build]
organ_affinity: [organ-ii]
triggers: [user-asks-about-r3f, context:react-threejs, context:react-3d, project-has-react-three-fiber]
complements: [three-js-interactive-builder, generative-art-algorithms, frontend-design-systems]
---

# React Three Fiber Patterns

Build 3D scenes declaratively with React using react-three-fiber.

## Setup

```bash
npm install three @react-three/fiber @react-three/drei
npm install -D @types/three
```

## Basic Scene

```tsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'

export function Scene() {
  return (
    <Canvas camera={{ position: [0, 2, 5], fov: 60 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <mesh position={[0, 1, 0]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="hotpink" />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[10, 10]} />
        <meshStandardMaterial color="#333" />
      </mesh>
      <OrbitControls />
      <Environment preset="sunset" />
    </Canvas>
  )
}
```

## Component Patterns

### Reusable 3D Components

```tsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface SpinningBoxProps {
  position: [number, number, number]
  color: string
  speed?: number
}

export function SpinningBox({ position, color, speed = 1 }: SpinningBoxProps) {
  const meshRef = useRef<THREE.Mesh>(null!)

  useFrame((state, delta) => {
    meshRef.current.rotation.y += delta * speed
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.5 + 1
  })

  return (
    <mesh ref={meshRef} position={position}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}
```

### Instanced Meshes (Performance)

```tsx
import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export function ParticleField({ count = 1000 }) {
  const meshRef = useRef<THREE.InstancedMesh>(null!)
  const dummy = useMemo(() => new THREE.Object3D(), [])

  const particles = useMemo(() =>
    Array.from({ length: count }, () => ({
      position: [
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
      ] as [number, number, number],
      speed: 0.5 + Math.random() * 2,
    })),
    [count]
  )

  useFrame((state) => {
    particles.forEach((p, i) => {
      dummy.position.set(...p.position)
      dummy.position.y += Math.sin(state.clock.elapsedTime * p.speed) * 0.5
      dummy.updateMatrix()
      meshRef.current.setMatrixAt(i, dummy.matrix)
    })
    meshRef.current.instanceMatrix.needsUpdate = true
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[0.05, 8, 8]} />
      <meshStandardMaterial color="#88ccff" />
    </instancedMesh>
  )
}
```

## Animation

### Spring Physics (react-spring)

```tsx
import { useSpring, animated } from '@react-spring/three'

export function AnimatedBox({ active }: { active: boolean }) {
  const springs = useSpring({
    scale: active ? 1.5 : 1,
    color: active ? '#ff6b6b' : '#4ecdc4',
  })

  return (
    <animated.mesh scale={springs.scale}>
      <boxGeometry />
      <animated.meshStandardMaterial color={springs.color} />
    </animated.mesh>
  )
}
```

### GSAP Integration

```tsx
import { useRef, useEffect } from 'react'
import gsap from 'gsap'
import * as THREE from 'three'

export function GSAPMesh() {
  const meshRef = useRef<THREE.Mesh>(null!)

  useEffect(() => {
    gsap.to(meshRef.current.rotation, {
      y: Math.PI * 2,
      duration: 4,
      repeat: -1,
      ease: 'none',
    })
    gsap.to(meshRef.current.position, {
      y: 2,
      duration: 2,
      yoyo: true,
      repeat: -1,
      ease: 'power1.inOut',
    })
  }, [])

  return (
    <mesh ref={meshRef}>
      <torusKnotGeometry args={[1, 0.3, 128, 32]} />
      <meshStandardMaterial color="gold" metalness={0.8} roughness={0.2} />
    </mesh>
  )
}
```

## Drei Helpers

```tsx
import {
  Text, Html, Float, MeshDistortMaterial,
  useGLTF, useTexture, Sparkles,
} from '@react-three/drei'

// 3D Text
<Text fontSize={0.5} color="white" anchorX="center">
  Hello World
</Text>

// HTML overlay in 3D space
<Html position={[0, 2, 0]} center>
  <div className="tooltip">Score: 42</div>
</Html>

// Floating animation
<Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
  <mesh><sphereGeometry /><meshStandardMaterial /></mesh>
</Float>

// Distortion material
<mesh>
  <sphereGeometry args={[1, 64, 64]} />
  <MeshDistortMaterial color="#8b5cf6" speed={2} distort={0.3} />
</mesh>

// Particle sparkles
<Sparkles count={200} scale={5} size={2} speed={0.5} />
```

## Custom Shaders

```tsx
import { shaderMaterial } from '@react-three/drei'
import { extend, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

const WaveMaterial = shaderMaterial(
  { uTime: 0, uColor: new THREE.Color('#4ecdc4') },
  // Vertex shader
  `varying vec2 vUv;
   uniform float uTime;
   void main() {
     vUv = uv;
     vec3 pos = position;
     pos.z += sin(pos.x * 4.0 + uTime) * 0.2;
     gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
   }`,
  // Fragment shader
  `varying vec2 vUv;
   uniform vec3 uColor;
   void main() {
     gl_FragColor = vec4(uColor * vUv.y, 1.0);
   }`
)

extend({ WaveMaterial })

export function WavePlane() {
  const materialRef = useRef<any>(null!)
  useFrame((state) => {
    materialRef.current.uTime = state.clock.elapsedTime
  })
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[10, 10, 64, 64]} />
      <waveMaterial ref={materialRef} />
    </mesh>
  )
}
```

## Performance

| Technique | When | Savings |
|-----------|------|---------|
| `useFrame` with delta | Always | Framerate-independent |
| `InstancedMesh` | >100 same geometry | 90%+ draw calls |
| `useMemo` for geometry | Static data | Prevents re-creation |
| `<Suspense>` + `useGLTF` | Asset loading | Non-blocking |
| `<Leva>` debug controls | Development | Easy parameter tuning |
| `gl={{ antialias: false }}` | Mobile | GPU savings |

## Anti-Patterns

- **Creating objects in useFrame** — Pre-create with useMemo or useRef
- **No key prop on dynamic lists** — React needs keys to track 3D elements
- **Direct Three.js mutation in render** — Use refs and useFrame instead
- **Loading models synchronously** — Always use Suspense boundaries
- **No dispose** — Clean up geometries and materials when unmounting
- **Pixel-perfect expectations** — WebGL rendering varies by GPU; test across devices
