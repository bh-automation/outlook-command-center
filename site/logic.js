/* Precision Workspace – reine Logik ohne Office-Abhängigkeit (testbar in Node). */
(function (root) {
  "use strict";

  var STATUS = ["ACTION", "WAITING", "PROJECT", "DONE", "REFERENCE"];

  function normalize(list) {
    if (!Array.isArray(list)) return [];
    return list
      .map(function (c) { return typeof c === "string" ? c : (c && c.displayName) || ""; })
      .filter(function (n) { return n.length > 0; });
  }

  function isStatus(name) {
    return STATUS.indexOf(String(name).toUpperCase()) !== -1;
  }

  /* Ermittelt die nötigen Änderungen für einen Klick auf einen Status.
     - Status bereits gesetzt  → nur diesen Status entfernen (Umschalten).
     - Status nicht gesetzt    → Ziel hinzufügen, andere Status-Kategorien entfernen.
     Nicht-Status-Kategorien (z. B. CAREER, FINANCE) bleiben immer unangetastet. */
  function plan(currentCategories, target) {
    var t = String(target).toUpperCase();
    if (!isStatus(t)) throw new Error("Unbekannter Status: " + target);
    var current = normalize(currentCategories);
    var has = current.some(function (n) { return n.toUpperCase() === t; });
    if (has) {
      return {
        add: [],
        remove: current.filter(function (n) { return n.toUpperCase() === t; }),
        result: "cleared"
      };
    }
    return {
      add: [t],
      remove: current.filter(function (n) { return isStatus(n) && n.toUpperCase() !== t; }),
      result: "set"
    };
  }

  function activeStatus(currentCategories) {
    var current = normalize(currentCategories).map(function (n) { return n.toUpperCase(); });
    for (var i = 0; i < STATUS.length; i++) {
      if (current.indexOf(STATUS[i]) !== -1) return STATUS[i];
    }
    return null;
  }

  var api = { STATUS: STATUS, normalize: normalize, isStatus: isStatus, plan: plan, activeStatus: activeStatus };
  root.PWLogic = api;
  if (typeof module === "object" && module.exports) module.exports = api;
})(typeof self !== "undefined" ? self : globalThis);
