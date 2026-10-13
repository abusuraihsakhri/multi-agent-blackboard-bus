import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { evaluateTask } from "../web/app.mjs";

const sample = { task_id: "T1", target_identifier: "KEY", primary_metric: 10,
  secondary_metric: 4, status_descriptor: "NOMINAL", is_critical_flag: false };

test("routine outcome has no alerts", () => {
  const result = evaluateTask(sample);
  assert.equal(result.overall_urgency, "ROUTINE");
  assert.equal(result.total_alerts, 0);
});
test("primary threshold and descriptor warnings", () => {
  const result = evaluateTask({ ...sample, primary_metric: 26, status_descriptor: "DISCORDANT" });
  assert.equal(result.total_alerts, 2);
  assert.equal(result.overall_urgency, "ELEVATED_RISK");
});
test("strict 25 / 12 thresholds", () => {
  assert.equal(evaluateTask({ ...sample, primary_metric: 25, secondary_metric: 12 }).total_alerts, 0);
  assert.equal(evaluateTask({ ...sample, secondary_metric: 12.01 }).total_alerts, 1);
});
test("critical flag escalates regardless of measurements", () => {
  const result = evaluateTask({ ...sample, is_critical_flag: true });
  assert.equal(result.overall_urgency, "CRITICAL_STAT_PANIC");
  assert.equal(result.critical_alerts_count, 1);
});
test("rejects invalid inputs", () => {
  assert.throws(() => evaluateTask({ ...sample, primary_metric: Infinity }), /finite/);
  assert.throws(() => evaluateTask({ ...sample, task_id: "" }), /required/);
});

test("HTML module script parses without JavaScript syntax errors", () => {
  const html = readFileSync(resolve(dirname(fileURLToPath(import.meta.url)), "../web/index.html"), "utf8");
  const tag = '<script type="module">';
  const start = html.indexOf(tag);
  const end = html.indexOf("</script>", start);
  assert.ok(start !== -1 && end > start, "expected an inline JavaScript module");
  const syntax = spawnSync(process.execPath, ["--input-type=module", "--check"],
    { input: html.slice(start + tag.length, end), encoding: "utf8" });
  assert.equal(syntax.status, 0, syntax.stderr);
});
