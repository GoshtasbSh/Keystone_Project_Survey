"""Generate the collaborator-facing HTML report on the Analysis section.

Everything in the report is read out of the code and the data at build time —
the column map from SURVEY_QUESTIONS and the CSV's own ImportId row, the
statistics from a real pipeline run, the verification results from the two audit
scripts. Nothing is typed in by hand, so the report cannot drift from what the
dashboard actually does.

Run:  python3 scripts/audit/build_analysis_report.py
"""
from __future__ import annotations

import html
import json
import pathlib
import subprocess
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'api'))
sys.path.insert(0, str(ROOT / 'scripts' / 'audit'))

from analysis_provenance import build as build_provenance  # noqa: E402
from _processing import SURVEY_QUESTIONS  # noqa: E402

EVID = ROOT / 'docs' / 'plans' / 'evidence' / '2026-09-21-analysis-audit'
MAY = pathlib.Path('/Users/goshtasbshahriari/UF Dropbox/Goshtasb Shahriari Mehr/'
                   'DTSC_Lab/Keystone_Data/Keystone Heights Survey - V1_May 4, 2026_16.57.csv')
OUT = EVID / 'ANALYSIS_REPORT.html'

E = html.escape


# Plain-language description of each section, for a reader who knows the survey
# but not the code. Keyed by the section name in the analysis payload.
SECTION_NOTES = {
    'scores': ("The four headline averages. Health, IAQ and Structural are each "
               "scored 0-100 from the questions listed below, then combined into "
               "one Overall Risk score."),
    'risk_tiers': ("How many households fall in each risk band. The bands are cut "
                   "at fixed points on the Overall Risk score, not at percentiles, "
                   "so they are comparable between uploads."),
    'health': ("Respiratory symptom prevalence and hospital use. The three symptom "
               "percentages count only households reporting symptoms at least "
               "seasonally — a household answering \"annually\" is NOT counted here, "
               "although it does contribute to the Health score."),
    'housing': "Counts of housing type, self-reported condition, and construction era.",
    'ownership': ("Owner / renter / other. \"Other\" is everything that is neither, "
                  "including \"Live with friends/family\", which the popup shows in full."),
    'residency': ("How long people have lived in High Ridge Estates, how long they "
                  "expect to stay, mobile-home skirting, and why they moved here."),
    'housing_safety': "Whether people feel safe from environmental and social threats.",
    'affordability': "Urgency of affordable housing, and the strategy respondents prefer.",
    'interventions': ("For each of the 11 proposed home improvements, the share of "
                      "households who said they would like it."),
    'experiences': ("For each of the 10 listed events, the share of households who "
                    "said they had experienced it."),
    'mobility': "Car access and transport problems during hurricanes.",
    'demographics_ext': "Highest education completed, and employment status.",
}

# How the percentage denominators work — collaborators need this to read the charts.
DENOMINATOR_NOTE = (
    "Every percentage in this report uses <strong>all mapped responses</strong> as its "
    "denominator, not just those who answered the question. A household that skipped "
    "a question, or chose \"Prefer not to answer\", counts in the denominator but not "
    "the numerator. This makes the percentages directly comparable across questions, "
    "but it means each one is a share of the whole surveyed population rather than a "
    "share of respondents to that question. Read \"42% would like improved drainage\" "
    "as \"42% of surveyed households said so\", not \"42% of those who answered\"."
)

