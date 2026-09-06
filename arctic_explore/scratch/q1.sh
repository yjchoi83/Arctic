set -u
qs=("Sentinel-1 sea ice navigation safety"
"Northern Sea Route SAR"
"Arctic ice routing POLARIS"
"Arctic navigability Sentinel-1 chokepoint"
"Arctic shipping risk index multi-criteria validation"
"NISAR sea ice"
"L-band C-band sea ice fusion"
"landfast ice breakup SAR port"
"Arctic shipping besetting grounding"
"SAR bathymetry Arctic chart adequacy")
for q in "${qs[@]}"; do
  echo "=== $q"
  eq=$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")
  curl -s --max-time 40 "https://api.openalex.org/works?search=$eq&per-page=5&filter=from_publication_date:2023-01-01&select=title,publication_year,doi,primary_location,cited_by_count&mailto=ldg810@koreatech.ac.kr" \
   | jq -r '.results[]? | "\(.publication_year) | \(.title[0:110]) | \(.primary_location.source.display_name // "NA") | \(.doi // "NA") | c=\(.cited_by_count)"'
  sleep 1
done
