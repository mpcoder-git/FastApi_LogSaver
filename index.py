from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import  Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:root@localhost/logsklad")
Base = declarative_base()
Session = sessionmaker(autoflush=False, bind=engine)

class Logrow(Base):
    __tablename__ = "logtable"
  
    Id = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer)
    LocalName = Column(String)
    Component = Column(String)
    Querytext = Column(Text)
    Datetimesave = Column(DateTime)



app = FastAPI()
 
@app.get("/")
def read_root():
    html_content = "<h2>WEB SERVER LOGSAVER</h2>"
    return HTMLResponse(content=html_content)

@app.get("/status")
def fn_status():
    html_content = "OK"
    return HTMLResponse(content=html_content)

@app.post("/logsave")
def fn_logsave(useridx='', locname='', dataset='', querytext='', dtsave='0000-00-00 00:00:00'):
    if (useridx == '') or (locname == '') or (dataset == '') or (querytext == '') or (dtsave == '0000-00-00 00:00:00'):
        message = "Одна или несколько переменных не найдены"
        return HTMLResponse(content=message)
    else:
        #print(querytext)
        message = ""
        # создаем сессию подключения к бд
        with Session(autoflush=False, bind=engine) as db:
            # создаем объект Logrow для добавления в бд
            lrow = Logrow(UserId=useridx, LocalName=locname, Component=dataset, Querytext=querytext, Datetimesave=dtsave)
            db.add(lrow)     # добавляем в бд
            db.commit()     # сохраняем изменения
            #print(lrow.id)   # можно получить установленный id
            message = str(lrow.Id)
            return HTMLResponse(content=message)