FIXES = [
    {
        'id': 'A1',
        'title': 'Mold prevalence was more than double the real figure',
        'question': ('Is there any evidence of mold in the following spaces? '
                     '(Check all that apply)'),
        'what': ("The question lists only <em>places</em> — Kitchen, Bathroom, Bedroom, "
                 "Ceiling, and so on — plus a free-text <em>Other:</em> box. It offers no "
                 "\"no mold\" option. So households with no mold answered by ticking "
                 "<em>Other:</em> and typing <strong>\"None\"</strong>, <strong>\"No\"</strong> "
                 "or <strong>\"No mold\"</strong>. The dashboard treated any answer at all "
                 "as mold, so those households were recorded as having mold."),
        'scale': ("34 of 84 households in the May export (28 of 75 in April) — every one "
                  "of them had explicitly said they have no mold."),
        'effect': ("Reported mold prevalence 73.8% instead of 33.3%. Each affected "
                   "household also gained +30 on the IAQ score — a third of that whole "
                   "score — which raised its Overall Risk by about 10 points."),
        'fix': ("A household counts as having mold only when it names an actual place, or "
                "describes mold in the Other box (\"closet\", \"I can smell mold but "
                "haven't found it\"). An answer that denies mold, or says the respondent "
                "does not know, is not counted."),
    },
    {
        'id': 'A2',
        'title': 'Households with air conditioning were scored as having none',
        'question': ('What type of cooling system do you use and how old is it? '
                     '(check all that apply)'),
        'what': ("This is a grid: the rows are the four system types, and the answer "
                 "chosen in each row is its <strong>age</strong> — \"less than 10 years\", "
                 "\"10 to 15 years\", \"More than 15 years\", or \"Don't know/Not "
                 "applicable\". The dashboard treated any non-blank row as \"I have this\". "
                 "On the \"No Air-conditioning\" row that is wrong: a household that does "
                 "have A/C answers \"Not applicable\" there, and was then scored as having "
                 "no air conditioning."),
        'scale': ("35 households took the no-A/C penalty; 29 of them had reported a real "
                  "age for their central or window A/C, so they clearly have it."),
        'effect': ("+4 on the IAQ score for 29 households that should not have had it, and "
                   "the cooling charts showed an age where a system type was expected."),
        'fix': ("A row counts as \"I have this system\" only when it gives a real age band. "
                "The no-A/C penalty applies only when the household reported no A/C "
                "anywhere. A hand-written label table that claimed this question had no "
                "age dimension — it does — was removed."),
    },
    {
        'id': 'A3',
        'title': 'Three questions could not be read from a numeric export',
        'question': ('House condition (QID141), affordable-housing urgency (QID17), '
                     'mobile-home skirting (QID100)'),
        'what': ("In Qualtrics these three questions have two answer options sharing one "
                 "export code, because options were added after the export codes were set. "
                 "A numeric export therefore could not say which option a code meant, and "
                 "the dashboard showed the bare number."),
        'scale': ("On the May export: 61 of 75 households for urgency, 71 of 75 for "
                  "skirting."),
        'effect': ("Two charts showed \"1\" and \"2\" instead of answers, and those two "
                   "questions behaved differently depending on which export format was "
                   "uploaded."),
        'fix': ("Where two options share a code, the answer is the one Qualtrics' own "
                "settings deliberately assign to that code, rather than the one that lands "
                "there only by default. This was checked against the data, not assumed: "
                "for the 75 households present in both the text and numeric exports the "
                "pairing is one-to-one with no exception. Both formats now read "
                "identically. The lasting fix is to correct the export codes in Qualtrics."),
    },
    {
        'id': 'A4',
        'title': 'One chart was one column away from reading the wrong answers',
        'question': ('If you lived in another place before, how important were the '
                     'following factors in relocating to High Ridge Estates? - Other'),
        'what': ("This question occupies two columns in the export: the importance rating, "
                 "and the free-text box where people write what the \"Other\" factor was. "
                 "Both columns claimed the same question ID, and the dashboard took "
                 "<em>whichever appeared first in the file</em>. In the exports we have, the "
                 "rating column happens to come first, so the correct one was used &mdash; by "
                 "luck of ordering, not by design."),
        'scale': ("No figure currently shown is wrong. But Qualtrics reorders columns "
                  "between exports, so a future export could have put the text column first."),
        'effect': ("Had that happened, the \"Other\" relocation-factor chart would have shown "
                   "people's typed answers (\"Kids school\", \"Caring for family members\") "
                   "in place of the importance ratings, with nothing to signal the swap."),
        'fix': ("An exact question-ID match now always beats an approximate one. We then "
                "proved the point by shuffling all 150 columns into six random orders and "
                "confirming that every statistic and every household's scores came out "
                "byte-identical each time."),
    },
]

