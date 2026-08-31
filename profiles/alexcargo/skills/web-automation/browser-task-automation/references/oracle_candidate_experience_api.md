# Oracle Candidate Experience (HCM) REST API & Job Monitoring

## API Endpoint
For career portals hosted on Oracle Cloud Candidate Experience (`.../hcmUI/CandidateExperience/en/sites/<site_id>/jobs...`):

- **REST Endpoint**:
  `GET https://<domain>/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=all&finder=findReqs;siteNumber=<site_id>,limit=50,sortBy=POSTING_DATES_DESC`
  
- **Direct Job Requisition Link**:
  `https://<domain>/hcmUI/CandidateExperience/en/sites/<site_id>/job/<Requisition_Id>`

## Key Finder Parameters
- `siteNumber`: Target career site ID (e.g. `CX_1`).
- `limit`: Number of job requisitions per page (e.g. `50`).
- `sortBy`: Sorting order (`POSTING_DATES_DESC` for newest jobs first).
- `facetsList`: Optional facets filter (`LOCATIONS;WORK_LOCATIONS;TITLES;CATEGORIES;ORGANIZATIONS;POSTING_DATES`).

## Response Structure
```json
{
  "items": [
    {
      "TotalJobsCount": 476,
      "requisitionList": [
        {
          "Id": "24034",
          "Title": "SDET I",
          "PostedDate": "2026-08-05",
          "PrimaryLocation": "Bangalore, Karnataka, India",
          "Category": "Engineering"
        }
      ]
    }
  ]
}
```

## Differential Monitoring Pattern (JSON Cache)
When writing a recurring Python script for cron monitoring:
1. Maintain seen job IDs in `~/.hermes/cache/<portal_name>_seen_jobs.json`.
2. On first run, record all existing job IDs so you don't dump hundreds of old jobs.
3. On subsequent runs, filter items where `str(job['Id'])` is not in `seen_ids`.
4. Return formatted markdown results with clickable direct links (`[Title](URL)`), location (`PrimaryLocation`), and publication date (`PostedDate`).

## Cronjob Parameter Gotcha
- Store the monitoring script in `~/.hermes/scripts/<script_name>.py`.
- Call `cronjob(action='create', script='<script_name>.py', schedule='0 9 * * *', deliver='all')`.
- Pass `script` as a filename relative to `~/.hermes/scripts/`, NOT as an absolute path like `C:/Users/...`.
- Pass `deliver='all'` or explicit target channel so cron execution outputs deliver live alerts to connected Telegram channels instead of silent local logs (`deliver='local'`).
