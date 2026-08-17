# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# ==============================================================================
# 1. PLUGIN MANAGER (Zinit)
# ==============================================================================
### Added by Zinit's installer
if [[ ! -f $HOME/.local/share/zinit/zinit.git/zinit.zsh ]]; then
    print -P "%F{33} %F{220}Installing %F{33}ZDHARMA-CONTINUUM%F{220} Initiative Plugin Manager (%F{33}zdharma-continuum/zinit%F{220})…%f"
    command mkdir -p "$HOME/.local/share/zinit" && command chmod g-rwX "$HOME/.local/share/zinit"
    command git clone https://github.com/zdharma-continuum/zinit "$HOME/.local/share/zinit/zinit.git" && \
        print -P "%F{33} %F{34}Installation successful.%f%b" || \
        print -P "%F{160} The clone has failed.%f%b"
fi

source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# Initialize Zsh Completion System (Fixes 'compdef: command not found')
autoload -Uz compinit
compinit -C

# Load a few important annexes, without Turbo
zinit light-mode for \
    zdharma-continuum/zinit-annex-as-monitor \
    zdharma-continuum/zinit-annex-bin-gem-node \
    zdharma-continuum/zinit-annex-patch-dl \
    zdharma-continuum/zinit-annex-rust

# Load Powerlevel10k theme
zinit ice depth=1; zinit light romkatv/powerlevel10k

# Fast syntax highlighting and inline auto-suggestions
zinit light zsh-users/zsh-autosuggestions
zinit light zsh-users/zsh-syntax-highlighting

# fzf keybindings & fuzzy completion
zinit light Aloxaf/fzf-tab

# === Zinit Initialization ===
# (Your existing Zinit setup here)

# === Load fzf-tab ===
zinit light Aloxaf/fzf-tab

# === Completion Configuration ===
autoload -Uz compinit && compinit

# Case-insensitive + substring matching
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'

# Use colored menu selection
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"

# ==============================================================================
# 2. KEYBINDINGS & BEHAVIOR
# ==============================================================================
# PC-style navigation and word deletion
bindkey '^H' backward-kill-word             # Ctrl + Backspace
bindkey '^[[1;5D' backward-word             # Ctrl + Left Arrow
bindkey '^[[1;5C' forward-word             # Ctrl + Right Arrow

# Accept autosuggestions with Right Arrow
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=8'
bindkey '^[[C' forward-char                 # Right-arrow accepts autosuggestion

# Zsh Options
setopt glob_dots                            # Do not hide dotfiles in globs
setopt no_auto_menu                         # Require extra TAB press for menu
autoload -Uz zmv

# ==============================================================================
# 3. ENVIRONMENT & PATHS
# ==============================================================================
export GPG_TTY=$TTY

# Modern Zsh PATH definition
typeset -U path
path=(
  ~/bin
  /home/atg/.spicetify
  /opt/nvim-linux-x86_64/bin
  /home/atg/.opencode/bin
  $path
)

# Python uv env startup
[[ -f "$HOME/.local/bin/env" ]] && . "$HOME/.local/bin/env"

# ==============================================================================
# 4. LAZY-LOADED NVM
# ==============================================================================
export NVM_DIR="$HOME/.nvm"
zsh-defer-nvm() {
  unset -f nvm node npm yarn
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
}
nvm()  { zsh-defer-nvm; nvm "$@"; }
node() { zsh-defer-nvm; node "$@"; }
npm()  { zsh-defer-nvm; npm "$@"; }
yarn() { zsh-defer-nvm; yarn "$@"; }

# ==============================================================================
# 5. FUNCTIONS & ALIASES
# ==============================================================================
# Create directory and jump into it
function md() { [[ $# == 1 ]] && mkdir -p -- "$1" && cd -- "$1" }
compdef _directories md

# Standard aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ls='ls --color=auto'

# Custom workflow aliases
alias c='clear'
alias p='systemctl poweroff -i'
alias u='sudo dnf update'
alias n='nvim'
alias oc='opencode'

# Source local overrides if present
[[ -f ~/.env.zsh ]] && source ~/.env.zsh

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
