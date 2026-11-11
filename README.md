# HGNN-PPO SCI Paper Framework

This is a modular Elsevier-style LaTeX scaffold for an HGNN + PPO paper. It contains structure and writing prompts, not manuscript claims or fabricated results.

## Folder layout

The project has five content folders:

1. `sections/` — front matter, seven main sections, and back matter.
2. `figures/` — framework diagrams, graph schemas, plots, and scheduling visualizations.
3. `tables/` — large reusable tables kept outside section files.
4. `references/` — the BibTeX database.
5. `styles/` — shared notation and custom LaTeX commands.

The root also contains `main.tex` (the only compilation entry), `latexmkrc`, this guide, and `.gitignore`.

## Recommended writing order

1. Fix the problem definition, assumptions, notation, objectives, and MDP in Section 3.
2. Specify the graph schema, HGNN encoder, PPO policy, and training algorithm in Section 4.
3. Design experiments, baselines, metrics, ablations, seeds, and statistical tests in Section 5.
4. Write the literature review around the exact gap established by Sections 3--5.
5. Write the introduction, discussion, and conclusions after the evidence is stable.
6. Write the title and abstract last.

## Compile

The manuscript uses the Elsevier `elsarticle` 5p two-column layout. Document-class settings belong in `main.tex`; they are not PowerShell commands. Wide figures, tables, and algorithms use starred float environments.

English body text uses Times New Roman at 10 pt with single spacing, with coordinated NewTX mathematics. Display equations are left aligned; related calculations share a numbered equation group. The `ctex` package uses `scheme=plain` to preserve the English template's font sizes and spacing; Times New Roman and the MiKTeX `newtx` package must be installed when compiling with XeLaTeX.

With a current TeX Live or MiKTeX installation:

```powershell
latexmk -interaction=nonstopmode -halt-on-error main.tex
```

The project configuration selects XeLaTeX to support Chinese text and UTF-8 image filenames. The output is `build/main.pdf`. Select XeLaTeX in your editor as well; do not override this with `latexmk -pdf` (pdfLaTeX).

Manual fallback (output in the project root):

```powershell
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

Run commands from this folder. If `elsarticle.cls` is missing, install the `elsarticle` package through your TeX distribution.

## Before submission

- Replace all square-bracket prompts and comment prompts with verified content.
- Verify every citation against the original source.
- Replace the journal, author, affiliation, and declaration placeholders.
- Check the target journal's current author guide and required document options.
- Confirm that all numerical claims can be traced to reproducible experiments.
