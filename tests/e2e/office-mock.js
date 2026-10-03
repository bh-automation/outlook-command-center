/* Office.js-Attrappe NUR für lokale Tests (wird nicht veröffentlicht). Fiktive Beispieldaten. */
(function () {
  var cfg = window.__PW_MOCK__ || {};
  var master = cfg.master || ["ACTION", "WAITING", "PROJECT", "DONE", "REFERENCE", "CAREER", "FINANCE", "PRIVATE"];
  var maxMinor = cfg.maxMinor || 14; /* Mailbox 1.14 */
  window.__calls = [];
  var delay = cfg.delay || 5;
  var delays = cfg.delays || {}; /* Verzögerung je Betreff (für Wettlauf-Tests) */
  function makeItem(subject, fromName, initial) {
    var cats = initial.map(function (n) { return { displayName: n, color: "Preset0" }; });
    var item = {
      subject: subject,
      from: { displayName: fromName, emailAddress: "test@example.invalid" },
      __cats: function () { return cats.map(function (c) { return c.displayName; }); },
      categories: {
        getAsync: function (cb) { window.__calls.push(["get", subject]); setTimeout(function () { cb({ status: "succeeded", value: cats.slice() }); }, delays[subject] || delay); },
        addAsync: function (list, cb) {
          window.__calls.push(["add", list.slice(), subject]);
          if (list.some(function (x) { return master.indexOf(x) === -1; })) {
            setTimeout(function () { cb({ status: "failed", error: { name: "InvalidCategory", message: "Invalid categories were provided." } }); }, delay);
            return;
          }
          list.forEach(function (x) { if (!cats.some(function (c) { return c.displayName === x; })) cats.push({ displayName: x, color: "Preset0" }); });
          setTimeout(function () { cb({ status: "succeeded" }); }, delay);
        },
        removeAsync: function (list, cb) {
          window.__calls.push(["remove", list.slice(), subject]);
          cats = cats.filter(function (c) { return list.indexOf(c.displayName) === -1; });
          setTimeout(function () { cb({ status: "succeeded" }); }, delay);
        }
      }
    };
    return item;
  }
  var first = makeItem("Angebot Wartungsvertrag – Rückmeldung bis Freitag", "Muster, Max", cfg.initial || ["CAREER"]);
  window.__items = [first];
  /* Simuliert Nachrichtenwechsel im angehefteten Bereich (null = keine Auswahl). */
  window.__switchItem = function (subject, fromName, initial) {
    var it = subject === null ? null : makeItem(subject, fromName, initial || []);
    if (it) window.__items.push(it);
    window.Office.context.mailbox.item = it;
    if (window.__itemChanged) window.__itemChanged({ type: "olkItemSelectedChanged" });
  };
  window.Office = {
    HostType: { Outlook: "Outlook" },
    AsyncResultStatus: { Succeeded: "succeeded", Failed: "failed" },
    EventType: { ItemChanged: "olkItemSelectedChanged" },
    onReady: function (cb) { setTimeout(function () { cb({ host: "Outlook" }); }, 0); },
    context: {
      requirements: { isSetSupported: function (n, v) { return n === "Mailbox" && parseInt(String(v).split(".")[1] || "0", 10) <= maxMinor; } },
      mailbox: {
        addHandlerAsync: function (t, h, cb) { window.__itemChanged = h; cb && cb({ status: "succeeded" }); },
        item: first
      }
    }
  };
})();
