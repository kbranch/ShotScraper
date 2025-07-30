getRankings = """
declare @kingdom nvarchar(20) = ?
declare @type varchar(20) = ?
declare @startDate datetime2 = dateadd(hour, 5, ?) -- Jank because UTC
declare @endDate datetime2 = dateadd(hour, 5, ?)

select Rankings.PlayerId
      ,Rankings.Name
	  ,Rankings.Power
	  ,Rankings.Rank
	  ,Rankings.Alliance
	  ,cast(datediff(second,{d '1970-01-01'}, dateadd(hour, 10, Samples.Date)) as bigint) * 1000 as Date
from Rankings
join Samples
  on Samples.SampleId = Rankings.SampleId
where Samples.Kingdom = @kingdom
      and Samples.Type = @type
	  and Samples.Date between dateadd(hour, -10, @startDate) and dateadd(hour, 10, @endDate)
group by Rankings.PlayerId
		,Rankings.Name
		,Rankings.Power
		,Rankings.Rank
		,Rankings.Alliance
		,Samples.Date
"""

getAllianceRankings = """
declare @kingdom nvarchar(20) = ?
declare @type varchar(20) = ?
declare @startDate datetime2 = dateadd(hour, 5, ?) -- Jank because UTC
declare @endDate datetime2 = dateadd(hour, 5, ?)

select Rankings.Alliance
      ,sum(Rankings.Power) as Power
	  ,datediff(second,{d '1970-01-01'}, dateadd(hour, 10, Samples.Date)) as Date
from Rankings
join Samples
  on Samples.SampleId = Rankings.SampleId
where Samples.Kingdom = @kingdom
      and Samples.Type = @type
	  and Samples.Date between dateadd(hour, -10, @startDate) and dateadd(hour, 10, @endDate)
group by Rankings.Alliance
		,Samples.Date
"""

getRankingGrowth = """
declare @kingdom nvarchar(20) = ?
declare @type varchar(20) = ?
declare @startDate datetime2 = dateadd(hour, 5, ?) -- Jank because UTC
declare @endDate datetime2 = dateadd(hour, 5, ?)

select LastRankings.PlayerId
      ,LastRankings.Name
	  ,LastRankings.Power
	  ,FirstRankings.Power as StartPower
	  ,LastRankings.Power - FirstRankings.Power as Growth
	  ,(LastRankings.Power - FirstRankings.Power) / cast(FirstRankings.Power as float) as GrowthPercent
	  ,LastRankings.Rank
	  ,LastRankings.Alliance
	  ,datediff(s, '1970-01-01 00:00:00', Samples.Date) as Date
from Rankings as LastRankings
outer apply (
	select top 1 First = FIRST_VALUE(SampleId) OVER (PARTITION BY Kingdom ORDER BY Date)
                ,Last = FIRST_VALUE(SampleId) OVER (PARTITION BY Kingdom ORDER BY Date DESC)
	from Samples
	where Samples.Kingdom = @kingdom
	      and Samples.Type = @type
		  and Samples.Date between dateadd(hour, -10, @startDate) and dateadd(hour, 10, @endDate)
) as targetSamples
outer apply (
	select *
	from Rankings
	where Rankings.SampleId = targetSamples.First
	      and Rankings.PlayerId = LastRankings.PlayerId
) as FirstRankings
join Samples
  on Samples.SampleId = targetSamples.Last
where LastRankings.SampleId = targetSamples.Last
"""

getAllianceRankingGrowth = """
declare @kingdom nvarchar(20) = ?
declare @type varchar(20) = ?
declare @startDate datetime2 = dateadd(hour, 5, ?) -- Jank because UTC
declare @endDate datetime2 = dateadd(hour, 5, ?)

;with Alliances as (
	select Rankings.Alliance
	from Rankings
	outer apply (
		select top 1 First = FIRST_VALUE(SampleId) OVER (PARTITION BY Kingdom ORDER BY Date)
					,Last = FIRST_VALUE(SampleId) OVER (PARTITION BY Kingdom ORDER BY Date DESC)
		from Samples
		where Samples.Kingdom = @kingdom
			  and Samples.Type = @type
			  and Samples.Date between dateadd(hour, -10, @startDate) and dateadd(hour, 10, @endDate)
	) as targetSamples
	where Rankings.SampleId = targetSamples.Last
	group by Rankings.Alliance
)

select Alliances.Alliance
      ,FirstRankings.Power as FirstPower
	  ,LastRankings.Power as LastPower
	  ,LastRankings.Power - FirstRankings.Power as Growth
	  ,(LastRankings.Power - FirstRankings.Power) / cast(FirstRankings.Power as float) as GrowthPercent
	  ,LastRankings.PlayerCount
from Alliances
outer apply (
	select top 1 First = FIRST_VALUE(SampleId) OVER (PARTITION BY Kingdom ORDER BY Date)
                ,Last = FIRST_VALUE(SampleId) OVER (PARTITION BY Kingdom ORDER BY Date DESC)
	from Samples
	where Samples.Kingdom = @kingdom
	      and Samples.Type = @type
		  and Samples.Date between dateadd(hour, -10, @startDate) and dateadd(hour, 10, @endDate)
) as targetSamples
outer apply (
	select sum(Rankings.Power) as Power
	from Rankings
	where Rankings.SampleId = targetSamples.First
	      and Rankings.Alliance = Alliances.Alliance
	group by Rankings.Alliance
) as FirstRankings
outer apply (
	select sum(Rankings.Power) as Power
		,count(*) as PlayerCount
	from Rankings
	where Rankings.SampleId = targetSamples.Last
	      and Rankings.Alliance = Alliances.Alliance
	group by Rankings.Alliance
) as LastRankings

"""