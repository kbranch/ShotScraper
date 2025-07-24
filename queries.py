insertRanking = """
INSERT INTO Rankings (Type, SampleId, PlayerId, Name, Power, Rank, Alliance, Date, Kingdom)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""