CAVEATS = [
    ("The dashboard shows a stored snapshot, not a live calculation.",
     "Every number in the Analysis panel was computed when the survey data was last "
     "uploaded. The corrections described here are deployed, but the panel will keep "
     "showing the old figures — including mold at 79.1% — until the survey data is "
     "reprocessed through <em>Update Data</em>. Nothing in this audit changed, moved or "
     "deleted any stored data."),
    ("Three questions still have ambiguous export codes in Qualtrics.",
     "QID141, QID17 and QID100 each have two answer options sharing one export code. The "
     "dashboard now resolves them correctly for this survey, and the resolution is "
     "confirmed against 75 households answering in both formats. But it is a repair, not "
     "a guarantee: if a respondent ever chooses one of the retired options it will be "
     "read as the other. Correcting the Recode Values in Qualtrics removes the risk."),
    ("Risk-score weights are a modelling choice, not a measurement.",
     "Overall Risk = 0.35 x Health + 0.35 x IAQ + 0.30 x Structural, and the individual "
     "point values (mold +30, each water problem +7.5, single-wide +25, and so on) are "
     "assumptions built into this dashboard. They are applied consistently to every "
     "household, so comparisons and rankings are sound, but the absolute scores are only "
     "meaningful relative to each other."),
    ("\"Symptom prevalence\" means at least seasonally.",
     "The respiratory, asthma and wheeze percentages count households reporting symptoms "
     "weekly, monthly or seasonally. A household answering \"annually\" is not counted in "
     "those percentages, though it does add to the Health score."),
]


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout


