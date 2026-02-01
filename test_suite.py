#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI Voice Detection API
Tests all endpoints, error cases, and edge cases
"""

import requests
import base64
import json
import sys
import time
from pathlib import Path

class APITester:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.test_results = []
        
    def run_test(self, name, test_func):
        """Run a single test and record result"""
        print(f"\n{'='*70}")
        print(f"TEST: {name}")
        print(f"{'='*70}")
        
        try:
            start_time = time.time()
            result = test_func()
            elapsed = time.time() - start_time
            
            self.test_results.append({
                'name': name,
                'status': 'PASS' if result else 'FAIL',
                'time': round(elapsed, 3)
            })
            
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"\nResult: {status} ({elapsed:.3f}s)")
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.test_results.append({
                'name': name,
                'status': 'ERROR',
                'error': str(e),
                'time': round(elapsed, 3)
            })
            print(f"\nResult: ✗ ERROR - {e}")
            return False
    
    def test_health_check(self):
        """Test health check endpoint"""
        url = f"{self.base_url}/health"
        response = requests.get(url, timeout=10)
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200 and response.json().get('status') == 'healthy'
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        url = self.base_url
        response = requests.get(url, timeout=10)
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200 and response.json().get('status') == 'active'
    
    def test_missing_api_key(self):
        """Test request without API key (should fail)"""
        url = f"{self.base_url}/detect"
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json={'language': 'en', 'audio_format': 'mp3', 'audio_base64': 'test'},
            timeout=10
        )
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 401
    
    def test_invalid_api_key(self):
        """Test request with invalid API key (should fail)"""
        url = f"{self.base_url}/detect"
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': 'invalid-key-12345'
            },
            json={'language': 'en', 'audio_format': 'mp3', 'audio_base64': 'test'},
            timeout=10
        )
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 401
    
    def test_missing_audio_data(self):
        """Test request without audio data (should fail)"""
        url = f"{self.base_url}/detect"
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key
            },
            json={'language': 'en', 'audio_format': 'mp3'},
            timeout=10
        )
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 400
    
    def test_invalid_base64(self):
        """Test request with invalid base64 (should fail)"""
        url = f"{self.base_url}/detect"
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key
            },
            json={
                'language': 'en',
                'audio_format': 'mp3',
                'audio_base64': 'this-is-not-valid-base64!!!'
            },
            timeout=10
        )
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code in [400, 500]
    
    def test_valid_detection_with_file(self, audio_file_path):
        """Test valid detection request with actual audio file"""
        if not Path(audio_file_path).exists():
            print(f"⚠ Skipping: Audio file not found at {audio_file_path}")
            return True  # Skip this test
        
        # Read and encode audio
        with open(audio_file_path, 'rb') as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Get file format
        audio_format = Path(audio_file_path).suffix.lower().replace('.', '')
        
        url = f"{self.base_url}/detect"
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': self.api_key
            },
            json={
                'language': 'en',
                'audio_format': audio_format,
                'audio_base64': audio_base64
            },
            timeout=30
        )
        
        print(f"URL: {url}")
        print(f"Audio File: {audio_file_path}")
        print(f"File Size: {len(audio_bytes)} bytes")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Validate response structure
            assert 'success' in data
            assert 'result' in data
            assert 'is_ai_generated' in data['result']
            assert 'confidence' in data['result']
            assert 'prediction' in data['result']
            
            print(f"\n📊 Detection Results:")
            print(f"   Prediction: {data['result']['prediction']}")
            print(f"   Confidence: {data['result']['confidence'] * 100:.2f}%")
            print(f"   Is AI: {data['result']['is_ai_generated']}")
            
            return True
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return False
    
    def test_different_languages(self, audio_file_path):
        """Test with different language codes"""
        if not Path(audio_file_path).exists():
            print(f"⚠ Skipping: Audio file not found")
            return True
        
        with open(audio_file_path, 'rb') as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        languages = ['en', 'hi', 'es', 'fr', 'de']
        url = f"{self.base_url}/detect"
        
        for lang in languages:
            print(f"\nTesting language: {lang}")
            response = requests.post(
                url,
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': self.api_key
                },
                json={
                    'language': lang,
                    'audio_format': 'mp3',
                    'audio_base64': audio_base64
                },
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   ✗ Failed for {lang}")
                return False
            
            print(f"   ✓ Success for {lang}")
        
        return True
    
    def test_stats_endpoint(self):
        """Test stats endpoint"""
        url = f"{self.base_url}/stats"
        response = requests.get(
            url,
            headers={'x-api-key': self.api_key},
            timeout=10
        )
        
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        errors = sum(1 for r in self.test_results if r['status'] == 'ERROR')
        
        print(f"\nTotal Tests: {total}")
        print(f"✓ Passed: {passed}")
        print(f"✗ Failed: {failed}")
        print(f"⚠ Errors: {errors}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        print("\nDetailed Results:")
        print("-"*70)
        for result in self.test_results:
            status_icon = {
                'PASS': '✓',
                'FAIL': '✗',
                'ERROR': '⚠'
            }.get(result['status'], '?')
            
            print(f"{status_icon} {result['name']:50s} {result['time']:6.3f}s")
        
        print("="*70)
        
        return passed == total

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_suite.py <base_url> [api_key] [audio_file]")
        print("\nExample:")
        print("  python test_suite.py http://localhost:5000")
        print("  python test_suite.py https://your-api.com hackathon-api-key-2024")
        print("  python test_suite.py https://your-api.com your-key sample.mp3")
        sys.exit(1)
    
    base_url = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else 'hackathon-api-key-2024'
    audio_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    print("\n" + "="*70)
    print("AI VOICE DETECTION API - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"\nBase URL: {base_url}")
    print(f"API Key: {api_key[:10]}..." if len(api_key) > 10 else f"API Key: {api_key}")
    if audio_file:
        print(f"Audio File: {audio_file}")
    
    tester = APITester(base_url, api_key)
    
    # Run tests
    tester.run_test("Health Check", tester.test_health_check)
    tester.run_test("Root Endpoint", tester.test_root_endpoint)
    tester.run_test("Missing API Key (should fail)", tester.test_missing_api_key)
    tester.run_test("Invalid API Key (should fail)", tester.test_invalid_api_key)
    tester.run_test("Missing Audio Data (should fail)", tester.test_missing_audio_data)
    tester.run_test("Invalid Base64 (should fail)", tester.test_invalid_base64)
    
    if audio_file:
        tester.run_test("Valid Detection Request", 
                       lambda: tester.test_valid_detection_with_file(audio_file))
        tester.run_test("Different Languages", 
                       lambda: tester.test_different_languages(audio_file))
    else:
        print("\n⚠ Skipping audio tests (no audio file provided)")
    
    tester.run_test("Stats Endpoint", tester.test_stats_endpoint)
    
    # Print summary
    success = tester.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
