getRankings = """
select Rankings.PlayerId
      ,Rankings.Name
	  ,Rankings.Power
	  ,Rankings.Rank
	  ,Rankings.Alliance
	  --,datediff(second,{d '1970-01-01'}, max(Rankings.Date)) as Date
	  ,max(Rankings.Date) as Date
from Rankings
where Rankings.Kingdom = ?
      and Rankings.Type = ?
	  --and Rankings.PlayerId in ('101554177', '104650801', '101636054', '101046699', '103044922')
group by Rankings.Type
        ,Rankings.PlayerId
		,Rankings.Name
		,Rankings.Power
		,Rankings.Rank
		,Rankings.Alliance
"""