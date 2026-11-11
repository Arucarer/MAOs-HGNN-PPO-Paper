# Reorder Methodology Figures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep both methodology figures in Chapter 4, with the attention mechanism first and the temporal graph representation second.

**Architecture:** Edit only the figure blocks and nearby narrative in `sections/04_methodology.tex`. Use `[H]` placement so the figures remain beside the relevant Chapter 4 text.

**Tech Stack:** LaTeX, latexmk, pdfLaTeX.

## Global Constraints

- Preserve the existing labels and image files.
- Number the attention-mechanism image before the temporal-graph image.

---

### Task 1: Reorder and anchor the Chapter 4 figures

**Files:**
- Modify: `sections/04_methodology.tex`

**Interfaces:**
- Consumes: `fig:attention_hgnn`, `fig:temporal_graph`, and their existing PNG files
- Produces: fixed-position Chapter 4 figures in the requested order

- [ ] **Step 1: Verify the current build/order**

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`; expect a successful build with `[t]` figures free to drift.

- [ ] **Step 2: Apply the minimal layout change**

Move `fig:temporal_graph` after `fig:attention_hgnn`, set both to `[H]`, and add nearby figure references.

- [ ] **Step 3: Compile and verify**

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`; expect exit code 0 and updated `build/main.pdf`.

