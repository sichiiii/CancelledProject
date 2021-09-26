from app import app, db
from sqlalchemy import create_engine 
from models.data import Channels, TimeLastCorrectChannels, SetParamsStatus, TractTable, TimeLastCorrectTract, ChannelStatus, EquipNums, EquipNumsArr, ControlParamsList, CommandStatus
import app_logger

engine = create_engine('sqlite:///test.db')
conn = engine.connect()

def insertChannels(channelNum, identA, portA, identB, portB, channelType, connectionType):
    conn.execute(f"INSERT INTO channels (channelNum, identA, portA, identB, portB, \
        channelType, connectionType) VALUES('{channelNum}', '{identA}', '{portA}', '{ident}')")

def insertTLCC(time):
    conn.execute(f"INSERT INTO time_last_correct_channels (time) VALUES('{time}')")

def insertSetParamsStatus(status):
    conn.execute(f"INSERT INTO set_params_status (status) VALUES('{status}')")

def insertTractTable(num, identA, portA, identB, portB, tractType, reservTractNum):
    conn.execute(f"INSERT INTO tract_table (num, identA, portA, identB, portB, tractType, \
        reservTractNum) VALUES('{num}', '{identA}', '{portA}', '{identB}', '{portB}', '{tractType}', '{reservTractNum}')")

def insertTimeLastCorTract(time):
    conn.execute(f"INSERT INTO time_last_correct_tract (time) VALUES('{time}')")

def insertChannelStatus(status, initiator, time, connectionNum):
    conn.execute(f"INSERT INTO channel_status (status, initiator, time, connectionNum) \
        VALUES('{status}', '{initiator}', '{time}', '{connectionNum}')")

def insertEquipNums(identArr):
    conn.execute(f"INSERT INTO equip_nums DEFAULT VALUES")
    idArr = conn.execute("SELECT MAX(ID) FROM equip_nums").fetchall()
    for i in range(len(identArr)):
       conn.execute(f"INSERT INTO equip_nums_arr (ident, equipid) VALUES('{identArr[i]}', '{idArr[0][0]}')")

def insertControlParamsList(ident):
    conn.execute(f"INSERT INTO control_params_list (ident) VALUES('{ident}')")

def insertCommandStatus(status):
    conn.execute(f"INSERT INTO command_status (status) VALUES('{status}')")

insertEquipNums(['23123,', '23123123', '123123'])
