select cats.product,
		url,
	   count(datasets.id) AS TotalDatasets
into #totaldatasetsurlproduto
from catsidentified_noduplication as cats left outer join datasets
	on cats.ID = datasets.ID
where product in ('CKAN', 'SOCRATA', 'ARCGIS', 'OPENDATASOFT')
group by cats.product, url
go
select * from #totaldatasetsurlproduto
go
select product,
	   avg(totaldatasets),
	   '= 0' = count(case when totaldatasets = 0 then 1 end),
	   '1-10' = count(case when totaldatasets between 1 and 10 then 1 end),
	   '11-100' = count(case when totaldatasets between 11 and 100 then 1 end),
	   '101-1,000' = count(case when totaldatasets between 101 and 1000 then 1 end),
	   '1,001-10,000' = count(case when totaldatasets between 1001 and 10000 then 1 end),
	   '>10,000' = count(case when totaldatasets > 10000 then 1 end)
from #totaldatasetsurlproduto
group by product
union
select 'TOTAL' AS product,
	   avg(totaldatasets),
	   '= 0' = count(case when totaldatasets = 0 then 1 end),
	   '1-10' = count(case when totaldatasets between 1 and 10 then 1 end),
	   '11-100' = count(case when totaldatasets between 11 and 100 then 1 end),
	   '101-1,000' = count(case when totaldatasets between 101 and 1000 then 1 end),
	   '1,001-10,000' = count(case when totaldatasets between 1001 and 10000 then 1 end),
	   '>10,000' = count(case when totaldatasets > 10000 then 1 end)
from #totaldatasetsurlproduto
