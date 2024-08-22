# K8S
alias k="kubectl"

# ZSH Reconfigure
alias reconfigure-zsh="nano ${HOME}/.zshrc && omz reload && rehash"
alias reload-zsh="omz reload && rehash"
alias update-zsh="omz update"

alias zsu="sudo su --login --whitelist-environment=SSH_CLIENT,SSH_CONNECTION,SSH_TTY,P9K_SSH,TZ"
