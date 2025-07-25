insertSample = """
insert into Samples (Name, Kingdom, Type)
values (?, ?, ?)
"""

getId = """
select @@identity as id
"""

insertRanking = """
insert into Rankings (SampleId, PlayerId, Name, Power, Rank, Alliance, Date)
values (?, ?, ?, ?, ?, ?, ?)
"""