-- top 10 countries
--datasets per country
select top 10 cats.country,
	   COUNT(datasets.ID) AS TotalDatasets
from catsidentified_noduplication as cats inner join datasets
	on cats.ID = datasets.ID
where product not in ('error', 'none') and country <> 'international'
group by cats.country
order by TotalDatasets desc

-- cats per country
select top 10 cats.country,
	   COUNT(*) AS TotalCats
from catsidentified_noduplication as cats 
where product not in ('error', 'none') and country <> 'international'
group by cats.country
order by TotalCats desc
