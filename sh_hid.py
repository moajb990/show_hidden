#importing libs
import queue
import threading
import urllib.error
import urllib.parse
import urllib.request
import optparse
import sys

#colors i need
green = "\033[92m"
red = "\033[91m"
close = "\033[0m"

#some values
file_extensions = [
    ".php", ".html", ".css", ".js", ".json", ".xml", 
    ".txt", ".bak", ".config", ".sql", ".log", 
    ".orig", ".asp", ".jsp"
]
resume = None

def get_argument():
    #create arguments -_-
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="target_url", help="need target url")
    parser.add_option("-w", "--wordlist", dest="wordlist", help="need wordlist")
    parser.add_option("-t", "--threads", type=int, default=30, dest="thread_number", help="need threading")
    parser.add_option("-a", "--useragent", default="Mozilla/5.0", dest="user_agent", help="need useragent")
    
    options, arguments = parser.parse_args()
    
    #check if the args -u -w is exists
    if not options.target_url:
        parser.error('[-] You Forgot To Put target url, Type -h,--help For Usage')
    if not options.wordlist:
        parser.error('[-] You Forgot To Put wordlist, Type -h,--help For Usage')
    
    return options

def build_wordlist():
    #building the wordlist
    with open(options.wordlist, "r") as l:
        raw_words = [line.rstrip("\n") for line in l]

    found_resume = False
    words = queue.Queue()

    # add the words
    for word in raw_words:
        if resume:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print(f"Resuming wordlist from: {resume}")
        else:
            words.put(word)
    return words

def dir_bruter(extensions=None):

    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # check extensions and.. 
        if "." not in attempt:
            attempt_list.append(f"/{attempt}/")
        else:
            attempt_list.append(f"/{attempt}")
        
        # try all extensions
        if extensions:
            for extension in extensions:
                attempt_list.append(f"/{attempt}{extension}")
            
        for brute in attempt_list:
            url = f"{options.target_url}{urllib.parse.quote(brute)}"
            
            try:
                headers = {"User-Agent": options.user_agent}
                r = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(r)
                
                content_length = len(response.read())
                size_kb = content_length / 1024
                
                if content_length > 0:
                    print(green + f"[+] {response.code} - {size_kb:.2f}KB  ==> {url}" + close)
                   
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    print(red + f"[-] {e.code} - {size_kb:.2f}KB ==> {url}" + close)

# get arguments
options = get_argument()

# build the wordlist
word_queue = build_wordlist()

# start threading 
for thread in range(options.thread_number):
    t = threading.Thread(target=dir_bruter, args=(file_extensions,))
    t.start()
