-- datasets per platform
select cats.product,
	   COUNT(datasets.ID) AS TotalDatasets
from catsidentified_noduplication as cats inner join datasets
	on cats.ID = datasets.ID
group by cats.product

-- cats per platform
select cats.product,
	   COUNT(*) AS TotalCats
from catsidentified_noduplication as cats 
group by cats.product
