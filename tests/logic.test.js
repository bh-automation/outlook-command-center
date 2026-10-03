"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const L = require("../site/logic.js");

test("Statusliste ist fix und hat 5 Einträge", () => {
  assert.deepEqual(L.STATUS, ["ACTION", "WAITING", "PROJECT", "DONE", "REFERENCE"]);
});

test("Setzen auf leerer Nachricht: nur hinzufügen", () => {
  assert.deepEqual(L.plan([], "ACTION"), { add: ["ACTION"], remove: [], result: "set" });
  assert.deepEqual(L.plan(null, "DONE"), { add: ["DONE"], remove: [], result: "set" });
});

test("WAITING ersetzt ACTION, fremde Kategorien bleiben", () => {
  const cur = [{ displayName: "ACTION", color: "Preset0" }, { displayName: "CAREER", color: "Preset8" }];
  assert.deepEqual(L.plan(cur, "WAITING"), { add: ["WAITING"], remove: ["ACTION"], result: "set" });
});

test("Erneuter Klick entfernt nur diesen Status", () => {
  assert.deepEqual(L.plan(["PROJECT", "FINANCE"], "PROJECT"), { add: [], remove: ["PROJECT"], result: "cleared" });
});

test("Mehrere alte Status werden bereinigt", () => {
  const p = L.plan(["ACTION", "WAITING", "PRIVATE"], "DONE");
  assert.deepEqual(p.add, ["DONE"]);
  assert.deepEqual(p.remove.sort(), ["ACTION", "WAITING"]);
});

test("Groß-/Kleinschreibung wird toleriert", () => {
  assert.deepEqual(L.plan(["action"], "ACTION"), { add: [], remove: ["action"], result: "cleared" });
  assert.equal(L.activeStatus(["reference"]), "REFERENCE");
});

test("Unbekannter Status wird abgelehnt", () => {
  assert.throws(() => L.plan([], "DELETE"));
});

test("activeStatus nimmt die erste Status-Kategorie in fester Reihenfolge", () => {
  assert.equal(L.activeStatus(["CAREER"]), null);
  assert.equal(L.activeStatus(["DONE", "ACTION"]), "ACTION");
});
