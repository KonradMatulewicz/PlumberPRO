# Runbook: Row volume drop

## Symptoms
A run succeeds but loads far fewer rows than the usual weekday baseline (z-score <= -3).

## Likely causes
1. Upstream extract returned a partial file (late or truncated delivery).
2. A filter or join in the transformation changed and drops rows.
3. Source system outage during the extraction window.

## Diagnosis steps
- Compare `rows_loaded` with the last 7 same-weekday runs.
- Check upstream pipeline run times and file sizes for the same business date.
- Diff the transformation code deployed since the last normal run.

## Fix
Re-run the extract once the upstream delivery is complete; revert the faulty change if any.

## Prevention
Add a dbt test on the target model, e.g. a row-count threshold relative to the 7-day average.
