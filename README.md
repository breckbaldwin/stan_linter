---
title: "Stan Linter"
author: "Breck Baldwin"
date: "4/20/2020"
output: html_document
---

# Stan Linter
This is a heuristic linter for .stan programs that attemtps to enforce the stan program style guide from the [Stan User's Guide](https://mc-stan.org/users/documentation/). 

## Using the linter
You must have python 3 installed and be comfortable with the command line. 

1. Open a terminal and cd to the location of your .stan file. There is an example program in the distubution that we will use. 
2. `cd <path to stan_linter>`
3. `python stan_linter.py small.stan`
4. Output should be:

`linting small.stan`

`spaces needed around operator =:line number:10='  real<lower=0> sigma;'`

`missing space after char 19',':line number:14='  alpha ~ normal(5,10);'`

## Modifying the linter

I created the linter to help clean up .stan models in the user's guide and have just gotten started. The linter is line based and I have assumed that the .stan programs pass the Stan compiler. The linter is mostly a series of regular expressions that look for common problems and report back. 

A good way to add patterns is to add the desired output to the unit test file `stan_linter_test.py` and then add a subroutine to `stan_linter.py` to pass the test. The test program is run using `pytest` and the complete command to run is `pytest stan_linter_test.py`. 