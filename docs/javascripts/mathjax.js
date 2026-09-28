window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// navigation.instant swaps page content without a reload, so MathJax has to be
// re-run on every navigation or equations vanish after the first page.
// clearFontCache is the SVG output's method; CHTML output calls it clearCache.
document$.subscribe(() => {
  MathJax.startup.output.clearFontCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
