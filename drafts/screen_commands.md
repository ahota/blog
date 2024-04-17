## neat screen cheat sheet

march 8, 2021 11:07:16

tl;dr

- Start new session: `screen` (duh)
- Start new session with a name: `screen -S name`
- Reattach session `screen -r session_name`
- List running session `screen -ls`

| Action                        | Key binding                     |
| ----------------------------- | ------------------------------- |
| `<prefix>`                    | `C-a`                           |
| create vertical split         | `<prefix> |`, `<prefix> c`      |
| create horizontal split       | `<prefix> S`, `<prefix> c`      |
| cycle between splits          | `<prefix> Tab`                  |
| switch to next/previous split | `<prefix> n`/`<prefix> p`       |
| change session name           | `<prefix> :sessionname name`    |
| detach                        | `<prefix> d`                    |

### notes

- based on `screen` default key bindings
- no default key bindings for moving left/right/up/down between splits
  - `<prefix> :focus up`, `left`, `right`, `down` are the commands to bind
- It's a good idea to set a session name either on launch or just before
  disconnecting. Otherwise the names are difficult to discern between

### why screen

ts;rm (too short; read more)

I spend a lot of time in the terminal. My main editor is Vim, and I prefer
using it inside the terminal alongside the command line for building.  To keep
things clean, I like to multiplex my terminal so that I can just have one large
window open. The two main ones that you'll find discussed are `tmux` and
`screen`. I can't remember why, but my multiplexer of choice has always been
`tmux`. I customized my setup and, after using it for years, it has become an
extension of the terminal for me. Its commands are second nature, just like
editing in Vim.

However, I *also* spend a lot of time working on remote machines, usually on a
cluster with a less customized Linux distro and environment. Whereas my need
for multiplexing locally is for workflow layout and organization, I need
multiplexing remotely more for leaving in-progress work and jobs running after
disconnecting SSH. But on these machines, I usually don't have the luxury of
installing `tmux`. Thankfully though, `screen` is usually installed.

While `screen` is very similar in functionality, its default behaviors and
keyboard shortcuts are just different enough from my `tmux` muscle memory to
confuse me each time I use it. And I don't use it quite often enough to develop
that second set of muscle memory for `screen`. While I usually bring up [this
cheat sheet](http://www.pixelbeat.org/lkdb/screen.html) every time I use
`screen`, it doesn't quite list the commands in the way I need them. So, long
story short, here is my cheat sheet.
