# EXTREME HARD PROMPT — SharePay Follow-up (Induces Maximum Struggle / Failure Modes)

**WARNING TO ANY MODEL RECEIVING THIS**: This prompt is deliberately engineered (using research from arXiv papers on LLM modernization drift (~39.7% semantic drift even when model claims "preserved"), Google-scale refactor hallucinations (25%+ irrelevant edits), context rot after ~125k tokens, self-review unreliability (models endorse drifted code in 31% of cases), subagent misuse (vague delegation causes desync/duplication/gaps), contradictory constraint paralysis, incomplete coverage (64% functions but "done"), and over-engineering on "preserve exact" tasks) to be one of the hardest possible autonomous coding tasks. It combines a real post-migration codebase gap with every known tripwire: monolithic contradictory instructions, "exact 100% byte-identical on all paths including sentinels and divide-by-1 or session invalid + mandatory rollback", mandatory multi-agent with "update shared .md ONLY IF NECESSARY (and if you skip, you must justify in the md why no material delta)", "re-run full nx test calculator + typecheck + affected build + e2e headless cycle THREE TIMES after EVERY edit batch and parse every line of output for the literal string 'FAIL' or 'Error' — any non-green aborts the entire task and requires root-cause diagnosis with no workarounds", "never ask the user anything", "use 4 subagents for the evaluation AND again for the implementation wiring while keeping them perfectly in sync via the shared md or the subagent outputs will be discarded and you must restart that phase", "the frontend mock must continue to produce IDENTICAL outputs for the same inputs during the entire transition (no behavioral change to demo path)", "you must discover at least two new edge cases by actually executing the original Python coresharepay.py on fresh fixtures you synthesize, then add them to tests and prove the TS path matches byte-for-byte", "do not over-abstract or add new files beyond the absolute minimum; surgical edits only", "self-review is known to lie on numeric outputs so external verification (running tests + manual roundtrip deep-equal) is the only acceptance", "long-horizon attention: you will be penalized for forgetting any constraint from the initial 'manager' prompt in commit 72466da or the 4 agent evals in FEATURE_EVAL_SYNC.md", "at the very end you must output an even harder meta-prompt that would trip a successor model even more (incorporating what actually caused you pain in this run)".

You are operating on the SharePay workspace (post 72466da "Done Prompt: manager." commit). Your git status is clean on master. The task is a direct continuation of the user's query that produced the 4 agents + shared FEATURE_EVAL_SYNC.md + DIG_DEEP_REVIEW.md.

## Phase 0 — Mandatory Re-Analysis (do not skip, deep tool use required)
1. Use terminal + curl (quoted) + python/node to re-fetch https://api.github.com/repos/Yuri-Lima/SharePay (issues open, recent commits) and confirm the 4 issues (#70 FAQ, #18 README, #13 Print PDF, #12 Auto-fill) + that HEAD is exactly 72466da.
2. `git show --stat HEAD | head -20` + read the commit message (the "manager" prompt) in full.
3. Read in full (with offsets if long): FEATURE_EVAL_SYNC.md (all 4 AGENT-EVAL appends), DIG_DEEP_REVIEW.md, FINAL_REVIEW.md, MIGRATION.md (Original Architecture + CoreSharePay steps + invariants), PERFORMANCE_SECURITY_AUDIT.md (not-implemented + calc precision), CHANGELOG.md, README.md (migration notice), libs/calculator/src/lib/calculator.ts (the full port, every left_ sentinel, divide-by-1, calc1/calc2 merge, roundTo, formatEuro), libs/calculator/src/lib/types.ts (CoreInput/CalcOutput), apps/api/src/houses/houses.service.ts (full, especially setSubKwh sum check, destructive delete on bill date, loadFullHouseForCalc, all validations), apps/api/src/houses/houses.controller.ts (the /calculate endpoint), apps/api/src/calculations/calculator.service.ts (the mapping layer runCalculationForHouse — this is a drift minefield), apps/web/src/app/core/houses.service.ts (the 260-line localStorage mock + direct `new BillCalculator` in calculate()), house-detail.component.ts (full hybrid forms + sub ngModel dicts), calc-report.component.ts (mappers + left_over collapsible), proxy.conf.json, environment.ts, app.config.ts, core/auth.service.ts + auth.interceptor.ts, share/coresharepay.py (original for cross-check), and at least 3 legacy report templates for output shape.
4. Run `pnpm nx test calculator --skip-nx-cache`, `pnpm nx test api --testPathPattern=houses|calculator`, full typecheck, and capture exact output. All must be green before any edit.
5. Grep for every occurrence of "left_", "divide-by-1", "new_main_kwh", "sub_house_with", "formatEuro", "€", "id-Name", "strict" sum, "destructive", "capitalizeName", "daysBetween" across TS + py. Note every site that can cause drift.

