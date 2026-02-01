#!/usr/bin/env python3
"""
Batch Audio Testing Script
Test multiple audio files at once and generate a report
"""

import requests
import base64
import json
import os
import time
from pathlib import Path
import csv

class BatchTester:
    def __init__(self, endpoint_url, api_key):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.results = []
    
    def test_audio_file(self, file_path):
        """Test a single audio file"""
        try:
            # Read and encode
            with open(file_path, 'rb') as f:
                audio_bytes = f.read()
            
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            audio_format = Path(file_path).suffix.lower().replace('.', '')
            
            # Make request
            start_time = time.time()
            response = requests.post(
                self.endpoint_url,
                headers={
                    'x-api-key': self.api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'language': 'en',
                    'audio_format': audio_format,
                    'audio_base64': audio_base64
                },
                timeout=30
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {})
                
                return {
                    'file': Path(file_path).name,
                    'status': 'success',
                    'prediction': result.get('prediction', 'N/A'),
                    'is_ai': result.get('is_ai_generated', None),
                    'confidence': result.get('confidence', 0),
                    'duration': result.get('audio_duration_seconds', 0),
                    'processing_time': round(elapsed, 3),
                    'file_size_kb': round(len(audio_bytes) / 1024, 2)
                }
            else:
                return {
                    'file': Path(file_path).name,
                    'status': 'error',
                    'error': response.json().get('message', 'Unknown error'),
                    'processing_time': round(elapsed, 3)
                }
                
        except Exception as e:
            return {
                'file': Path(file_path).name,
                'status': 'error',
                'error': str(e)
            }
    
    def test_directory(self, directory_path, extensions=None):
        """Test all audio files in a directory"""
        if extensions is None:
            extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
        
        directory = Path(directory_path)
        audio_files = []
        
        for ext in extensions:
            audio_files.extend(directory.glob(f"*{ext}"))
        
        print(f"Found {len(audio_files)} audio files")
        
        for i, file_path in enumerate(audio_files, 1):
            print(f"\nTesting {i}/{len(audio_files)}: {file_path.name}")
            result = self.test_audio_file(file_path)
            self.results.append(result)
            
            if result['status'] == 'success':
                print(f"  ✓ {result['prediction']} (confidence: {result['confidence']*100:.1f}%)")
            else:
                print(f"  ✗ Error: {result.get('error', 'Unknown')}")
    
    def test_file_list(self, file_paths):
        """Test a list of audio files"""
        print(f"Testing {len(file_paths)} files")
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"\nTesting {i}/{len(file_paths)}: {Path(file_path).name}")
            result = self.test_audio_file(file_path)
            self.results.append(result)
            
            if result['status'] == 'success':
                print(f"  ✓ {result['prediction']} (confidence: {result['confidence']*100:.1f}%)")
            else:
                print(f"  ✗ Error: {result.get('error', 'Unknown')}")
    
    def generate_report(self, output_file='test_report.txt'):
        """Generate a detailed report"""
        with open(output_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("BATCH AUDIO TESTING REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Endpoint: {self.endpoint_url}\n")
            f.write(f"Total Files Tested: {len(self.results)}\n\n")
            
            # Summary statistics
            successful = [r for r in self.results if r['status'] == 'success']
            errors = [r for r in self.results if r['status'] == 'error']
            
            f.write(f"Successful: {len(successful)}\n")
            f.write(f"Errors: {len(errors)}\n")
            
            if successful:
                ai_count = sum(1 for r in successful if r.get('is_ai'))
                human_count = len(successful) - ai_count
                avg_confidence = sum(r.get('confidence', 0) for r in successful) / len(successful)
                avg_time = sum(r.get('processing_time', 0) for r in successful) / len(successful)
                
                f.write(f"\nDetection Summary:\n")
                f.write(f"  AI-Generated: {ai_count}\n")
                f.write(f"  Human: {human_count}\n")
                f.write(f"  Average Confidence: {avg_confidence*100:.2f}%\n")
                f.write(f"  Average Processing Time: {avg_time:.3f}s\n")
            
            f.write("\n" + "-"*80 + "\n")
            f.write("DETAILED RESULTS\n")
            f.write("-"*80 + "\n\n")
            
            for result in self.results:
                f.write(f"File: {result['file']}\n")
                if result['status'] == 'success':
                    f.write(f"  Status: ✓ Success\n")
                    f.write(f"  Prediction: {result['prediction']}\n")
                    f.write(f"  Confidence: {result['confidence']*100:.2f}%\n")
                    f.write(f"  Audio Duration: {result['duration']:.2f}s\n")
                    f.write(f"  Processing Time: {result['processing_time']}s\n")
                    f.write(f"  File Size: {result['file_size_kb']} KB\n")
                else:
                    f.write(f"  Status: ✗ Error\n")
                    f.write(f"  Error: {result.get('error', 'Unknown')}\n")
                f.write("\n")
        
        print(f"\n✓ Report saved to: {output_file}")
    
    def generate_csv(self, output_file='test_results.csv'):
        """Generate CSV report"""
        with open(output_file, 'w', newline='') as f:
            fieldnames = ['file', 'status', 'prediction', 'is_ai', 'confidence', 
                         'duration', 'processing_time', 'file_size_kb', 'error']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'file': result.get('file', ''),
                    'status': result.get('status', ''),
                    'prediction': result.get('prediction', ''),
                    'is_ai': result.get('is_ai', ''),
                    'confidence': result.get('confidence', ''),
                    'duration': result.get('duration', ''),
                    'processing_time': result.get('processing_time', ''),
                    'file_size_kb': result.get('file_size_kb', ''),
                    'error': result.get('error', '')
                })
        
        print(f"✓ CSV report saved to: {output_file}")
    
    def print_summary(self):
        """Print summary to console"""
        print("\n" + "="*80)
        print("BATCH TESTING SUMMARY")
        print("="*80)
        
        successful = [r for r in self.results if r['status'] == 'success']
        errors = [r for r in self.results if r['status'] == 'error']
        
        print(f"\nTotal Files: {len(self.results)}")
        print(f"✓ Successful: {len(successful)}")
        print(f"✗ Errors: {len(errors)}")
        
        if successful:
            ai_count = sum(1 for r in successful if r.get('is_ai'))
            human_count = len(successful) - ai_count
            
            print(f"\nDetections:")
            print(f"  🤖 AI-Generated: {ai_count}")
            print(f"  👤 Human: {human_count}")
            
            # Show highest and lowest confidence
            sorted_results = sorted(successful, key=lambda x: x.get('confidence', 0))
            if sorted_results:
                print(f"\nLowest Confidence: {sorted_results[0]['file']} - {sorted_results[0]['confidence']*100:.1f}%")
                print(f"Highest Confidence: {sorted_results[-1]['file']} - {sorted_results[-1]['confidence']*100:.1f}%")

def main():
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python batch_test.py <endpoint_url> <api_key> <directory_or_files...>")
        print("\nExamples:")
        print("  python batch_test.py http://localhost:5000/detect api-key ./audio_samples/")
        print("  python batch_test.py http://localhost:5000/detect api-key file1.mp3 file2.wav")
        sys.exit(1)
    
    endpoint_url = sys.argv[1]
    api_key = sys.argv[2]
    paths = sys.argv[3:]
    
    tester = BatchTester(endpoint_url, api_key)
    
    # Determine if testing directory or individual files
    if len(paths) == 1 and os.path.isdir(paths[0]):
        print(f"Testing directory: {paths[0]}")
        tester.test_directory(paths[0])
    else:
        print(f"Testing {len(paths)} file(s)")
        tester.test_file_list(paths)
    
    # Generate reports
    tester.print_summary()
    tester.generate_report()
    tester.generate_csv()

if __name__ == '__main__':
    main()
