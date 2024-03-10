# Ulauncher Vercel

> [ulauncher](https://ulauncher.io/) Extension to easy access your [Vercel](https://vercel.com) projects.

## Requirements

* [ulauncher 5](https://ulauncher.io/)
* Python >= 3
* [Vercel](https://vercel.com) account.

## Install

First install project dependencies:

```make deps```

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```https://github.com/FrancocDev/ulauncher-vercel```

## Usage

* Before usage you need to configure your Vercel "token" in plugin preferences. You can get your Token [here](https://vercel.com/account/tokens).
* Set your username/team slug on the configuration field. 
* Then, on the Ulauncher bar, type "vc" to see your sites. The results are cached by 1h.
* Tapping "enter" on a result will open the respective site while "Alt+Enter" will open the project dashboard.

## Notes
Due to the way the Vercel project API works, it is very slow to verify in each project the url to access the panel, so the plugin only works with the specified personal account and only one computer (those specified in configurations).


## Development

```
make link
```

To see your changes, stop ulauncher and run it from the command line with: ```ulauncher -v```.


## Contributing

Contributions, issues and Features requests are welcome.
