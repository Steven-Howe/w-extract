```usage: w-extract [-h] [-p] [-v] [-A] [-c] [-u] [-o OUTFILE] filepath

w-extract creates custom wordlists by extracting pathnames (default behavior), parameter names, or parameter values from URLs   
to aid in web discovery and exploitation efforts.

positional arguments:
  filepath              filepath of file containing list of URLs

optional arguments:
  -h, --help            show this help message and exit
  -p, --parameters      extracts found parameter names into a wordlist
  -v, --values          extracts found parameter values into a wordlist
  -A, --all             extracts pathnames, parameter names, and values into a wordlist
  -c, --count           counts occurences of extracted items
  -u, --urldecode       URL decodes values
  -o OUTFILE, --outfile OUTFILE
                        filepath of file which output will be written to

Written by Steven Howe, v1.0
```
