#!/usr/bin/env python3
"""
Audio to Base64 Converter
Converts audio files to base64 format for API testing
"""

import base64
import sys
import os
from pathlib import Path

def audio_to_base64(file_path):
    """
    Convert audio file to base64 string
    
    Args:
        file_path: Path to audio file
        
    Returns:
        base64 encoded string
    """
    try:
        with open(file_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        
        base64_string = base64.b64encode(audio_bytes).decode('utf-8')
        return base64_string
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def get_file_info(file_path):
    """Get basic file information"""
    file_size = os.path.getsize(file_path)
    file_ext = Path(file_path).suffix.lower().replace('.', '')
    
    return {
        'size_bytes': file_size,
        'size_kb': round(file_size / 1024, 2),
        'size_mb': round(file_size / (1024 * 1024), 2),
        'format': file_ext
    }

def save_to_file(base64_string, output_path):
    """Save base64 string to file"""
    with open(output_path, 'w') as f:
        f.write(base64_string)

def main():
    if len(sys.argv) < 2:
        print("Usage: python audio_to_base64.py <audio_file> [output_file]")
        print("\nExample:")
        print("  python audio_to_base64.py sample.mp3")
        print("  python audio_to_base64.py sample.mp3 output.txt")
        print("\nSupported formats: mp3, wav, flac, ogg, m4a")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("=" * 70)
    print("Audio to Base64 Converter")
    print("=" * 70)
    
    # Get file info
    print(f"\nInput File: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)
    
    file_info = get_file_info(input_file)
    print(f"Format: {file_info['format'].upper()}")
    print(f"Size: {file_info['size_kb']} KB ({file_info['size_mb']} MB)")
    
    # Check size
    if file_info['size_mb'] > 10:
        print("\n⚠ Warning: File is larger than 10MB. API may reject it.")
    
    # Convert to base64
    print("\nConverting to Base64...")
    base64_string = audio_to_base64(input_file)
    
    if base64_string is None:
        sys.exit(1)
    
    print(f"✓ Conversion successful!")
    print(f"Base64 length: {len(base64_string)} characters")
    
    # Save to file if output specified
    if output_file:
        save_to_file(base64_string, output_file)
        print(f"✓ Saved to: {output_file}")
    else:
        # Auto-generate output filename
        output_file = f"{Path(input_file).stem}_base64.txt"
        save_to_file(base64_string, output_file)
        print(f"✓ Saved to: {output_file}")
    
    # Show preview
    print("\n" + "-" * 70)
    print("Base64 Preview (first 200 characters):")
    print("-" * 70)
    print(base64_string[:200] + "...")
    print("-" * 70)
    
    # Show JSON payload example
    print("\n" + "=" * 70)
    print("Example API Request Payload:")
    print("=" * 70)
    print(f"""
{{
  "language": "en",
  "audio_format": "{file_info['format']}",
  "audio_base64": "{base64_string[:50]}..."
}}
""")
    
    print("\n" + "=" * 70)
    print("Ready to use!")
    print("=" * 70)
    print(f"Copy the contents of '{output_file}' to use in your API request.")

if __name__ == '__main__':
    main()
