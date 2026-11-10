# Using GNU Stow in this dotfiles repo

A reference dialogue for adding new configs to `dotfiles/` in the future.

**Q: How does stow decide where files end up?**

**A:** Stow maps a package's top level onto the target, which for this repo is always `$HOME`. So the package layout is the real path with the `$HOME/` prefix cut off and replaced by the package name:

```
real file:   ~/.config/fastfetch/config.jsonc
package:     dotfiles/fastfetch/.config/fastfetch/config.jsonc
                               ^ package name (= one dir at stow top level)
```

**Q: A new app left a config in `~/.config`. How do I back it up with this method?**

**A:** Move the files into a package, then stow. Never leave real files in both places — the package copy is the source of truth, `~/.config` only gets symlinks.

```bash
cd /home/atg/Programs/configuration

# 1. mirror the path into a package (mkdir -p creates all levels)
mkdir -p dotfiles/APP/.config/APP
mv ~/.config/APP/... dotfiles/APP/.config/APP/   # the files you want backed up
rmdir ~/.config/APP                              # only if it is now empty

# 2. link it back
cd dotfiles
stow -v -t "$HOME" APP

# 3. verify, then commit
ls -l ~/.config/APP
cd .. && git add dotfiles/APP && git commit -m "stow APP"
```

For loose files in `~/.config` itself (no subdirectory), drop the `APP` layer: `~/.config/futu.d/conf.toml` → `dotfiles/futu/.config/futu.d/conf.toml`.

**Q: After a config is stowed, how do I edit it?**

**A:** Edit through the symlink as usual — `~/.config/APP/config` is the repo file. `git status` shows the change; commit to back it up, `git checkout -- dotfiles/APP` to restore.

**Q: Why is `-t "$HOME"` mandatory here and never `-t ~/.config`?**

**A:** With `dotfiles/<package>` layouts, the package's `.config` maps onto `~/.config` only when the target is `$HOME`. Passing `-t ~/.config` nests a second `.config` inside `.config` (`~/.config/.config/...`) — that was the bug that once left kitty and xkb linked in the wrong tree with `~/.config/kitty` dangling.

**Q: I don't want `*.bak` backups linked or committed. Fix it once?**

**A:** Yes — create `dotfiles/.stow-local-ignores` (one file covers every package) containing:

```
\.bak
\.bak\d+
```

It is honored because it lives at the stow dir root. (Stow's default ignore list never matches `foo.conf.bak`, so without this the backups flow through.)

**Q: In the past, big real directories confused stow with "existing target is not owned by stow". What does that mean?**

**A:** The path in `~/.config` is a real file/dir instead of a stow symlink. Don't force it: move it into the package like in the new-app recipe, then stow again. Stow replaces an empty/absent path with a symlink with no complaint.

**Q: Which files should NOT be stowed?**

**A:** Caches, regenerable state, and files a tool rewrites wholesale (`settings.json` files, icon dirs, session state) — they turn into permanent `git status` noise. For a big directory where you want half the contents, copy it into the package and delete the unwanted parts before stowing; stow links whatever the package ends up containing.

**Q: New machine or reinstall — how do I recover everything at once?**

**A:**

```bash
git clone <repo-url> /home/atg/Programs/configuration
cd /home/atg/Programs/configuration/dotfiles
stow -v -t "$HOME" nvim zsh kitty xkb APP ...   # name the packages you want
```

Name the packages explicitly (or `stow -t "$HOME" */` works only when the stow dir has no extra non-package entries — README.md is ignored by default, but check before globbing).

**Q: Existing packages in this repo for reference:**

**A:** `kitty`, `xkb`, `nvim`, `zsh`, `mango`, `kanshi`, `danksearch`, `DankMaterialShell`, `Code`, `opencode` — each stowed with `stow -v -t "$HOME" <name>` from `dotfiles/`.
