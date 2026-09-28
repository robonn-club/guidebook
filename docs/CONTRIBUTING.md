# Contributing to the Mobile Robotics Guidebook

This guidebook is maintained by [Robonn](https://robonn.de) — the Robotics Club at Universität Bonn — and is open to contributions from anyone, inside or outside the university.

---

## What We're Building

A curated map of the best learning resources in mobile robotics. For each topic we list what you need to know, then point to the single best video, book chapter, or paper for learning it — with a working link and an honest sentence on why that resource and not another.

We are not rewriting Probabilistic Robotics. The value here is *curation*: someone has already read the six candidate resources and tells you which one to spend your evening on.

---

## How to Contribute

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/guidebook.git
cd guidebook
```

### 2. Pick a topic

Check open issues for `help wanted` or `good first contribution` labels, or open a new issue to propose something before starting large additions.

### 3. Write

- Work inside the relevant course folder under `docs/courses/`.
- Every resource you add **must be a working link**. An entry without a URL is not useful
  to a reader — it just makes them go and search for it themselves.
- Point to the exact location: chapter and page range for a book, the specific lecture for
  a series. "See Probabilistic Robotics" is not a pointer; "Probabilistic Robotics, Ch. 3,
  pp. 40–81" is.
- Add one sentence saying what that resource gives you that the others don't. This is the
  part a search engine cannot do, and it is the reason this guidebook exists.
- Prefer the author's or publisher's own copy. Never link pirated PDFs.
- Use `docs/courses/TEMPLATE.md` as a starting point for new course pages.
- **If you study MoRo at Bonn, you can contribute something nobody else can.** The
  *At Bonn* boxes state what the module manual says; they cannot say what an exam is
  actually like, what caught people out, or which listed resource was worth the time.
  If you have sat a module,
  [write that up](https://github.com/robonn-club/guidebook/issues/new?template=exam-experience.yml) —
  it is the most valuable page-edit available on this project.

### 4. Preview locally

```bash
pip install -r requirements.txt
mkdocs serve
# → http://127.0.0.1:8000

# Before opening a PR, run the same check CI runs:
mkdocs build --strict
```

If you changed anything in `examples/`, also run the tests:

```bash
pip install -r examples/requirements.txt pytest
pytest tests
```

### 5. Open a pull request

- One topic or fix per PR — keep scope tight.
- Title the PR clearly: `Add EKF localization example` not `updates`.
- Describe what you added and why it belongs here.

---

## Content Standards

| Do | Avoid |
|---|---|
| Link every resource you name, with a canonical URL | Naming a book, video, or paper with no link |
| Give the exact chapter, page range, or lecture number | "Further reading: Thrun et al." with no location |
| Say in one sentence why *this* resource over the alternatives | Restating what a Wikipedia article already says |
| Link the author's or publisher's own copy, or a DOI / arXiv page | Pirated PDFs, mirrors, and re-uploads |
| Fix links you find broken or moved | Large reformats without content improvement |
| Keep *At Bonn* facts traceable to the module manual | Stating exam details from memory |

---

## Lessons with Runnable Code

The [Start Here](start-here/index.md) lessons show how to pair a page with code that is guaranteed to run:

- **Code lives in `examples/`**, one short NumPy-only file per lesson, runnable with `python examples/<name>.py`.
- **Pages embed the real file**, not a copy. Mark a region in the Python file with
  `# --8<-- [start:name]` and `# --8<-- [end:name]`, then include it in Markdown with
  `--8<-- "file.py:name"` inside a code fence. The strict build fails if the file or section is missing.
- **Numbers quoted on a page are tested.** `tests/test_lesson_pages.py` runs each example and checks
  that every line of the page's ```` ```text ```` output blocks still appears in the real output; other
  tests check the hand-worked examples and the statistics quoted in the text. Results of exercises
  that require changing the code ("What we saw" boxes) are hand-run experiments: re-run them when
  you change the example they modify.
- **Figures are generated**, never hand-edited: `pip install matplotlib && python scripts/make_figures.py`
  writes light and dark SVGs to `docs/start-here/assets/`. Show them with
  `![alt](assets/name-light.svg#only-light)` and `![alt](assets/name-dark.svg#only-dark)`.
- **Every source is checked.** Link to the actual video, paper (DOI) or chapter; do not cite from memory.

---

## Folder Conventions

```
courses/<n>_topic_name/
└── README.md          # the whole topic: what to learn, and where to learn it
```

One `README.md` per course, with three sections in this order:

| Section | What goes in it |
|---|---|
| `## Topics` | What this subject actually covers, as nested bullets. The syllabus. |
| `## Videos` | Lectures and talks — linked, in the order you should watch them. |
| `## Book / Article Resources` | Books, papers, and documentation — linked, with chapter or page pointers. |

GitHub renders `README.md` automatically, and MkDocs maps it to the folder's URL — so it is
the entry point in both places.

---

## Links

- Club home: [robonn.de](https://robonn.de)
- Course overview: [Courses](courses/README.md)

---

## Recognition

Everyone who contributes shows up in the **[Contributors](https://github.com/robonn-club/guidebook#contributors)**
image in the README — your avatar, linked to your GitHub profile. It updates
automatically from the commit history, so once your pull request is merged you'll
appear there. You don't need to write a whole chapter — correcting one mistake counts.

## License

By contributing, you agree that your contributions will be licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
