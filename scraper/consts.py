from config import *

connectionString = f"""
    DRIVER={{SQL Server}};
    SERVER={serverName};
    DATABASE={database};
    UID={username};
    PWD={password};
    Trusted_Connection=no;
"""

pageSize = 7
headerHeight = 33
sidebarWidth = 34

swipeDownTop = (0.5, 0.25933609958506224066)
swipeDownBottom = (0.5, 0.98029045643153526971)

swipeUpTop = (0.5, 0.05)
swipeUpBottom = (0.5, 0.69)
swipeRecoil = (0.6, 0.05)

listTop = 0.12202688728024819028
rankHeight = 0.10548086866597724922

lineClickPoint = (0.5, listTop + rankHeight / 2)

rankRect = (0.07536764705882352941, listTop, 0.17647058823529411765, listTop + rankHeight)

powerRect = (0.69669117647058823529, listTop, 0.95036764705882352941, listTop + rankHeight)

backPoint = (0.07352941176470588235, 0.03102378490175801448)

idCopyPoint = (0.89154411764705882353, 0.74870734229576008273)

nameDotsPoint = (0.88970588235294117647, 0.71044467425025853154)
nameCopyPoint = (0.51102941176470588235, 0.56566701137538779731)

titleRect = (0.12316176470588235294, 0.00723888314374353671, 0.90257352941176470588, 0.05067218200620475698)

kingdomRect = (0.52757352941176470588, 0.85935884177869700103, 0.75183823529411764706, 0.88624612202688728025)