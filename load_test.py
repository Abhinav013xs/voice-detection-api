#!/usr/bin/env python3
"""
Load Testing Script for AI Voice Detection API
Tests API performance under concurrent requests
"""

import requests
import base64
import time
import threading
import queue
from datetime import datetime
import statistics
import sys

class LoadTester:
    def __init__(self, endpoint_url, api_key, audio_file):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.audio_file = audio_file
        self.results = queue.Queue()
        self.audio_base64 = None
        self.audio_format = None
        
        # Load audio file
        self._load_audio()
    
    def _load_audio(self):
        """Load and encode audio file once"""
        try:
            with open(self.audio_file, 'rb') as f:
                audio_bytes = f.read()
            
            self.audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            self.audio_format = self.audio_file.split('.')[-1].lower()
            
            print(f"✓ Audio file loaded: {self.audio_file}")
            print(f"  Size: {len(audio_bytes)} bytes")
            print(f"  Format: {self.audio_format}")
            
        except Exception as e:
            print(f"✗ Error loading audio file: {e}")
            sys.exit(1)
    
    def make_request(self, request_id):
        """Make a single API request"""
        try:
            start_time = time.time()
            
            response = requests.post(
                self.endpoint_url,
                headers={
                    'x-api-key': self.api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'language': 'en',
                    'audio_format': self.audio_format,
                    'audio_base64': self.audio_base64
                },
                timeout=60
            )
            
            elapsed = time.time() - start_time
            
            result = {
                'request_id': request_id,
                'status_code': response.status_code,
                'response_time': elapsed,
                'success': response.status_code == 200,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            if response.status_code == 200:
                data = response.json()
                result['prediction'] = data.get('result', {}).get('prediction')
            else:
                result['error'] = response.text
            
            self.results.put(result)
            
        except Exception as e:
            self.results.put({
                'request_id': request_id,
                'status_code': 0,
                'response_time': 0,
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            })
    
    def run_concurrent_test(self, num_requests, num_threads):
        """Run concurrent load test"""
        print(f"\n{'='*70}")
        print(f"LOAD TEST: {num_requests} requests with {num_threads} concurrent threads")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        threads = []
        requests_per_thread = num_requests // num_threads
        
        # Create and start threads
        for i in range(num_threads):
            thread_requests = requests_per_thread
            if i == num_threads - 1:
                # Last thread handles remaining requests
                thread_requests += num_requests % num_threads
            
            for j in range(thread_requests):
                request_id = i * requests_per_thread + j + 1
                thread = threading.Thread(
                    target=self.make_request,
                    args=(request_id,)
                )
                threads.append(thread)
                thread.start()
                
                # Add small delay between thread starts to avoid overwhelming
                if len(threads) % num_threads == 0:
                    time.sleep(0.1)
        
        # Wait for all threads to complete
        print(f"Waiting for {len(threads)} requests to complete...")
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # Collect results
        results = []
        while not self.results.empty():
            results.append(self.results.get())
        
        self._print_results(results, total_time)
        return results
    
    def run_sequential_test(self, num_requests):
        """Run sequential load test"""
        print(f"\n{'='*70}")
        print(f"SEQUENTIAL TEST: {num_requests} requests")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        for i in range(num_requests):
            print(f"Request {i+1}/{num_requests}...", end='\r')
            self.make_request(i + 1)
        
        total_time = time.time() - start_time
        
        # Collect results
        results = []
        while not self.results.empty():
            results.append(self.results.get())
        
        print()  # New line after progress
        self._print_results(results, total_time)
        return results
    
    def _print_results(self, results, total_time):
        """Print test results"""
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"\n{'='*70}")
        print("LOAD TEST RESULTS")
        print(f"{'='*70}\n")
        
        print(f"Total Requests: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        print(f"Success Rate: {len(successful)/len(results)*100:.2f}%")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Requests/Second: {len(results)/total_time:.2f}")
        
        if successful:
            response_times = [r['response_time'] for r in successful]
            print(f"\nResponse Times:")
            print(f"  Min: {min(response_times):.3f}s")
            print(f"  Max: {max(response_times):.3f}s")
            print(f"  Mean: {statistics.mean(response_times):.3f}s")
            print(f"  Median: {statistics.median(response_times):.3f}s")
            
            if len(response_times) > 1:
                print(f"  Std Dev: {statistics.stdev(response_times):.3f}s")
            
            # Percentiles
            sorted_times = sorted(response_times)
            p50 = sorted_times[len(sorted_times)//2]
            p90 = sorted_times[int(len(sorted_times)*0.9)]
            p95 = sorted_times[int(len(sorted_times)*0.95)]
            p99 = sorted_times[int(len(sorted_times)*0.99)] if len(sorted_times) > 100 else sorted_times[-1]
            
            print(f"\nPercentiles:")
            print(f"  P50: {p50:.3f}s")
            print(f"  P90: {p90:.3f}s")
            print(f"  P95: {p95:.3f}s")
            print(f"  P99: {p99:.3f}s")
        
        if failed:
            print(f"\nFailed Requests:")
            error_types = {}
            for r in failed:
                error = r.get('error', 'Unknown')
                error_types[error] = error_types.get(error, 0) + 1
            
            for error, count in error_types.items():
                print(f"  {error}: {count}")
        
        print(f"\n{'='*70}\n")
    
    def run_ramp_test(self, max_threads, step=1, requests_per_step=10):
        """Run ramp-up load test"""
        print(f"\n{'='*70}")
        print(f"RAMP TEST: 1 to {max_threads} threads")
        print(f"{'='*70}\n")
        
        all_results = []
        
        for num_threads in range(1, max_threads + 1, step):
            print(f"\nTesting with {num_threads} concurrent threads...")
            results = self.run_concurrent_test(requests_per_step, num_threads)
            all_results.extend(results)
            time.sleep(1)  # Brief pause between ramp steps
        
        return all_results

def main():
    if len(sys.argv) < 4:
        print("Usage: python load_test.py <endpoint_url> <api_key> <audio_file> [mode] [params...]")
        print("\nModes:")
        print("  sequential <num_requests>")
        print("  concurrent <num_requests> <num_threads>")
        print("  ramp <max_threads> [step] [requests_per_step]")
        print("\nExamples:")
        print("  python load_test.py http://localhost:5000/detect api-key sample.mp3 sequential 10")
        print("  python load_test.py http://localhost:5000/detect api-key sample.mp3 concurrent 100 10")
        print("  python load_test.py http://localhost:5000/detect api-key sample.mp3 ramp 10 2 5")
        sys.exit(1)
    
    endpoint_url = sys.argv[1]
    api_key = sys.argv[2]
    audio_file = sys.argv[3]
    mode = sys.argv[4] if len(sys.argv) > 4 else 'sequential'
    
    tester = LoadTester(endpoint_url, api_key, audio_file)
    
    if mode == 'sequential':
        num_requests = int(sys.argv[5]) if len(sys.argv) > 5 else 10
        tester.run_sequential_test(num_requests)
    
    elif mode == 'concurrent':
        num_requests = int(sys.argv[5]) if len(sys.argv) > 5 else 100
        num_threads = int(sys.argv[6]) if len(sys.argv) > 6 else 10
        tester.run_concurrent_test(num_requests, num_threads)
    
    elif mode == 'ramp':
        max_threads = int(sys.argv[5]) if len(sys.argv) > 5 else 10
        step = int(sys.argv[6]) if len(sys.argv) > 6 else 1
        requests_per_step = int(sys.argv[7]) if len(sys.argv) > 7 else 10
        tester.run_ramp_test(max_threads, step, requests_per_step)
    
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == '__main__':
    main()
