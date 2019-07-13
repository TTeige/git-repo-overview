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
The generated output:

Checklist
- [ ] [eias-emottakstub](https://stash.adeo.no/projects/FEL/repos/eias-emottakstub/browse)
- [ ] [orkestratoren](https://stash.adeo.no/projects/FEL/repos/orkestratoren/browse)
- [ ] [testnorge-aareg](https://stash.adeo.no/projects/FEL/repos/testnorge-aareg/browse)
- [ ] [testnorge-arena](https://stash.adeo.no/projects/FEL/repos/testnorge-arena/browse)
- [ ] [testnorge-arena-inntekt](https://stash.adeo.no/projects/FEL/repos/testnorge-arena-inntekt/browse)
- [ ] [testnorge-bisys](https://stash.adeo.no/projects/FEL/repos/testnorge-bisys/browse)
- [ ] [testnorge-ereg-mapper](https://stash.adeo.no/projects/FEL/repos/testnorge-ereg-mapper/browse)
- [ ] [testnorge-hodejegeren](https://stash.adeo.no/projects/FEL/repos/testnorge-hodejegeren/browse)
- [ ] [testnorge-inst](https://stash.adeo.no/projects/FEL/repos/testnorge-inst/browse)
- [ ] [testnorge-medl](https://stash.adeo.no/projects/FEL/repos/testnorge-medl/browse)
- [ ] [testnorge-meldekort](https://stash.adeo.no/projects/FEL/repos/testnorge-meldekort/browse)
- [ ] [testnorge-nav-endringsmeldinger](https://stash.adeo.no/projects/FEL/repos/testnorge-nav-endringsmeldinger/browse)
- [ ] [testnorge-pen](https://stash.adeo.no/projects/FEL/repos/testnorge-pen/browse)
- [ ] [testnorge-sam](https://stash.adeo.no/projects/FEL/repos/testnorge-sam/browse)
- [ ] [testnorge-sigrun](https://stash.adeo.no/projects/FEL/repos/testnorge-sigrun/browse)
- [ ] [testnorge-skd](https://stash.adeo.no/projects/FEL/repos/testnorge-skd/browse)
- [ ] [testnorge-tp](https://stash.adeo.no/projects/FEL/repos/testnorge-tp/browse)
- [ ] [testnorge-inntektstub](https://github.com/navikt/testnorge-inntektstub)
- [ ] [testnorge-aaregstub](https://github.com/navikt/testnorge-aaregstub)
- [ ] [testnorge-ereg-mapper](https://github.com/navikt/testnorge-ereg-mapper)
- [ ] [testnorge-statisk-data-forvalter](https://github.com/navikt/testnorge-statisk-data-forvalter)


### Bitbucket api version note
The supported version of bitbucket api is 1.0. This is due to NAV only using this version.  


## Why make it?

During the development of the test infrastructure for NAV using micro-services we found that
we needed to maintain a list of applications which we had responsibility of developing. 

We didn't want to maintain it by hand, so I made a tool to find them based on some keywords.