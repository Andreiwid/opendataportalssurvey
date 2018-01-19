-- The 10 largest open data portals in the world
select top 10 cats.url,
		cats.product,
		cats.COUNTRY,
	   COUNT(*) AS TotalDatasets
from catsidentified_noduplication as cats inner join datasets
	on cats.ID = datasets.ID
group by url, country, cats.product
order by TotalDatasets desc
