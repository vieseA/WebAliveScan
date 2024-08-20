from lib.common.request import Request
from lib.common.output import Output
from lib.utils.wappalyzer import Wappalyzer
from lib.common.dirbrute import Dirbrute
from lib.utils.tools import *
import fire
import time
import logging
import concurrent.futures

logging.basicConfig(filename='program.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Program(object):
    def __init__(self, target, port, brute=False, delay=0, headers=None, proxy=None, wordlist=None, output_format='json', credentials=None):
        self.output = Output(output_format=output_format)
        self.wappalyzer = Wappalyzer(detailed=True)  # Enable detailed technology fingerprinting
        self.request = Request(target, port, self.output, self.wappalyzer, headers=headers, proxy=proxy)
        
        # Save the alive paths to a file
        save_result(self.request.alive_path, 
                    ['url', 'title', 'status', 'size', 'server', 'language', 'application', 'frameworks', 'system', 'versions'], 
                    self.request.alive_result_list, output_format=output_format)
        self.output.resultOutput(f'Alive result saved to: {self.request.alive_path}')
        logging.info(f'Alive result saved to: {self.request.alive_path}')
        
        # Test credentials if provided
        if credentials:
            self.test_credentials(target, credentials)
        
        # Perform directory brute-forcing if required
        if brute:
            self.run_brute_force(self.request.alive_result_list, delay, wordlist)
    
    def run_brute_force(self, alive_result_list, delay, wordlist):
        brute_result_list = []
        self.output.newLine('')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.run_dirbrute, info.get('url'), brute_result_list, wordlist): info for info in alive_result_list}
            for future in concurrent.futures.as_completed(futures):
                future.result()
                time.sleep(delay)  # Adding delay between brute force attempts if specified
                
        # Save the brute-force results to a file
        save_result(self.request.brute_path, ['url', 'status', 'size'], brute_result_list, output_format=self.output.output_format)
        self.output.resultOutput(f'Brute result saved to: {self.request.brute_path}')
        logging.info(f'Brute result saved to: {self.request.brute_path}')
    
    def run_dirbrute(self, url, brute_result_list, wordlist):
        dirbrute = Dirbrute(url, self.output, brute_result_list, wordlist=wordlist)
        dirbrute.run()
    
    def test_credentials(self, target, credentials):
        # Placeholder for credential testing logic
        # You could implement a loop here to test the credentials against the target
        self.output.resultOutput(f'Testing credentials for target: {target}')
        logging.info(f'Testing credentials for target: {target}')
        # Example pseudo-implementation
        for username, password in credentials:
            # Attempt login and log success/failure
            success = self.attempt_login(target, username, password)
            if success:
                self.output.resultOutput(f'Credentials found: {username}:{password}')
                logging.info(f'Credentials found: {username}:{password}')
            else:
                self.output.resultOutput(f'Failed login attempt: {username}:{password}')
                logging.info(f'Failed login attempt: {username}:{password}')
    
    def attempt_login(self, target, username, password):
        # Placeholder for actual login logic
        # Return True if login is successful, otherwise False
        return False  # This should be replaced with actual login attempt logic

def run(target, port, brute=False, delay=0, headers=None, proxy=None, wordlist=None, output_format='json', credentials=None):
    main = Program(target, port, brute, delay, headers, proxy, wordlist, output_format, credentials)

if __name__ == '__main__':
    fire.Fire(run)
