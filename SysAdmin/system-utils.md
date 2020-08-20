## `entr`
`entr` as one-line `modd`: `ls file | entr -s 'cmd'`


## Replacement for built-in commands
```shell
alias ls="exa"
alias grep="ag"
alias find="fd"
alias du="dust"
alias ps="procs"
```
* `hyperfine` for performance testing


## Batch converting svg to png

The following will create png for svg files in A5 size with 300DPI.
`cairosvg` has nice support for fonts.

`find . -name "*.svg" -exec cairosvg --output-width 1740 --output-height 2490  -f png {} -o {}.png \;`




