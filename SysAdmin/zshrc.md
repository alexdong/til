```vim
ZSH_THEME="agnoster"

DISABLE_AUTO_TITLE="true"
ENABLE_CORRECTION="true"
plugins=(aws brew dotenv iterm2 git pip python pylint ssh-agent vi-mode virtualenv yarn z)

export EDITOR='vim'
export LANG=en_NZ.UTF-8
export LC_ALL=en_NZ.UTF-8
export ARCHFLAGS="-arch x86_64"

export FLASK_APP='happymoose.app'

alias vz="vim ~/.zshrc"
alias sz="source ~/.zshrc"
alias gs="git status"
alias ga="git add ."
alias gz="git cz"
alias gcm="git checkout master"
alias gmm="git merge master"
alias gp="git push"
alias g="git pull"
```
