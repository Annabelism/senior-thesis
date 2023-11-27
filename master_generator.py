import multiprocessing
import os
from data100 import data

def run_script(script_name, url, site_name):
    site_name = site_name.replace(" ", "_")
    os.system(f'python {script_name} {url} {site_name}')

if __name__ == '__main__':
    for site in data:
        url = site["url"]
        name = site["site_name"]
        processes = []

        for script in ['no_ad_blocker.py', 'with_ad_blocker.py']:
            p = multiprocessing.Process(target=run_script, args=(script, url, name))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()