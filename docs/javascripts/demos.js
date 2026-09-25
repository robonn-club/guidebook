/* Interactive demos for the Start Here lessons.
 *
 * <div class="bayes-demo"></div>  - Lesson 1: the hallway Bayes filter
 * <div class="gauss-demo"></div>  - Lesson 2: fusing two Gaussians
 *
 * The models match examples/bayes_filter_1d.py and examples/kalman_filter_1d.py.
 */
(function () {
  "use strict";

  var SVG = "http://www.w3.org/2000/svg";

  function el(tag, attrs, parent) {
    var node = tag.indexOf("svg:") === 0
      ? document.createElementNS(SVG, tag.slice(4))
      : document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    if (parent) parent.appendChild(node);
    return node;
  }

  function pct(p) { return Math.round(p * 100) + "%"; }

  function demoWidth(root) {
    var style = getComputedStyle(root);
    var inner = root.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
    return Math.round(Math.max(280, Math.min(640, inner || 640)));
  }

  /* ---------------------------------------------------------------- Lesson 1 */

  var HALLWAY = [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0];

  function initBayes(root) {
    var n = HALLWAY.length;
    var state = {};

    root.innerHTML = "";
    var controls = el("div", { class: "demo-controls" }, root);
    var senseBtn = el("button", { type: "button", class: "md-button md-button--primary", text: "Sense" }, controls);
    var moveBtn = el("button", { type: "button", class: "md-button md-button--primary", text: "Move 1 cell →" }, controls);
    var resetBtn = el("button", { type: "button", class: "md-button", text: "Reset" }, controls);
    var peekLabel = el("label", { class: "demo-check" }, controls);
    var peek = el("input", { type: "checkbox" }, peekLabel);
    peekLabel.appendChild(document.createTextNode(" Show where the robot really is"));

    var sliders = el("div", { class: "demo-sliders" }, root);
    var acc = slider(sliders, "Sensor is right", 55, 99, 90, "%");
    var slip = slider(sliders, "Wheels slip (each way)", 0, 20, 5, "%");

    // Lay out at the real container width so text stays readable on phones.
    var w = demoWidth(root), h = 250, top = 12, barBottom = 170, left = 44;
    var cw = (w - left - 4) / n;
    var labelEvery = cw >= 18 ? 1 : 5;
    var svg = el("svg:svg", { viewBox: "0 0 " + w + " " + h, class: "demo-svg", role: "img",
      "aria-label": "Belief over the 20 hallway cells" }, root);
    [0, 0.25, 0.5, 0.75, 1].forEach(function (p) {
      var y = barBottom - p * (barBottom - top);
      el("svg:line", { x1: left, x2: w - 4, y1: y, y2: y, class: "demo-grid" }, svg);
      el("svg:text", { x: left - 6, y: y + 4, class: "demo-tick", "text-anchor": "end", text: pct(p) }, svg);
    });
    var bars = [], doors = [];
    for (var i = 0; i < n; i++) {
      var x = left + i * cw;
      bars.push(el("svg:rect", { x: x + 3, width: cw - 6, rx: 3, class: "demo-bar" }, svg));
      doors.push(el("svg:rect", { x: x + 4, y: barBottom + 8, width: cw - 8, height: 22, rx: 2,
        class: HALLWAY[i] ? "demo-door" : "demo-wall" }, svg));
      if (i % labelEvery === 0) {
        el("svg:text", { x: x + cw / 2, y: barBottom + 46, class: "demo-tick", "text-anchor": "middle", text: i }, svg);
      }
    }
    var robot = el("svg:text", { y: barBottom + 68, class: "demo-robot", "text-anchor": "middle", text: "▲ robot" }, svg);

    var status = el("p", { class: "demo-status", "aria-live": "polite" }, root);
    var legend = el("p", { class: "demo-legend" }, root);
    legend.innerHTML = '<span class="demo-key demo-door"></span> door &nbsp; ' +
      '<span class="demo-key demo-wall"></span> wall &nbsp; bars: the robot\'s belief p(cell)';

    function slider(parent, label, min, max, value, unit) {
      var wrap = el("label", { class: "demo-slider" }, parent);
      var text = el("span", { text: label + ": " + value + unit }, wrap);
      var input = el("input", { type: "range", min: min, max: max, value: value }, wrap);
      input.addEventListener("input", function () { text.textContent = label + ": " + input.value + unit; });
      return input;
    }

    function kernel() {
      var s = slip.value / 100;
      return [s, 1 - 2 * s, s];
    }

    function reset() {
      state.truth = Math.floor(Math.random() * n);
      state.belief = HALLWAY.map(function () { return 1 / n; });
      state.steps = 0;
      render("The robot has just been switched on somewhere in the hallway. " +
        "Every cell is equally likely (" + pct(1 / n) + " each).");
    }

    function sense() {
      var p = acc.value / 100;
      var z = Math.random() < p ? HALLWAY[state.truth] : 1 - HALLWAY[state.truth];
      var post = state.belief.map(function (b, i) { return b * (HALLWAY[i] === z ? p : 1 - p); });
      var total = post.reduce(function (a, b) { return a + b; }, 0);
      state.belief = post.map(function (b) { return b / total; });
      state.steps++;
      render("Sensed a " + (z ? "door" : "wall") + ". Cells that match got multiplied by " +
        p.toFixed(2) + ", the others by " + (1 - p).toFixed(2) + ", then everything was rescaled to sum to 100%.");
    }

    function move() {
      var k = kernel(), r = Math.random(), moved = r < k[0] ? 0 : r < k[0] + k[1] ? 1 : 2;
      state.truth = (state.truth + moved) % n;
      var prior = state.belief.map(function () { return 0; });
      for (var i = 0; i < n; i++) {
        for (var m = 0; m < 3; m++) prior[(i + m) % n] += k[m] * state.belief[i];
      }
      state.belief = prior;
      state.steps++;
      render("Moved. Every bar shifted one cell right, and a little of each leaked into its neighbours " +
        "because the wheels may have slipped. Moving never makes the robot more certain.");
    }

    function render(message) {
      var best = 0;
      state.belief.forEach(function (b, i) {
        var y = barBottom - b * (barBottom - top);
        bars[i].setAttribute("y", y);
        bars[i].setAttribute("height", Math.max(barBottom - y, 0.5));
        if (b > state.belief[best]) best = i;
      });
      bars.forEach(function (bar, i) { bar.classList.toggle("demo-bar--best", i === best); });
      robot.setAttribute("x", left + (state.truth + 0.5) * cw);
      robot.style.display = peek.checked ? "" : "none";
      var guess = "Most likely cell: " + best + " (" + pct(state.belief[best]) + ").";
      if (peek.checked) guess += state.truth === best ? " That's right." : " The robot is really in cell " + state.truth + ".";
      status.textContent = message + " " + guess;
    }

    senseBtn.addEventListener("click", sense);
    moveBtn.addEventListener("click", move);
    resetBtn.addEventListener("click", reset);
    peek.addEventListener("change", function () { render(status.textContent.split(" Most likely")[0]); });
    reset();
  }

  /* ---------------------------------------------------------------- Lesson 2 */

  function initGauss(root) {
    root.innerHTML = "";
    var sliders = el("div", { class: "demo-sliders" }, root);
    var mu = slider("Prediction mean μ̄", 0, 20, 8, 0.1, " m");
    var sp = slider("Prediction std σ̄", 0.2, 4, 1.5, 0.1, " m");
    var z = slider("GPS reading z", 0, 20, 12, 0.1, " m");
    var sz = slider("GPS std σ_z", 0.2, 4, 1, 0.1, " m");

    var w = demoWidth(root), h = 220, top = 10, bottom = 180, left = 14, right = w - 14;
    var svg = el("svg:svg", { viewBox: "0 0 " + w + " " + h, class: "demo-svg", role: "img",
      "aria-label": "Prediction, measurement and fused Gaussian" }, root);
    for (var t = 0; t <= 20; t += w >= 480 ? 2 : 5) {
      var x = left + (t / 20) * (right - left);
      el("svg:line", { x1: x, x2: x, y1: top, y2: bottom, class: "demo-grid" }, svg);
      el("svg:text", { x: x, y: bottom + 16, class: "demo-tick", "text-anchor": "middle", text: t + " m" }, svg);
    }
    var fill = el("svg:path", { class: "demo-post-fill" }, svg);
    var pred = el("svg:path", { class: "demo-pred" }, svg);
    var meas = el("svg:path", { class: "demo-meas" }, svg);
    var post = el("svg:path", { class: "demo-post" }, svg);
    var legend = el("p", { class: "demo-legend" }, root);
    legend.innerHTML = '<span class="demo-line demo-pred"></span> prediction &nbsp; ' +
      '<span class="demo-line demo-meas"></span> measurement &nbsp; ' +
      '<span class="demo-line demo-post"></span> fused estimate';
    var out = el("p", { class: "demo-status", "aria-live": "polite" }, root);

    function slider(label, min, max, value, step, unit) {
      var wrap = el("label", { class: "demo-slider" }, sliders);
      var text = el("span", {}, wrap);
      // step must be set before value, or the browser snaps value to the default step of 1
      var input = el("input", { type: "range", min: min, max: max, step: step, value: value }, wrap);
      function show() { text.textContent = label + ": " + (+input.value).toFixed(1) + unit; }
      input.addEventListener("input", function () { show(); draw(); });
      show();
      return input;
    }

    function curve(m, s, peak) {
      var d = "";
      for (var i = 0; i <= 200; i++) {
        var xv = (i / 200) * 20;
        var y = Math.exp(-0.5 * Math.pow((xv - m) / s, 2)) / s;
        var px = left + (xv / 20) * (right - left);
        var py = bottom - (y / peak) * (bottom - top);
        d += (i ? "L" : "M") + px.toFixed(1) + " " + py.toFixed(1);
      }
      return d;
    }

    function draw() {
      var m1 = +mu.value, s1 = +sp.value, m2 = +z.value, s2 = +sz.value;
      var K = s1 * s1 / (s1 * s1 + s2 * s2);
      var m = m1 + K * (m2 - m1), s = Math.sqrt((1 - K) * s1 * s1);
      var peak = 1 / Math.min(s1, s2, s);
      pred.setAttribute("d", curve(m1, s1, peak));
      meas.setAttribute("d", curve(m2, s2, peak));
      var d = curve(m, s, peak);
      post.setAttribute("d", d);
      fill.setAttribute("d", d + "L" + right + " " + bottom + "L" + left + " " + bottom + "Z");
      out.textContent = "Kalman gain K = σ̄² / (σ̄² + σ_z²) = " + K.toFixed(2) +
        ". Fused estimate: " + m.toFixed(2) + " m ± " + s.toFixed(2) + " m, " +
        "which is " + (K > 0.5 ? "closer to the measurement" : K < 0.5 ? "closer to the prediction" : "halfway between them") +
        " and narrower than either input.";
    }
    draw();
  }

  function initAll() {
    document.querySelectorAll(".bayes-demo:not([data-ready])").forEach(function (r) {
      r.setAttribute("data-ready", ""); initBayes(r);
    });
    document.querySelectorAll(".gauss-demo:not([data-ready])").forEach(function (r) {
      r.setAttribute("data-ready", ""); initGauss(r);
    });
  }

  // Material's instant navigation swaps pages without a full reload.
  if (typeof document$ !== "undefined") document$.subscribe(initAll);
  else document.addEventListener("DOMContentLoaded", initAll);
})();
