# Git repository finder

A simple tool to find repositories spread between Bitbucket and Github. 

## Usage

`python3 main.py --help`

The tool uses the following environment variables:
* `GITHUB_USERNAME`
* `GITHUB_PASSWORD`
* `BITBUCKET_USERNAME`
* `BITBUCKET_PASSWORD`

Example usage to generate a markdown list of repositories with links:

`python3 main.py -i names -c -v -l --bitbucket --github --bitbucket_url <api url>`

where names is a file containing newline seperated names to search for.

### Bitbucket api version note
The supported version of bitbucket api is 1.0. This is due to NAV only using this version.  


## Why make it?

During the development of the test infrastructure for NAV using micro-services we found that
we needed to maintain a list of applications which we had responsibility of developing. 

We didn't want to maintain it by hand, so I made a tool to find them based on some keywords.