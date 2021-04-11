# pyac3airborne_book

This bo the data from the AC3 related airborne campaigns

## Usage

### Building the book

If you'd like to develop on and build the pyac3airborne_book book, you should:

- Clone this repository and run
- Run `pip install -r requirements.txt` (it is recommended you do this within a virtual environment)
- (Recommended) Remove the existing `pyac3airborne_book/_build/` directory
- Run `jupyter-book build pyac3airborne_book/`

A fully-rendered HTML version of the book will be built in `pyac3airborne-book/_build/html/`.

Now you need to add it to git, commit is and push it back.

- `git add .`
- `git commit -m "describe your work"`
- `git push`
 
### Hosting the book

The html version of the book is hosted on the `gh-pages` branch of this repo.

- Navigating to your local build; and running,
- `ghp-import -n -p -f pyac3airborne_book/_build/html`

This will automatically push your build to the `gh-pages` branch. More information on this hosting process can be found [here](https://jupyterbook.org/publish/gh-pages.html#manually-host-your-book-with-github-pages).

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/mariomech/pyac3airborne_book/graphs/contributors).

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
