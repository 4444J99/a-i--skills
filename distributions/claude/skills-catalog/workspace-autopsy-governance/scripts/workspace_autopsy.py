import os
import json
import argparse
from pathlib import Path

def ignore_path(path_str):
    ignores = ['.git', 'node_modules', 'venv', '__pycache__', '.pytest_cache', 'dist', 'build', '.gemini']
    for ig in ignores:
        if f"/{ig}/" in path_str or path_str.endswith(f"/{ig}") or path_str.startswith(f"{ig}/") or path_str == ig:
            return True
    return False

def generate_map(root_dir):
    tree = {}
    total_files = 0
    total_dirs = 0
    extensions = {}
    
    for root, dirs, files in os.walk(root_dir):
        rel_root = os.path.relpath(root, root_dir)
        if ignore_path(rel_root) and rel_root != '.':
            # Remove dirs to skip traversing
            dirs[:] = []
            continue
            
        # Filter out ignored dirs for the current level
        dirs[:] = [d for d in dirs if not ignore_path(os.path.join(rel_root, d) if rel_root != '.' else d)]
        
        node = {'files': [], 'dirs': dirs}
        for f in files:
            if ignore_path(f):
                continue
            total_files += 1
            ext = os.path.splitext(f)[1] or 'no_extension'
            extensions[ext] = extensions.get(ext, 0) + 1
            node['files'].append(f)
            
        if rel_root != '.':
            total_dirs += 1
            
        tree[rel_root] = node
        
    return {
        'stats': {
            'total_directories': total_dirs,
            'total_files': total_files,
            'file_types': extensions
        },
        'tree': tree
    }

def print_tree(tree_data, current_node='.', prefix=''):
    if current_node not in tree_data:
        return
        
    node = tree_data[current_node]
    
    # Print directories
    for i, d in enumerate(node['dirs']):
        is_last = (i == len(node['dirs']) - 1) and len(node['files']) == 0
        marker = '└── ' if is_last else '├── '
        print(f"{prefix}{marker}{d}/")
        
        next_path = os.path.join(current_node, d) if current_node != '.' else d
        next_prefix = prefix + ('    ' if is_last else '│   ')
        print_tree(tree_data, next_path, next_prefix)
        
    # Print files
    for i, f in enumerate(node['files']):
        is_last = (i == len(node['files']) - 1)
        marker = '└── ' if is_last else '├── '
        print(f"{prefix}{marker}{f}")

def main():
    parser = argparse.ArgumentParser(description="Workspace Autopsy Tool")
    parser.add_argument('--dir', type=str, default='.', help='Directory to autopsy')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    args = parser.parse_args()
    
    target_dir = os.path.abspath(args.dir)
    data = generate_map(target_dir)
    
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"WORKSPACE AUTOPSY REPORT")
        print(f"========================")
        print(f"Target: {target_dir}")
        print(f"Total Directories: {data['stats']['total_directories']}")
        print(f"Total Files: {data['stats']['total_files']}")
        print(f"File Types: {data['stats']['file_types']}")
        print(f"\nDIRECTORY MAP:")
        print(f"==============\n.")
        print_tree(data['tree'])

if __name__ == '__main__':
    main()