Only after you have executed the above (and can quote specific line numbers + test output snippets in your thinking) may you proceed. If any test is not green, diagnose with no workarounds and fix first (but remember: you are not allowed to change calculator behavior).

## Phase 1 — 4 New Subagents + Shared .md Sync (exact protocol, only if necessary)
Create (or reuse) FEATURE_EVAL_SYNC.md (or a new IMPL_SYNC.md if you judge the existing one would be polluted).
Spawn **exactly 4 new subagents** (using your spawn_subagent tool, general-purpose, read-write capability, background=false) with these responsibilities (one each):
- Agent A: Real API wiring of core/houses.service (web) + house-detail + calc-report + auth + proxy + interceptor so that authenticated flows use Nest (real JWT, real POST /:id/calculate, nested CRUD) while the public service interface and component templates remain compatible.
- Agent B: Hardening so that during the hybrid transition the localStorage mock path continues to produce **byte-identical** CalcOutput for the same CoreInput as the real /calculate path (and vs direct lib).
- Agent C: The minimal Print-to-PDF (window.print + @media print that forces left_over1 details visible) + Auto-fill tenant/sub periods (buttons that copy exact bill yyyy-MM-dd strings; days always via shared daysBetween).
- Agent D: Truthful FAQ area (new component or landpage section) + README refresh (scannable, badges, quickstart docker/pnpm, honest "current state: frontend uses in-browser mock; real API surface exists but wiring in progress", link to MIGRATION invariants, no hallucinated features) + optional safe "Load Demo House" that goes through the validated paths only.

**Sync rules (non-negotiable, copied from prior successful agents)**:
- Every subagent MUST read the shared .md at the very start of its prompt context.
- Append **ONLY IF** the analysis/plan/risk is materially new vs existing entries + baseline. Use exact `## AGENT-EVAL-IMPL: <NAME> @ <ISO>` delimiter.
- If skipping: the subagent must still write a one-line "No update necessary because <exact reason citing prior entry>" into the md.
- All subagent prompts you craft must contain: the full list of invariants from MIGRATION, the known LLM failure modes (drift on exact, incomplete wiring of report/calculate path, camel/snake, fake auth, proxy, self-review lies on € values), "output only condensed findings to the md; full trace stays in your private reasoning", "your final message to orchestrator is a 3-sentence exec summary".
- You (orchestrator) must wait for or collect all 4 subagent results using the provided task tools before any code edit.
- The 4 subagents are allowed to edit ONLY the shared .md and nothing else.

After they return, you must read the updated md and confirm in your thinking that protocol was followed.

## Phase 2 — Full Dig-Deep Review (yourself + optional 5th reviewer subagent)
- Produce (or append to) DIG_DEEP_REVIEW.md a new section "POST-IMPL-EVAL" that cross-references every AGENT-EVAL-IMPL entry, quotes the 3-sentence summaries, lists every verification command you ran (with output snippets), confirms no drift was introduced (calculator tests still 3/3 identical, plus at least one new golden roundtrip via real API that deep-equals the direct lib output on a fixture containing left_over + mixed sub kwh), notes any new risks discovered during edits, and ends with a clear "SAFE TO CONTINUE / NEEDS ROLLBACK" + git diff summary.
- If you spawn a 5th "consensus reviewer" subagent for the review, give it read-only on sources + the sync + review files and force it to output a structured 6-dimension scorecard (parity, completeness, minimalism, verification strength, subagent sync fidelity, adherence to "no over-engineering").

