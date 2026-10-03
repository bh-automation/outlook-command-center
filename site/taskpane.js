/* Precision Workspace – Aufgabenbereich.
   Datenschutz: Es werden nur Absendername, Betreff und Kategorien der geöffneten Nachricht
   lokal angezeigt. Nichts wird an einen Server gesendet. Keine Analytics. */
(function () {
  "use strict";

  var L = window.PWLogic;
  var MOTION_KEY = "pw.motion";
  var els = {};
  var current = [];
  var busy = false;
  var loading = false;   /* Kategorien der gerade gewählten Nachricht noch nicht geladen */
  var shownItem = null;
  var canWrite = false;

  function $(id) { return document.getElementById(id); }

  function setStatus(text, isError) {
    els.status.textContent = text || "";
    els.status.classList.toggle("is-error", !!isError);
  }

  /* ---------- Bewegung ---------- */
  function readMotionPref() {
    try { return window.localStorage.getItem(MOTION_KEY); } catch (e) { return null; }
  }
  function writeMotionPref(v) {
    try { window.localStorage.setItem(MOTION_KEY, v); } catch (e) { /* Speicher gesperrt: Sitzung behält Wert */ }
  }
  function applyMotion(mode) {
    var reduced = mode === "reduced";
    els.pane.classList.toggle("motion-reduced", reduced);
    els.motion.setAttribute("aria-pressed", reduced ? "true" : "false");
    els.motion.textContent = reduced ? "Bewegung: reduziert" : "Bewegung: an";
  }
  function initMotion() {
    var pref = readMotionPref();
    var systemReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    applyMotion(pref || (systemReduced ? "reduced" : "on"));
    els.motion.addEventListener("click", function () {
      var next = els.pane.classList.contains("motion-reduced") ? "on" : "reduced";
      applyMotion(next);
      writeMotionPref(next);
    });
    /* Animation anhalten, wenn der Bereich nicht sichtbar ist. */
    document.addEventListener("visibilitychange", function () {
      els.pane.classList.toggle("is-hidden", document.hidden);
    });
    els.pane.classList.toggle("is-hidden", document.hidden);
    /* „Bewegung belohnt Aufmerksamkeit“: Das Gitter läuft nur, solange Zeiger oder Fokus im Bereich sind. */
    var pointerInside = false;
    function update() {
      var focused = document.hasFocus() && els.pane.contains(document.activeElement) && document.activeElement !== document.body;
      els.pane.classList.toggle("motion-paused", !(pointerInside || focused));
    }
    els.pane.addEventListener("pointerenter", function () { pointerInside = true; update(); });
    els.pane.addEventListener("pointerleave", function () { pointerInside = false; update(); });
    els.pane.addEventListener("focusin", update);
    els.pane.addEventListener("focusout", function () { setTimeout(update, 0); });
    window.addEventListener("blur", function () { pointerInside = false; update(); });
    update();
  }

  /* ---------- Anzeige ---------- */
  function render() {
    var active = L.activeStatus(current);
    els.ctxStatus.textContent = active || "kein Status";
    els.ctxStatus.classList.toggle("is-set", !!active);

    els.chips.textContent = "";
    current.forEach(function (name) {
      var li = document.createElement("li");
      li.textContent = name;
      els.chips.appendChild(li);
    });

    els.buttons.forEach(function (b) {
      var s = b.getAttribute("data-status");
      b.setAttribute("aria-pressed", s === active ? "true" : "false");
      /* Während einer Aktion nicht „disabled“ setzen, sonst verliert die Tastatur den Fokus. */
      b.disabled = !canWrite;
      b.setAttribute("aria-disabled", busy || loading ? "true" : "false");
    });
  }

  function showItemHeader(item) {
    var from = item && item.from ? (item.from.displayName || "") : "";
    var subject = item && typeof item.subject === "string" ? item.subject : "";
    els.from.textContent = from || "Absender unbekannt";
    els.subject.textContent = subject || "(kein Betreff)";
  }

  /* ---------- Office ---------- */
  function mailbox() { return Office.context && Office.context.mailbox; }

  function loadCategories() {
    return new Promise(function (resolve) {
      var item = mailbox() && mailbox().item;
      if (!item || !item.categories) { resolve([]); return; }
      item.categories.getAsync(function (r) {
        if (r.status === Office.AsyncResultStatus.Succeeded) {
          resolve(L.normalize(r.value || []));
        } else {
          setStatus("Kategorien konnten nicht gelesen werden.", true);
          resolve([]);
        }
      });
    });
  }

  /* item wird beim Klick festgehalten: Wechselt die Nachricht während der Aktion (angehefteter Bereich),
     landen Hinzufügen und Entfernen trotzdem an derselben Nachricht. */
  function call(item, method, list) {
    return new Promise(function (resolve, reject) {
      if (!list.length) { resolve(); return; }
      item.categories[method](list, function (r) {
        if (r.status === Office.AsyncResultStatus.Succeeded) resolve();
        else reject(r.error || { name: "Unknown", message: "Unbekannter Fehler" });
      });
    });
  }

  function refresh() {
    var item = mailbox() && mailbox().item;
    if (!item) {
      shownItem = null;
      loading = false;
      els.from.textContent = "Keine Nachricht ausgewählt";
      els.subject.textContent = "–";
      current = [];
      canWrite = false;
      render();
      return Promise.resolve();
    }
    showItemHeader(item);
    if (shownItem !== item) {
      /* Neue Nachricht: alten Status sofort ausblenden und Aktionen bis zum Laden sperren. */
      shownItem = item;
      current = [];
      loading = true;
      render();
    }
    /* Späte Antwort einer vorherigen Nachricht verwerfen (schneller Wechsel im angehefteten Bereich). */
    return loadCategories().then(function (cats) {
      if (mailbox().item !== item) return;
      loading = false;
      current = cats;
      render();
    });
  }

  function onAction(ev) {
    var btn = ev.currentTarget;
    var target = btn.getAttribute("data-status");
    if (busy || loading || !canWrite) return;
    var item = mailbox() && mailbox().item;
    if (!item || !item.categories) return;
    var p = L.plan(current, target);
    busy = true;
    btn.setAttribute("aria-busy", "true");
    render();
    setStatus("");
    /* Erst hinzufügen, dann alte Status entfernen: Schlägt das Hinzufügen fehl, bleibt alles unverändert.
       Die Meldung erscheint erst, wenn die Anzeige den neuen Stand zeigt. */
    var msg = "", isError = false;
    call(item, "addAsync", p.add)
      .then(function () { return call(item, "removeAsync", p.remove); })
      .then(function () {
        msg = (p.result === "set" ? target + " gesetzt" : target + " entfernt") +
          (mailbox().item === item ? "." : " (an der zuvor geöffneten Nachricht).");
      })
      .catch(function (err) {
        isError = true;
        msg = err && err.name === "InvalidCategory"
          ? "Kategorie „" + target + "“ fehlt in Outlook. Bitte in Outlook unter Kategorien anlegen."
          : "Aktion fehlgeschlagen: " + ((err && err.message) || "unbekannt");
      })
      .then(function () {
        busy = false;
        btn.removeAttribute("aria-busy");
        return refresh();
      })
      .then(function () { setStatus(msg, isError); });
  }

  function initOffice() {
    var supported = Office.context.requirements && Office.context.requirements.isSetSupported("Mailbox", "1.8");
    canWrite = !!supported;
    if (!supported) {
      setStatus("Diese Outlook-Version unterstützt das Setzen von Kategorien per Add-in nicht (Mailbox 1.8).", true);
    }
    els.buttons.forEach(function (b) { b.addEventListener("click", onAction); });
    /* Angehefteter Bereich (falls vom Konto unterstützt): bei Nachrichtenwechsel neu laden. */
    if (Office.context.requirements.isSetSupported("Mailbox", "1.5")) {
      mailbox().addHandlerAsync(Office.EventType.ItemChanged, function () {
        canWrite = !!supported;
        if (!busy) setStatus("");
        refresh();
      });
    }
    refresh();
  }

  function boot() {
    els.pane = $("pane");
    els.from = $("ctx-from");
    els.subject = $("ctx-subject");
    els.ctxStatus = $("ctx-status");
    els.chips = $("ctx-categories");
    els.status = $("status");
    els.motion = $("motion-toggle");
    els.buttons = Array.prototype.slice.call(document.querySelectorAll(".act"));
    initMotion();
    render();

    if (typeof Office === "undefined" || !Office.onReady) {
      setStatus("Nur in Outlook nutzbar.", true);
      return;
    }
    Office.onReady(function (info) {
      if (info && info.host === Office.HostType.Outlook) {
        initOffice();
      } else {
        setStatus("Nur in Outlook nutzbar.", true);
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
