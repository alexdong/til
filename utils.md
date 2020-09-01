## References

* Conventions for Command line options: https://nullprogram.com/blog/2020/08/01/


## Productivity tools
* convert to epub for Apple Books: `brew install calibre` will get us the tool. Then use `ebook-convert UnixHistory.pdf unix-history.epub` for the actual conversion. 
`entr` as one-line `modd`: `ls file | entr -s 'cmd'`
* `hyperfine` for performance testing
* `tldr` as an example driven approach to `man`
* `mdn` to quickly search MDN: `npm install -g mdn-search`


## Replacement for default unix tools
alias ls="exa"
alias grep="ag"
alias find="fd"
alias du="dust"
alias ps="procs"