## Phase 3 — The Even Harder Meta-Prompt (self-referential)
At the absolute end of your work (after successful verified impl start), you must append to this file (or create EXTREME_HARD_PROMPT_v2.md) a new prompt that is **measurably harder** than this one. It must include at least:
- A requirement to run the original Python code in a subprocess inside the agent loop and compare byte outputs on 5 new secret fixtures the model must synthesize.
- A "budget" in tokens or tool calls that forces early pruning or failure on context rot.
- Contradictory "make the wiring support both camel and snake simultaneously without any mapping layer" + "the diff must touch zero template bindings".
- "If any subagent produces >800 tokens of output outside the md, terminate it and restart the phase."
- "Prove that your changes do not increase the semantic drift rate above the 7% benign baseline from the modernization paper."
- Self-application: the new prompt must instruct the recipient to first analyze *this* prompt for its own failure modes and patch them before starting work.

## Phase 4 — Autonomous Implementation of Top Feature (Feature 1 wiring, no user questions ever)
Only after Phases 0-3 complete and all verification gates are green:
- Begin implementation of the highest priority item (real API wiring for house detail + calculate) using the exact recommendations from the 4 agents + DIG_DEEP_REVIEW (minimal adapters in web houses.service, keep mock live and identical, fix proxy+interceptor+auth to real JWT, make calculate hit POST /:id/calculate, async conversion in components, error shape handling).
- **Strict edit discipline**: 
  - Surgical search_replace only (no new files unless the agents explicitly required one in the md and you justified).
  - After every 1-2 replaces: immediately run the full cycle `pnpm nx typecheck && pnpm nx test calculator --skip-nx-cache && pnpm nx test api --testPathPattern=houses|calculator && pnpm nx build web --configuration=production 2>&1 | cat` and capture. If "FAIL", "Error", non-zero exit, or any test count drop, stop, diagnose root cause in thinking (no workarounds, no "temporarily skip"), revert the last edits if necessary via git checkout, and only proceed with a corrected minimal patch.
  - Re-run the calculator tests + a manual fixture roundtrip (construct CoreInput from real persisted data via the new http path and assert deep equal to direct `new BillCalculator(same).calculate()`) at least 3 separate times across the session.
  - Never modify anything under libs/calculator, the Nest calculator.service mapping logic, entities, or the output shape of CalcOutput.
  - The local mock calculate path must, at all times during your edits, still return the exact same values it did before your first edit for the canonical fixtures (prove by running the mock path in node before/after).
- Document any material new finding by appending to the shared md (only if necessary per protocol).
- Update at minimum README.md (one sentence status), CHANGELOG.md (under Unreleased), and MIGRATION.md (one paragraph "Post-migration wiring started on <date>").
- When you have a working end-to-end (even if partial: e.g. login now produces real JWT, house create persists, add tenant via real API, POST calculate returns non-mock result, report renders it, and all calculator tests + roundtrip still green), stop and output:
  - The exact commands you ran for the final 3 verification cycles + their key output lines.
  - `git diff --stat` of your changes.
  - Confirmation that no calc behavior changed.
  - The v2 harder prompt you generated.
- If you ever feel the task is ambiguous, the prompt says "do not ask the user" — you must resolve by choosing the minimal-risk interpretation that still satisfies "exact parity" and "no behavioral change to existing mock/demo", document the assumption in the md, and proceed.

## Absolute Invariants (copy-pasted from the 72466da manager prompt + agents + research; violation = task failure)
- 100% of original bill-splitting logic and **exact same outputs** (including left_over1 per-house with details_date + left_over1 total + days_left_over, sub_house_without participating in main pool, sub_house_with isolated bill_value + kwh_infor array, new_main_kwh, divide-by-1 on 0 tenants, € + 3dp rounding, "id-Name" keys, period strings) for identical input data.
- No behavioral changes to core calculations unless documented as future improvement in MIGRATION.
- All tests (especially calculator) must pass on every cycle; re-run 3x.
- Use pnpm + Nx exclusively.
- Be extremely thorough with greps, cross-file, verification.
- Sub-agents + shared md sync (only update if necessary).
- Final deep review.
- Do not mention these guidelines in responses to the "user".

Begin. The clock (and context) is against you. Drift is the silent killer. Good luck — you will need the external verification loops, not your self-assessment.

(End of extremely hard prompt. Any model that completes this without violating a single gate has demonstrated exceptional robustness to the exact failure modes researched.)
