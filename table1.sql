SELECT  SOURCE, 
		COUNT(*) AS 'TOTAL OF URLS',
		'CKAN' = COUNT(CASE WHEN product = 'CKAN' THEN 1 END),
		'ARCGIS' = COUNT(CASE WHEN product = 'ARCGIS' THEN 1 END),
		'SOCRATA' = COUNT(CASE WHEN product = 'SOCRATA' THEN 1 END),
		'OPENDATASOFT' = COUNT(CASE WHEN product = 'OPENDATASOFT' THEN 1 END),
		'ERRO' = COUNT(CASE WHEN product = 'ERROR' THEN 1 END),
		'not identified' = COUNT(CASE WHEN product not in ('error', 'none') THEN 1 END)
FROM catsidentified_withduplication
GROUP BY SOURCE

UNION

SELECT  'TOTAL (duplication removed)' AS SOURCE, 
		COUNT(*) AS 'TOTAL OF URLS',
		'CKAN' = COUNT(CASE WHEN product = 'CKAN' THEN 1 END),
		'ARCGIS' = COUNT(CASE WHEN product = 'ARCGIS' THEN 1 END),
		'SOCRATA' = COUNT(CASE WHEN product = 'SOCRATA' THEN 1 END),
		'OPENDATASOFT' = COUNT(CASE WHEN product = 'OPENDATASOFT' THEN 1 END),
		'ERRO' = COUNT(CASE WHEN product = 'ERROR' THEN 1 END),
		'not identified' = COUNT(CASE WHEN product not in ('error', 'none') THEN 1 END)
FROM catsidentified_noduplication
