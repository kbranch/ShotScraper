import pyodbc
import config
import queries
import platform

connectionString = f"""
    DRIVER={"{SQL Server}" if platform.system() == "Windows" else "ODBC Driver 18 for SQL Server"};
    SERVER={config.serverName};
    DATABASE={config.database};
    UID={config.username};
    PWD={config.password};
    Trusted_Connection=no;
    TrustServerCertificate=yes;
"""

def getRankings(kingdom, type):
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    cursor.execute(queries.getRankings, (kingdom, type))

    rankings = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    cursor.close()
    conn.close()

    return [{columns[i]: row[i] for i in range(len(columns))} for row in rankings]
