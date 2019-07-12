import argparse
import os
import re
from collections import namedtuple

import requests
from requests.auth import HTTPBasicAuth


def input_args():
    parser = argparse.ArgumentParser(description='Create a list of repositories pertinent to a team')
    parser.add_argument('--bitbucket_password', '-p', dest='b_pw',
                        default=os.environ.get("BITBUCKET_PASSWORD"),
                        help='password for bitbucket')
    parser.add_argument('--https_proxy', default='socks5://localhost:14122',
                        help='proxy for https')
    parser.add_argument('--http_proxy', default='socks5://localhost:14122',
                        help='proxy for http')
    parser.add_argument('--bitbucket_username', '-u', dest='b_user',
                        default=os.environ.get("BITBUCKET_USERNAME"),
                        help='username for bitbucket')
    parser.add_argument('--search_regex', '-x', dest='regex',
                        help='regex which is used to search for the repositories')
    parser.add_argument('--repository_name_file', '-i', help='list of names to be searched for')
    parser.add_argument('--strict_list_search', help='does the list contain qualified names?')
    parser.add_argument('--names', '-m', nargs='*', help='names to search for')
    parser.add_argument('--checklist', '-c', help='create a markdown checklist for the found repos',
                        action='store_true')
    parser.add_argument('--output', '-o', help='output file name', default='checklist.md')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--links_inline', '-l', dest='links', help='write output as links', action='store_true')
    parser.add_argument('--bitbucket_url', help='repository base url', default='https://stash.adeo.no/rest/api/1.0')
    parser.add_argument('--bitbucket', help='Search bitbucket for repositories', default=True, action='store_true')
    parser.add_argument('--github', help='Search Github for repositories', default=True, action='store_true')
    parser.add_argument('--github_login_user', help='Github username', default=os.environ.get("GITHUB_USERNAME"),
                        dest='g_user')
    parser.add_argument('--github_login_password', help='Github password', default=os.environ.get("GITHUB_PASSWORD"),
                        dest='g_pw')
    parser.add_argument('--github_org', help='Organization to search through', default='navikt')
    parser.add_argument('--github_user', help='User to search through')
    parser.add_argument('--exclude', help='exclude names', nargs='*')

    return parser.parse_args()


def load_from_bitbucket(repo_obj):
    name = repo_obj.name
    link = ""
    for l in repo_obj.links:
        for l2 in l:
            if not hasattr(l2, 'name'):
                link = l2.href
    return Repository(name, link)


def load_from_github(repo_obj):
    return Repository(repo_obj.name, repo_obj.html_url)


class Repository:
    def __init__(self, name, link):
        self.name = name
        self.link = link


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def get_names_from_file(args):
    if args.repository_name_file is not None:
        if args.names is None:
            args.names = []
        if os.path.exists(args.repository_name_file):
            with open(args.repository_name_file, 'r') as f:
                for l in f:
                    args.names.append(l.strip('\n'))


def match_regex(args, matching_repos, i):
    if args.regex is not None:
        match = re.search(args.regex, i.name, re.M | re.I)
        if match:
            matching_repos.append(load_from_bitbucket(i))


def match_names(args, matching_repos, i):
    if args.names is not None:
        for name in args.names:
            if name in i.name:
                matching_repos.append(load_from_bitbucket(i))


def get_bitbucket_repos(args, proxies, obj=None):
    if obj is not None:
        resp = requests.get(args.bitbucket_url + "/projects/FEL/repos?start=" + str(obj.nextPageStart), verify=False,
                            auth=HTTPBasicAuth(args.b_user, args.b_pw),
                            proxies=proxies)
    else:
        resp = requests.get(args.bitbucket_url + "/projects/FEL/repos", verify=False,
                            auth=HTTPBasicAuth(args.b_user, args.b_pw),
                            proxies=proxies)
    return resp.json(object_hook=_json_object_hook)


def get_filter_repos(args, matching_repos):
    to_remove = []
    if args.exclude is not None:
        for r in matching_repos:
            for e in args.exclude:
                if e in r.name:
                    to_remove.append(r)
    return to_remove


def create_checklist(args, matching_repos):
    s = "Checklist\n"
    for repo_list in matching_repos:
        for r in repo_list:
            if args.links:
                s += '- [ ] [' + r.name + '](' + r.link + ')\n'
            else:
                s += '- [ ] ' + r.name + '\n'
    if args.checklist:
        with open(args.output, 'w+') as f:
            f.write(s)
    if args.verbose:
        print(s, end='')


def handle_bitbucket(args):
    proxies = {
        'https': args.https_proxy,
        'http': args.http_proxy,
    }
    matching_repos = []
    obj = get_bitbucket_repos(args, proxies)

    while not obj.isLastPage:
        for i in obj.values:
            match_regex(args, matching_repos, i)
            match_names(args, matching_repos, i)

        obj = get_bitbucket_repos(args, proxies, obj)

    to_remove = get_filter_repos(args, matching_repos)

    return [x for x in matching_repos if x not in to_remove]


def handle_github(args):
    if args.github_user != "" and args.github_user is not None:
        query_string = "/search/repositories?q=user:" + args.github_user
    else:
        names = ""
        if args.names is not None:
            # names = "+".join(args.names) + "+"
            names = args.names[2] + "+"
        query_string = "/search/repositories?q=" + names + "org:" + args.github_org

    return get_github_repos(args, query_string)


def get_github_repos(args, query_string):
    resp = requests.get("https://api.github.com" + query_string, auth=HTTPBasicAuth(args.g_user, args.g_pw))
    if resp.status_code != 200:
        return

    last = resp.links.get("last", {}).get("url", "")
    current = resp.links.get("next", {}).get("url", "")
    obj = resp.json(object_hook=_json_object_hook)

    repos = [load_from_github(o) for o in obj.items]

    while current != last:
        resp = requests.get(current,
                            auth=HTTPBasicAuth(args.g_user, args.g_pw))

        obj = resp.json(object_hook=_json_object_hook)
        current = resp.links.get("next", {}).get("url", "")
        repos.extend([load_from_github(o) for o in obj.items])

    return repos


def main(args):
    get_names_from_file(args)
    matching_repos = []
    if args.bitbucket:
        matching_repos.append(handle_bitbucket(args))
    if args.github:
        matching_repos.append(handle_github(args))
    if args.checklist or args.verbose:
        create_checklist(args, matching_repos)


if __name__ == '__main__':
    main(input_args())
