# Motion Capture Data Formats

## BVH (Biovision Hierarchy)

### Structure

```
HIERARCHY
ROOT Hips
{
    OFFSET 0.00 0.00 0.00
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Spine
    {
        OFFSET 0.00 10.00 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
        JOINT Spine1
        {
            ...
        }
    }
    JOINT LeftUpLeg
    {
        OFFSET -8.00 0.00 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
        JOINT LeftLeg
        {
            OFFSET 0.00 -45.00 0.00
            CHANNELS 3 Zrotation Xrotation Yrotation
            End Site
            {
                OFFSET 0.00 -40.00 0.00
            }
        }
    }
}
MOTION
Frames: 100
Frame Time: 0.0333333
0.00 0.00 0.00 0.00 0.00 0.00 10.5 -3.2 0.1 ...
```

### Parsing BVH

```python
def parse_bvh(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Parse hierarchy
    joints = {}
    stack = []
    current_joint = None
    in_motion = False
    frames = []
    frame_time = 0

    for line in lines:
        line = line.strip()

        if line.startswith('HIERARCHY'):
            continue
        elif line.startswith('MOTION'):
            in_motion = True
            continue

        if in_motion:
            if line.startswith('Frames:'):
                num_frames = int(line.split(':')[1])
            elif line.startswith('Frame Time:'):
                frame_time = float(line.split(':')[1])
            else:
                # Motion data
                values = [float(x) for x in line.split()]
                frames.append(values)
        else:
            # Parse hierarchy
            if 'ROOT' in line or 'JOINT' in line:
                name = line.split()[-1]
                joint = {'name': name, 'children': [], 'channels': []}
                if current_joint:
                    current_joint['children'].append(joint)
                    stack.append(current_joint)
                current_joint = joint
                joints[name] = joint
            elif 'OFFSET' in line:
                parts = line.split()
                current_joint['offset'] = [float(parts[1]), float(parts[2]), float(parts[3])]
            elif 'CHANNELS' in line:
                parts = line.split()
                current_joint['channels'] = parts[2:]
            elif line == '}':
                if stack:
                    current_joint = stack.pop()

    return {'joints': joints, 'frames': frames, 'frame_time': frame_time}
```

## FBX

Binary format from Autodesk. Use libraries for parsing:

```python
# Using FBX SDK Python bindings
import fbx

def read_fbx(filename):
    manager = fbx.FbxManager.Create()
    ios = fbx.FbxIOSettings.Create(manager, fbx.IOSROOT)
    manager.SetIOSettings(ios)

    importer = fbx.FbxImporter.Create(manager, "")
    importer.Initialize(filename, -1, manager.GetIOSettings())

    scene = fbx.FbxScene.Create(manager, "scene")
    importer.Import(scene)
    importer.Destroy()

    # Access animation
    anim_stack = scene.GetCurrentAnimationStack()
    # ... process animation data

    return scene
```

## C3D

Common format for biomechanics data.

```python
import c3d

def read_c3d(filename):
    reader = c3d.Reader(open(filename, 'rb'))

    # Get marker labels
    labels = reader.point_labels

    # Get frames
    frames = []
    for i, points, analog in reader.read_frames():
        frame = {
            'frame': i,
            'markers': {}
        }
        for j, label in enumerate(labels):
            frame['markers'][label] = {
                'x': points[j, 0],
                'y': points[j, 1],
                'z': points[j, 2]
            }
        frames.append(frame)

    return {
        'labels': labels,
        'frames': frames,
        'frame_rate': reader.header.frame_rate
    }
```

## JSON Pose Format

Common for web-based applications:

```json
{
    "fps": 30,
    "frames": [
        {
            "time": 0.0,
            "joints": {
                "hips": {
                    "position": [0, 1, 0],
                    "rotation": [0, 0, 0, 1]
                },
                "spine": {
                    "position": [0, 0.2, 0],
                    "rotation": [0.1, 0, 0, 0.995]
                }
            }
        }
    ],
    "skeleton": {
        "hips": {
            "parent": null,
            "offset": [0, 1, 0]
        },
        "spine": {
            "parent": "hips",
            "offset": [0, 0.2, 0]
        }
    }
}
```

## MediaPipe Landmarks

```python
# 33 body landmarks from MediaPipe
LANDMARK_NAMES = [
    'nose', 'left_eye_inner', 'left_eye', 'left_eye_outer',
    'right_eye_inner', 'right_eye', 'right_eye_outer',
    'left_ear', 'right_ear', 'mouth_left', 'mouth_right',
    'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
    'left_wrist', 'right_wrist', 'left_pinky', 'right_pinky',
    'left_index', 'right_index', 'left_thumb', 'right_thumb',
    'left_hip', 'right_hip', 'left_knee', 'right_knee',
    'left_ankle', 'right_ankle', 'left_heel', 'right_heel',
    'left_foot_index', 'right_foot_index'
]

def mediapipe_to_skeleton(landmarks):
    """Convert MediaPipe landmarks to skeleton format"""
    skeleton = {}
    for i, name in enumerate(LANDMARK_NAMES):
        lm = landmarks.landmark[i]
        skeleton[name] = {
            'x': lm.x,
            'y': lm.y,
            'z': lm.z,
            'visibility': lm.visibility
        }
    return skeleton
```

## Format Conversion

```python
def bvh_to_json(bvh_data, output_file):
    """Convert BVH to JSON format"""
    result = {
        'fps': 1.0 / bvh_data['frame_time'],
        'frames': [],
        'skeleton': {}
    }

    # Build skeleton
    for name, joint in bvh_data['joints'].items():
        result['skeleton'][name] = {
            'offset': joint.get('offset', [0, 0, 0]),
            'channels': joint.get('channels', [])
        }

    # Convert frames
    for frame_data in bvh_data['frames']:
        frame = {'joints': {}}
        idx = 0
        for name, joint in bvh_data['joints'].items():
            channels = joint.get('channels', [])
            values = {}
            for ch in channels:
                values[ch] = frame_data[idx]
                idx += 1
            frame['joints'][name] = values
        result['frames'].append(frame)

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
```
