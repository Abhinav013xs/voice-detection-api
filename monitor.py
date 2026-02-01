#!/usr/bin/env python3
"""
API Monitoring and Health Check Script
Continuously monitors the API health and logs results
"""

import requests
import time
import json
from datetime import datetime
import sys

class APIMonitor:
    def __init__(self, base_url, api_key, check_interval=60):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.check_interval = check_interval
        self.log_file = 'api_monitor.log'
        self.stats = {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'average_response_time': 0,
            'uptime_percentage': 0
        }
    
    def log_message(self, message, level='INFO'):
        """Log message to file and console"""
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def check_health(self):
        """Check API health endpoint"""
        try:
            start_time = time.time()
            response = requests.get(
                f"{self.base_url}/health",
                timeout=10
            )
            response_time = time.time() - start_time
            
            self.stats['total_checks'] += 1
            
            if response.status_code == 200:
                self.stats['successful_checks'] += 1
                self.log_message(
                    f"✓ Health check passed (Response time: {response_time:.3f}s)",
                    'INFO'
                )
                return True, response_time
            else:
                self.stats['failed_checks'] += 1
                self.log_message(
                    f"✗ Health check failed (Status: {response.status_code})",
                    'WARNING'
                )
                return False, response_time
                
        except requests.exceptions.Timeout:
            self.stats['failed_checks'] += 1
            self.stats['total_checks'] += 1
            self.log_message("✗ Health check timeout", 'ERROR')
            return False, 10.0
            
        except requests.exceptions.ConnectionError:
            self.stats['failed_checks'] += 1
            self.stats['total_checks'] += 1
            self.log_message("✗ Connection error - API may be down", 'ERROR')
            return False, 0
            
        except Exception as e:
            self.stats['failed_checks'] += 1
            self.stats['total_checks'] += 1
            self.log_message(f"✗ Unexpected error: {e}", 'ERROR')
            return False, 0
    
    def check_endpoint_response(self):
        """Check main endpoint with dummy request"""
        try:
            start_time = time.time()
            response = requests.get(
                self.base_url,
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'active':
                    self.log_message(
                        f"✓ Root endpoint responsive (Response time: {response_time:.3f}s)",
                        'INFO'
                    )
                    return True, response_time
            
            self.log_message(
                f"⚠ Root endpoint returned unexpected response",
                'WARNING'
            )
            return False, response_time
            
        except Exception as e:
            self.log_message(f"✗ Endpoint check error: {e}", 'ERROR')
            return False, 0
    
    def update_stats(self, response_time):
        """Update monitoring statistics"""
        # Calculate average response time
        if self.stats['successful_checks'] > 0:
            current_avg = self.stats['average_response_time']
            new_avg = ((current_avg * (self.stats['successful_checks'] - 1)) + response_time) / self.stats['successful_checks']
            self.stats['average_response_time'] = new_avg
        
        # Calculate uptime percentage
        if self.stats['total_checks'] > 0:
            self.stats['uptime_percentage'] = (self.stats['successful_checks'] / self.stats['total_checks']) * 100
    
    def print_stats(self):
        """Print current statistics"""
        print("\n" + "="*70)
        print("MONITORING STATISTICS")
        print("="*70)
        print(f"Total Checks: {self.stats['total_checks']}")
        print(f"Successful: {self.stats['successful_checks']}")
        print(f"Failed: {self.stats['failed_checks']}")
        print(f"Uptime: {self.stats['uptime_percentage']:.2f}%")
        print(f"Avg Response Time: {self.stats['average_response_time']:.3f}s")
        print("="*70 + "\n")
    
    def run(self, duration=None):
        """
        Run monitoring loop
        duration: Total monitoring duration in seconds (None = infinite)
        """
        self.log_message("Starting API monitoring...", 'INFO')
        self.log_message(f"Target: {self.base_url}", 'INFO')
        self.log_message(f"Check interval: {self.check_interval}s", 'INFO')
        
        start_time = time.time()
        checks_count = 0
        
        try:
            while True:
                # Check if duration exceeded
                if duration and (time.time() - start_time) >= duration:
                    self.log_message("Monitoring duration completed", 'INFO')
                    break
                
                # Perform health check
                success, response_time = self.check_health()
                
                if success:
                    self.update_stats(response_time)
                    
                    # Also check root endpoint every 5 checks
                    checks_count += 1
                    if checks_count % 5 == 0:
                        self.check_endpoint_response()
                
                # Print stats every 10 checks
                if checks_count % 10 == 0:
                    self.print_stats()
                
                # Wait for next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log_message("\nMonitoring stopped by user", 'INFO')
        
        finally:
            self.print_stats()
            self.log_message("Monitoring session ended", 'INFO')

def main():
    if len(sys.argv) < 2:
        print("Usage: python monitor.py <base_url> [api_key] [interval] [duration]")
        print("\nExample:")
        print("  python monitor.py http://localhost:5000")
        print("  python monitor.py https://your-api.com api-key 30")
        print("  python monitor.py https://your-api.com api-key 60 3600  # Monitor for 1 hour")
        print("\nPress Ctrl+C to stop monitoring")
        sys.exit(1)
    
    base_url = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else 'hackathon-api-key-2024'
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    duration = int(sys.argv[4]) if len(sys.argv) > 4 else None
    
    monitor = APIMonitor(base_url, api_key, interval)
    monitor.run(duration)

if __name__ == '__main__':
    main()
