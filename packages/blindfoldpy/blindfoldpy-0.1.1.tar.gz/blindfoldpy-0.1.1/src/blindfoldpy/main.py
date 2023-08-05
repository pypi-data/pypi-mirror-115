import argparse
import requests
import sys
from urllib.parse import urljoin

API_URL='https://www.toptal.com/developers/gitignore/api/'

def get_all():
    r = requests.get(urljoin(API_URL,'list'))

    gitignores =[] 

    for line in r.text.split('\n'):
        for tech in line.split(','):
            gitignores.append(tech)    

    print("\n".join(gitignores))

def get_gitignore(req_str):
    print(req_str)
    r = requests.get(urljoin(API_URL,req_str))
    gitignore = r.text.split("\n")
    gitignore.insert(2, '# Automated by https://github.com/iwishiwasaneagle/blindfold.py')
    print("\n".join(gitignore))

def main(args = None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Don\'t use this. Use the real blindfold. I\'m just trying to spite the original author who\'s a close friend of mine.')
    parser.add_argument('-l','--list', 
                        action='store_true',
                        help='List all tech and tech stacks available')
    parser.add_argument('-o','--opts', 
                        nargs='*',
                        help="The tech or tech stack you are using in your project. Example: \"python node\"")

    args = parser.parse_args(args=args)

    if args.list:
        get_all()
        exit
    elif args.opts:
        req_str = ""
        for tech in args.opts:
            req_str+=tech+","        
        req_str = req_str[0:-1]
        get_gitignore(req_str)
        exit
    else:
        parser.print_help()
        exit

if __name__ == "__main__":
    main()
