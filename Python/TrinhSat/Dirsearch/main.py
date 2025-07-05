import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import os
import time
from datetime import datetime
import threading
from queue import Queue
import signal
import sys
import re
from urllib.parse import urlparse, urljoin
import json
from typing import Dict, List, Optional, Callable

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class DirectoryScannerAPI:
    def __init__(self, base_url: str, wordlist_file: Optional[str] = None, 
                 threads: int = 50, timeout: int = 10, 
                 callback: Optional[Callable] = None):
        """
        Initialize the Directory Scanner API
        
        Args:
            base_url (str): Base URL to scan
            wordlist_file (str, optional): Path to wordlist file
            threads (int): Number of concurrent threads
            timeout (int): Request timeout in seconds
            callback (callable, optional): Callback function for real-time updates
        """
        # Validate and normalize the URL
        self.base_url = self._normalize_url(base_url)
        self.wordlist_file = wordlist_file
        self.threads = threads
        self.timeout = timeout
        self.callback = callback
        
        # Results storage
        self.results = []
        self.found_urls = []
        self.scanned_count = 0
        self.total_paths = 0
        self.start_time = None
        
        # Control flags
        self.is_scanning = False
        self.stop_requested = False
        self.stop_event = threading.Event()
        
        # Threading
        self.lock = threading.Lock()
        self.result_queue = Queue()
        self.scan_thread = None
        
        # Status codes that indicate success
        self.success_codes = ['2', '3']  # 2xx and 3xx status codes
        
        # Initialize wordlist path if not provided
        if not self.wordlist_file:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.wordlist_file = os.path.join(current_dir, "Dictionary", "dicc.txt")
        
        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()
    
    def _normalize_url(self, url_input: str) -> str:
        """
        Normalize and validate URL input
        
        Args:
            url_input (str): Raw URL input from user
            
        Returns:
            str: Normalized URL
        """
        # Remove leading/trailing whitespace
        url_input = url_input.strip()
        
        # Check if it's just a hostname (no protocol)
        if not url_input.startswith(('http://', 'https://')):
            # Check if it contains a path (has /)
            if '/' in url_input:
                # Assume http if no protocol specified
                url_input = 'http://' + url_input
            else:
                # Just hostname, assume http
                url_input = 'http://' + url_input
        
        # Parse the URL to validate it
        try:
            parsed = urlparse(url_input)
            
            # Check if we have at least a scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL format")
            
            # Normalize the URL (remove trailing slash, ensure proper format)
            normalized_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Add path if it exists (but not trailing slash)
            if parsed.path and parsed.path != '/':
                normalized_url += parsed.path.rstrip('/')
            
            return normalized_url
            
        except Exception as e:
            raise ValueError(f"Invalid URL '{url_input}': {str(e)}")
    
    def _test_connection(self) -> bool:
        """
        Test connection to the target URL
        
        Returns:
            bool: True if connection successful
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout, allow_redirects=False)
            
            if response.status_code in [200, 301, 302, 403, 401]:
                return True
            else:
                return True  # Still proceed, might be intentional
                
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            return False
        except Exception:
            return False
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.stop()
        
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    def _load_wordlist(self) -> List[str]:
        """
        Load paths from wordlist file
        
        Returns:
            list: List of paths to scan
        """
        if self.wordlist_file is None:
            raise ValueError("Wordlist file path is not set")
            
        if not os.path.exists(self.wordlist_file):
            raise FileNotFoundError(f"Wordlist file '{self.wordlist_file}' not found.")
        
        try:
            with open(self.wordlist_file, "r", encoding='utf-8') as f:
                paths = [line.strip() for line in f if line.strip()]
            return paths
            
        except Exception as e:
            raise Exception(f"Error reading wordlist file: {e}")
    
    def _check_url(self, path: str) -> Optional[Dict]:
        """
        Check if a specific path exists on the target
        
        Args:
            path (str): Path to check
            
        Returns:
            dict: Result information or None if stopped
        """
        # Check if stop was requested
        if self.is_stopped():
            return None
        
        url = f"{self.base_url}/{path}"
        result = {
            'url': url,
            'path': path,
            'status_code': None,
            'response_time': None,
            'error': None,
            'found': False,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=self.timeout, allow_redirects=False)
            response_time = time.time() - start_time
            
            result['status_code'] = response.status_code
            result['response_time'] = round(response_time, 3)
            
            # Check if status code indicates success
            if str(response.status_code)[0] in self.success_codes:
                result['found'] = True
            
        except requests.RequestException as e:
            result['error'] = str(e)
        
        # Update counters
        with self.lock:
            self.scanned_count += 1
        
        # Call callback if provided
        if self.callback:
            try:
                self.callback(result)
            except Exception:
                pass  # Don't let callback errors break the scan
        
        return result
    
    def _scan_worker(self):
        """Worker method for scanning in a separate thread"""
        try:
            # Test connection first
            if not self._test_connection():
                return
            
            # Load wordlist
            paths = self._load_wordlist()
            self.total_paths = len(paths)
            self.start_time = time.time()
            
            # Start scanning with ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                # Submit all tasks
                future_to_path = {executor.submit(self._check_url, path): path for path in paths}
                
                # Process completed tasks in real-time
                for future in as_completed(future_to_path):
                    # Check if stop was requested
                    if self.is_stopped():
                        break
                    
                    result = future.result()
                    if result is not None:
                        if result['found']:
                            self.found_urls.append(result)
                        self.results.append(result)
            
        except Exception as e:
            print(f"Scan error: {e}")
        finally:
            self.is_scanning = False
    
    def start_scan(self) -> bool:
        """
        Start the scanning process in a separate thread
        
        Returns:
            bool: True if scan started successfully
        """
        if self.is_scanning:
            return False
        
        self.is_scanning = True
        self.stop_requested = False
        self.stop_event.clear()
        self.scanned_count = 0
        self.results = []
        self.found_urls = []
        
        self.scan_thread = threading.Thread(target=self._scan_worker, daemon=True)
        self.scan_thread.start()
        return True
    
    def stop(self):
        """Stop the scanning process gracefully"""
        self.stop_requested = True
        self.stop_event.set()
    
    def is_stopped(self) -> bool:
        """Check if stop was requested"""
        return self.stop_requested or self.stop_event.is_set()
    
    def get_status(self) -> Dict:
        """
        Get current scan status
        
        Returns:
            dict: Current status information
        """
        status = {
            'is_scanning': self.is_scanning,
            'stop_requested': self.stop_requested,
            'scanned_count': self.scanned_count,
            'total_paths': self.total_paths,
            'found_urls_count': len(self.found_urls),
            'results_count': len(self.results)
        }
        
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            status['elapsed_time'] = round(elapsed_time, 2)
            if elapsed_time > 0:
                status['rate'] = round(self.scanned_count / elapsed_time, 1)
            
            if self.total_paths > 0:
                status['progress_percent'] = round((self.scanned_count / self.total_paths) * 100, 1)
        
        return status
    
    def get_results(self, found_only: bool = False) -> List[Dict]:
        """
        Get scan results
        
        Args:
            found_only (bool): Return only found URLs if True
            
        Returns:
            list: List of results
        """
        if found_only:
            return self.found_urls.copy()
        return self.results.copy()
    
    def get_found_urls(self) -> List[Dict]:
        """
        Get only found URLs
        
        Returns:
            list: List of found URLs
        """
        return self.found_urls.copy()
    
    def wait_for_completion(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for scan to complete
        
        Args:
            timeout (float, optional): Maximum time to wait in seconds
            
        Returns:
            bool: True if scan completed, False if timeout or stopped
        """
        if not self.is_scanning or self.scan_thread is None:
            return True
        
        if timeout:
            self.scan_thread.join(timeout=timeout)
            return not self.scan_thread.is_alive()
        else:
            self.scan_thread.join()
            return True
    
    def save_results(self, filename: Optional[str] = None, found_only: bool = True) -> str:
        """
        Save scan results to file
        
        Args:
            filename (str, optional): Output filename
            found_only (bool): Save only found URLs if True
            
        Returns:
            str: Filename where results were saved
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_results_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Directory Scan Results\n")
                f.write(f"Target: {self.base_url}\n")
                f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Scanned: {self.scanned_count}\n")
                f.write(f"Found URLs: {len(self.found_urls)}\n")
                f.write("-" * 50 + "\n\n")
                
                results_to_save = self.found_urls if found_only else self.results
                for result in results_to_save:
                    f.write(f"{result['url']} (Status: {result['status_code']})\n")
            
            return filename
            
        except Exception as e:
            raise Exception(f"Error saving results: {e}")
    
    def get_summary(self) -> Dict:
        """
        Get scan summary
        
        Returns:
            dict: Summary information
        """
        summary = {
            'target': self.base_url,
            'total_scanned': self.scanned_count,
            'found_urls': len(self.found_urls),
            'total_results': len(self.results),
            'is_completed': not self.is_scanning,
            'was_interrupted': self.stop_requested
        }
        
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            summary['elapsed_time'] = round(elapsed_time, 2)
            if elapsed_time > 0:
                summary['average_rate'] = round(self.scanned_count / elapsed_time, 1)
        
        return summary


# Example callback function for real-time updates
def print_result_callback(result: Dict):
    """Example callback function to print results in real-time"""
    if result['found']:
        status_color = Fore.GREEN if result['status_code'] == 200 else Fore.YELLOW
        print(f"{status_color}[+] Found: {result['path']} (Status: {result['status_code']}, Time: {result['response_time']}s){Style.RESET_ALL}")
    elif result['error']:
        print(f"{Fore.RED}[!] Error: {result['path']} - {result['error']}{Style.RESET_ALL}")



"""Simple test function to verify the API works"""
scanner = DirectoryScannerAPI(
    base_url="http://testphp.vulnweb.com/",
    threads=10,
    timeout=5,
    callback=print_result_callback
)
    
print("Starting test scan...")
scanner.start_scan()
scanner.wait_for_completion()
    
found_urls = scanner.get_found_urls()
print(f"\nTest completed. Found {len(found_urls)} URLs")