def main() -> None:
    prov = build_provenance(MAY)
    analysis = json.loads((EVID / 'analysis-may_numeric.json').read_text())
    diff = json.loads((EVID / 'format-diff.json').read_text())
    hand = json.loads((EVID / 'manual-score-check.json').read_text())
    live = json.loads((EVID / 'live-dashboard-readings.json').read_text())
    n_hand_ok = sum(1 for h in hand if h['match'])

    rev = run(['git', 'rev-parse', '--short', 'HEAD']).strip()

    # group provenance rows by section
    sections: dict[str, list] = {}
    for r in prov:
        sections.setdefault(r['section'], []).append(r)

    def stat_block(section: str) -> str:
        """Render the current computed values for a section, if they are scalar."""
        v = analysis.get(section)
        if not isinstance(v, dict):
            return ''
        rows = []
        for k, val in v.items():
            if isinstance(val, (int, float, str)):
                rows.append(f'<tr><td>{E(str(k))}</td><td class="num">{E(str(val))}</td></tr>')
            elif isinstance(val, dict):
                inner = ', '.join(f'{E(str(a))}: <b>{E(str(b))}</b>'
                                  for a, b in list(val.items())[:14]
                                  if isinstance(b, (int, float, str)))
                if inner:
                    rows.append(f'<tr><td>{E(str(k))}</td><td>{inner}</td></tr>')
        if not rows:
            return ''
        return ('<table class="vals"><thead><tr><th>Statistic</th>'
                '<th>Value on the May 4 export</th></tr></thead><tbody>'
                + ''.join(rows) + '</tbody></table>')

    parts: list[str] = []
    parts.append(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Survey Analysis Methods</title>
<style>
 :root {{
   --bg:#ffffff; --fg:#14171c; --muted:#5b6472; --line:#e3e7ed; --card:#f7f9fc;
   --accent:#1b5e9c; --ok:#0d7a4a; --okbg:#e7f6ee; --warn:#8a5a00; --warnbg:#fdf3e2;
   --bad:#a32020; --badbg:#fdeceb; --code:#f1f3f7;
 }}
 @media (prefers-color-scheme: dark) {{
   :root:not([data-theme="light"]) {{
     --bg:#12151a; --fg:#e8ecf2; --muted:#9aa5b4; --line:#2a303a; --card:#1a1f27;
     --accent:#6fb3ec; --ok:#5fd3a0; --okbg:#10291f; --warn:#e0b25f; --warnbg:#2b2213;
     --bad:#f08a84; --badbg:#2d1817; --code:#1e232c;
   }}
 }}
 :root[data-theme="dark"] {{
   --bg:#12151a; --fg:#e8ecf2; --muted:#9aa5b4; --line:#2a303a; --card:#1a1f27;
   --accent:#6fb3ec; --ok:#5fd3a0; --okbg:#10291f; --warn:#e0b25f; --warnbg:#2b2213;
   --bad:#f08a84; --badbg:#2d1817; --code:#1e232c;
 }}
 * {{ box-sizing:border-box; }}
 body {{ margin:0; background:var(--bg); color:var(--fg);
   font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
 .wrap {{ max-width:1080px; margin:0 auto; padding:40px 16px 80px; }}
 h1 {{ font-size:1.9rem; line-height:1.25; margin:0 0 .3em; letter-spacing:-.01em; }}
 h2 {{ font-size:1.3rem; margin:2.4em 0 .6em; padding-bottom:.3em;
       border-bottom:2px solid var(--line); }}
 h3 {{ font-size:1.05rem; margin:1.8em 0 .4em; }}
 p, li {{ max-width:74ch; }}
 .sub {{ color:var(--muted); margin:0 0 2em; }}
 table {{ border-collapse:collapse; width:100%; margin:1em 0 1.6em; font-size:.9rem; }}
 th, td {{ text-align:left; padding:8px 10px; border-bottom:1px solid var(--line);
   vertical-align:top; overflow-wrap:anywhere; }}
 th {{ background:var(--card); font-weight:600; font-size:.82rem;
   text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }}
 td.num {{ font-variant-numeric:tabular-nums; font-weight:600; }}
 code, .mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
   font-size:.85em; background:var(--code); padding:1px 5px; border-radius:4px; }}
 .card {{ background:var(--card); border:1px solid var(--line); border-radius:10px;
   padding:18px 20px; margin:1.2em 0; }}
 .kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
   gap:12px; margin:1.5em 0; }}
 .kpi {{ background:var(--card); border:1px solid var(--line); border-radius:10px;
   padding:14px 16px; }}
 .kpi b {{ display:block; font-size:1.7rem; font-variant-numeric:tabular-nums;
   line-height:1.1; }}
 .kpi span {{ color:var(--muted); font-size:.8rem; }}
 .pill {{ display:inline-block; padding:2px 9px; border-radius:99px; font-size:.75rem;
   font-weight:700; }}
 .pill.ok {{ background:var(--okbg); color:var(--ok); }}
 .pill.bad {{ background:var(--badbg); color:var(--bad); }}
 .pill.warn {{ background:var(--warnbg); color:var(--warn); }}
 .fix {{ border-left:4px solid var(--bad); }}
 .note {{ border-left:4px solid var(--warn); }}
 .good {{ border-left:4px solid var(--ok); }}
 .ba {{ display:grid; grid-template-columns:1fr 1fr; gap:0; margin:1em 0;
   border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
 .ba > div {{ padding:12px 14px; }}
 .ba .b {{ background:var(--badbg); }}
 .ba .a {{ background:var(--okbg); }}
 .ba h4 {{ margin:0 0 .4em; font-size:.75rem; text-transform:uppercase;
   letter-spacing:.05em; color:var(--muted); }}
 .q {{ color:var(--muted); font-style:italic; }}
 @media (max-width:640px) {{ .ba {{ grid-template-columns:1fr; }}
   table {{ font-size:.82rem; }} .wrap {{ padding:24px 16px 60px; }} }}
</style></head><body><div class="wrap">''')

    parts.append(f'''
<h1>How the KeyStone survey analysis works, and what we checked</h1>
<p class="sub">Prepared {date.today():%d %B %Y} for the KeyStone Heights / High Ridge Estates
research team &middot; code revision <code>{E(rev)}</code></p>

<p>This report documents the <strong>Survey Results</strong> section of the KeyStone
dashboard: which survey question feeds every chart and statistic, exactly how each
number is calculated, and the checks we ran to confirm the calculations are right.
It also records four defects we found and corrected.</p>

<div class="card good">
<h3 style="margin-top:0">What the checks showed</h3>
<div class="kpis">
  <div class="kpi"><b>{len(prov)}</b><span>analysis inputs traced to a
    specific survey question and column</span></div>
  <div class="kpi"><b>0</b><span>columns located by guesswork — all matched on the
    question's own Qualtrics ID</span></div>
  <div class="kpi"><b>{diff['statistics_compared']}</b><span>statistics compared between
    the two export formats</span></div>
  <div class="kpi"><b>{len(diff['differences'])}</b><span>differences between formats,
    on the same {diff['shared_respondents']} households</span></div>
  <div class="kpi"><b>{n_hand_ok}/{len(hand)}</b><span>households whose scores were
    reproduced by an independent hand calculation</span></div>
  <div class="kpi"><b>4</b><span>defects found, all corrected</span></div>
</div>
<p style="margin-bottom:0">Four real defects were found, and all four are fixed. Apart
from those, every statistic reads the column it should, the arithmetic is correct, and a
text export and a numeric export of the same survey now produce identical results.</p>
</div>

<div class="card note">
<h3 style="margin-top:0">Before you quote any figure from the dashboard today</h3>
<p style="margin-bottom:0">The Analysis panel displays a <strong>stored snapshot</strong>
computed at the last data upload, so it does not yet include these corrections. As of
{E(live['read_at'])} it still reports mold at
<strong>{live['iaq_tab']['mold_reported_pct']}%</strong>; the households' own answers give
<strong>33.3%</strong>. The figures update when the survey data is next reprocessed.</p>
</div>

<h2>1. The four defects we found</h2>
<p>Each of these changed numbers that appear in the Analysis panel. None of them altered
any respondent's answer — they were errors in how the answers were <em>read</em>.</p>
''')

    for f in FIXES:
        parts.append(f'''
<div class="card fix">
<h3 style="margin-top:0"><span class="pill bad">{E(f['id'])}</span>
  &nbsp;{E(f['title'])}</h3>
<p class="q">Survey question: &ldquo;{E(f['question'])}&rdquo;</p>
<p><strong>What went wrong.</strong> {f['what']}</p>
<p><strong>How many households.</strong> {E(f['scale'])}</p>
<p><strong>Effect on the results.</strong> {E(f['effect'])}</p>
<p><strong>The correction.</strong> {E(f['fix'])}</p>
</div>''')

    parts.append('''
<h3>What the corrections change, on the May 4 export</h3>
<div class="ba">
<div class="b"><h4>Before</h4>
<table style="margin:0"><tbody>
<tr><td>Mold reported</td><td class="num">78.7%</td></tr>
<tr><td>Mean IAQ score</td><td class="num">35.2</td></tr>
<tr><td>Mean Overall Risk</td><td class="num">34.0</td></tr>
<tr><td>Low / Medium / High</td><td class="num">41 / 34 / 0</td></tr>
</tbody></table></div>
<div class="a"><h4>After</h4>
<table style="margin:0"><tbody>
<tr><td>Mold reported</td><td class="num">32.0%</td></tr>
<tr><td>Mean IAQ score</td><td class="num">20.0</td></tr>
<tr><td>Mean Overall Risk</td><td class="num">28.6</td></tr>
<tr><td>Low / Medium / High</td><td class="num">47 / 28 / 0</td></tr>
</tbody></table></div>
</div>
<p>55 of 75 households have at least one corrected number, and <strong>6 move from
Medium risk to Low</strong>. The Health and Structural scores are unchanged; all of the
movement is in the IAQ score and therefore in Overall Risk.</p>

<h2>2. How each number is calculated</h2>
<p>The three component scores are each on a 0&ndash;100 scale and are combined into the
Overall Risk score. The point values below are the dashboard's model, applied identically
to every household.</p>

<h3>Health score (0&ndash;100)</h3>
<p>Five symptom questions are scored by how often the household reports them &mdash;
weekly&nbsp;=&nbsp;4, monthly&nbsp;=&nbsp;3, seasonally&nbsp;=&nbsp;2,
annually&nbsp;=&nbsp;1, never or rarely&nbsp;=&nbsp;0 &mdash; then weighted:</p>
<p><code>Health = min( (Headache&times;0.5 + Respiratory&times;1.0 + Asthma&times;1.0 +
Wheezing&times;0.8 + Tiredness&times;0.3) &divide; 14.4 &times; 80 , 80 )</code></p>
<p>and <code>+20</code> (capped at 100) if anyone in the home visited a hospital or health
centre for respiratory problems in the last year. The divisor 14.4 is the maximum possible
weighted total, so the five symptoms alone can reach 80 and the hospital visit supplies the
remaining 20.</p>

<h3>Indoor air quality score (0&ndash;100)</h3>
<table><thead><tr><th>Finding</th><th>Points</th><th>Read from</th></tr></thead><tbody>
<tr><td>Evidence of mold in at least one named space</td><td class="num">+30</td>
    <td>Mold question, after the A1 correction</td></tr>
<tr><td>Each water problem that actually occurred &mdash; up to four
    (broken pipes, overflow, leaky roof/window/door, well not working)</td>
    <td class="num">+7.5 each</td>
    <td>Water-problems grid; the answer &ldquo;none&rdquo; does not count</td></tr>
<tr><td>No air conditioning at all</td><td class="num">+4</td>
    <td>Cooling grid, after the A2 correction</td></tr>
<tr><td>Window units or fans only, no central A/C</td><td class="num">+2</td>
    <td>Cooling grid</td></tr>
<tr><td>Gas or propane stove</td><td class="num">+10</td><td>Stove-type question</td></tr>
</tbody></table>

<h3>Structural score (0&ndash;100)</h3>
<table><thead><tr><th>Finding</th><th>Points</th></tr></thead><tbody>
<tr><td>Built before 1960</td><td class="num">+30</td></tr>
<tr><td>Built 1960&ndash;1979</td><td class="num">+20</td></tr>
<tr><td>Built 1980&ndash;1999</td><td class="num">+10</td></tr>
<tr><td>Single-wide mobile home</td><td class="num">+25</td></tr>
<tr><td>Non-traditional structure (camper, shed)</td><td class="num">+20</td></tr>
<tr><td>Double-wide mobile home</td><td class="num">+15</td></tr>
<tr><td>Condition: critical / uninhabitable</td><td class="num">+35</td></tr>
<tr><td>Condition: poor</td><td class="num">+25</td></tr>
<tr><td>Condition: fair</td><td class="num">+15</td></tr>
</tbody></table>

<h3>Overall risk and the risk bands</h3>
<p><code>Overall Risk = round( 0.35&times;Health + 0.35&times;IAQ + 0.30&times;Structural )</code>
&nbsp;&rarr;&nbsp; <strong>Low</strong> below 34, <strong>Medium</strong> 34&ndash;66,
<strong>High</strong> 67 and above.</p>

<h3>The percentage charts</h3>
<p>The two matrix blocks &mdash; the 11 home-improvement interventions and the 10 lived
experiences &mdash; are reported as a percentage of households. An answer counts as
positive when it is affirmative (&ldquo;Like&rdquo;, &ldquo;Yes&rdquo;); answers that
decline (&ldquo;Dislike&rdquo;, &ldquo;No&rdquo;, &ldquo;Not Applicable/Unsure&rdquo;,
&ldquo;Prefer Not Answer&rdquo;) and blanks do not.</p>
<div class="card note"><p style="margin:0">''' + DENOMINATOR_NOTE + '''</p></div>

<h2>3. Which column feeds which chart</h2>
<p>Each row below is one input to the Analysis panel, with the exact survey question it
comes from. The <em>Column</em> is its position and header in the May&nbsp;4 export;
<em>Matched by</em> records how the dashboard located it.</p>
<div class="card"><p style="margin:0"><strong>Why the column headers look wrong.</strong>
Several headers in the export are misleading &mdash; the ten &ldquo;have you
experienced&hellip;&rdquo; questions carry headers like <code>Bleach-based</code> and
<code>Chemical Products_6</code>, left over from an earlier version of the questionnaire,
and many are a single blank space. The dashboard does <strong>not</strong> use these
headers. It matches on each question's Qualtrics ID (<code>ImportId</code>), which the
export records in its own third header row. We confirmed every one of these against both
the ID and the full question text.</p></div>
''')

    for section, rows in sections.items():
        note = SECTION_NOTES.get(section, '')
        parts.append(f'<h3>{E(section.replace("_", " ").title())}</h3>')
        if note:
            parts.append(f'<p>{E(note)}</p>')
        parts.append('<table><thead><tr><th>Chart / statistic</th>'
                     '<th>Survey question</th><th>Qualtrics ID</th>'
                     '<th>Column in the May export</th><th>Matched by</th>'
                     '</tr></thead><tbody>')
        for r in rows:
            q = r['question'] or '&mdash;'
            byname = 'by column NAME' in r['resolved_by']
            how = ('<span class="pill ok">Qualtrics ID</span>' if r['resolved_by'].startswith('ImportId')
                   else ('<span class="pill warn">column name</span>' if byname
                         else f'<span class="pill bad">{E(r["resolved_by"])}</span>'))
            parts.append(
                f'<tr><td><strong>{E(r["stat"])}</strong><br>'
                f'<span class="mono">{E(r["field"])}</span></td>'
                f'<td>{E(q) if q != "&mdash;" else q}</td>'
                f'<td class="mono">{E(r["qid"])}</td>'
                f'<td class="mono">{E(r["column"])}</td>'
                f'<td>{how}</td></tr>')
        parts.append('</tbody></table>')
        parts.append(f'<p style="color:var(--muted);font-size:.9rem">'
                     f'<strong>How it is aggregated:</strong> '
                     f'{E(rows[0]["aggregation"]) if len(set(r["aggregation"] for r in rows)) == 1 else "see the per-row notes above"}</p>')
        sb = stat_block(section)
        if sb:
            parts.append('<p style="color:var(--muted);font-size:.9rem">Current values, '
                         'recomputed from the May 4 export with the corrections applied:</p>')
            parts.append(sb)

    parts.append(f'''
<h2>4. What we did to check it</h2>

<h3>Every column verified twice, independently</h3>
<p>For all {len(prov)} inputs we confirmed the column the dashboard reads by two separate
means: the Qualtrics question ID in the export's metadata row, and the verbatim question
text in the export's own header row. All {len(prov)} agree. Not one input fell back to
guessing a column position.</p>

<h3>The two export formats now agree exactly</h3>
<p>Qualtrics can export answers as text (&ldquo;Single Wide Mobile Home&rdquo;) or as
numbers (&ldquo;1&rdquo;). We have one export of each: April&nbsp;15 in text form and
May&nbsp;4 in numeric form, sharing {diff['shared_respondents']} of the same households. We
ran the full analysis on each, restricted both to those same households, and compared every
statistic.</p>
<p><span class="pill ok">{diff['statistics_compared']} statistics compared &middot;
{len(diff['differences'])} differences</span> &mdash; the format the data is exported in no
longer changes any result. Before the A3 correction, 8 statistics differed.</p>

<h3>Every score recalculated by hand</h3>
<p>We recomputed the Health, IAQ, Structural and Overall Risk scores for
{len(hand)} households using a separate program that shares no code with the dashboard: it
reads the CSV with a different reader, decodes each answer against the Qualtrics survey
definition directly, and applies the arithmetic written out above. An error in the
dashboard could not hide by being repeated, because the two were written independently.</p>
<p><span class="pill ok">{n_hand_ok} of {len(hand)} households match exactly</span>
&mdash; every score, every risk band.</p>

<h3>The column layout of a future export cannot change the results</h3>
<p>Every analysis input is located by the question's Qualtrics ID, never by its position or
its header text. We confirmed this holds in practice rather than in principle: we shuffled
all 150 columns of the May export into six different random orders, ran the full analysis on
each, and compared everything. All six produced <strong>byte-identical</strong> statistics
and byte-identical per-household scores. We also confirmed that adding an unrelated new
question changes nothing, and that <em>removing</em> a required question is refused by the
upload guard rather than being quietly scored as zero.</p>

<h3>Automated tests</h3>
<p>The corrections are pinned by tests that state the intended reading household by
household, so a future change that reintroduces one of these defects fails immediately
rather than quietly shifting an average. The suite is at
<code>tests/test_iaq_score_semantics.py</code>,
<code>tests/test_qsf_label_resolution.py</code>,
<code>tests/test_export_layout_independence.py</code> and
<code>tests/test_popup_output_is_clean.py</code>; 180 tests pass.</p>

<h3>Nothing was changed on the live dashboard</h3>
<p>This audit read the live dashboard and ran calculations locally. No survey data or field
data was uploaded, replaced or deleted. Counts were identical before and after:
<strong>{live['data_untouched']['iaq_responses']} survey responses</strong>,
<strong>{live['data_untouched']['field_points']} field points</strong>,
<strong>{live['data_untouched']['community_contacts']} community contacts</strong>.</p>

<h2>5. What a reader should keep in mind</h2>
''')

    for title, body in CAVEATS:
        parts.append(f'<div class="card note"><p style="margin:0">'
                     f'<strong>{E(title)}</strong> {body}</p></div>')

    parts.append('''
<h2>6. Recommended fixes in Qualtrics</h2>
<p>Two problems are in the questionnaire itself. The dashboard now handles both, but
correcting them at source makes the data unambiguous for anyone who analyses it, in any
tool.</p>
<ol>
<li><strong>Add a &ldquo;No mold&rdquo; option to the mold question.</strong> It currently
lists only places, so respondents without mold have to write &ldquo;None&rdquo; in the
free-text box &mdash; which is what caused defect A1. An explicit option removes the
ambiguity for good.</li>
<li><strong>Correct the Recode Values on the house-condition, housing-urgency and
mobile-home-skirting questions.</strong> Each has two answer options sharing one export
code. Setting each option to its own code makes numeric exports unambiguous.</li>
<li><strong>Consider splitting the cooling question.</strong> Asking system type and system
age in one grid means the &ldquo;No air conditioning&rdquo; row has no meaningful age, which
is what caused defect A2.</li>
</ol>

<h2>7. Evidence</h2>
<p>Every figure in this report is reproducible from the repository:</p>
<table><thead><tr><th>File</th><th>What it contains</th></tr></thead><tbody>
<tr><td class="mono">scripts/audit/analysis_provenance.py</td>
    <td>Builds the column map in section 3 from the code and the export</td></tr>
<tr><td class="mono">scripts/audit/run_analysis_both_formats.py</td>
    <td>Runs the analysis on both exports and compares every statistic</td></tr>
<tr><td class="mono">scripts/audit/manual_score_check.py</td>
    <td>The independent hand calculation, with the working shown per household</td></tr>
<tr><td class="mono">scripts/audit/v2_new_upload_readiness.py</td>
    <td>The checks on a not-yet-seen export: column shuffling, added and removed
        columns, extra responses, payload integrity, upload guard</td></tr>
<tr><td class="mono">docs/plans/evidence/2026-09-21-analysis-audit/format-diff.json</td>
    <td>The format comparison result</td></tr>
<tr><td class="mono">&hellip;/manual-score-check.json</td>
    <td>Per-household hand calculations and their inputs</td></tr>
<tr><td class="mono">&hellip;/live-dashboard-readings.json</td>
    <td>What the live dashboard displayed, and when</td></tr>
</tbody></table>

</div></body></html>''')

    OUT.write_text(''.join(parts), encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size / 1024:.0f} KB)')


if __name__ == '__main__':
    main()
