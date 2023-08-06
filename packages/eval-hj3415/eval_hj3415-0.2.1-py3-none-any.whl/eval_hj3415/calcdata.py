import math
from db_hj3415 import setting, mongo, sqlite
from .report import make_eval_df_all

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)

# avgper 과 yieldgap 계산


def calc_avg_per() -> float:
    # 가중조화평균으로 평균 per 산출 mi db에 저장
    per_r_cap_all = []
    cap_all = []
    eval_list = make_eval_df_all().to_dict('records')
    for data in eval_list:
        # eval data: {'code': '111870', '종목명': 'KH 일렉트론', '주가': 1070, 'PER': -2.28, 'PBR': 0.96,
        # '시가총액': 103300000000, 'RED': -11055.0, '주주수익률': -7.13, '이익지표': -0.30426, 'ROIC': -40.31,
        # 'ROE': 0.0, 'PFCF': -7.7, 'PCR': nan}
        logger.debug(f'eval data: {data}')
        if data['PER'] is None or data['PER'] == 0 or math.isnan(data['PER']):
            continue
        if data['시가총액'] is None or math.isnan(data['시가총액']):
            continue
        cap_all.append(data['시가총액'])
        per_r_cap_all.append((1 / data['PER']) * data['시가총액'])
    logger.debug(f'Count cap_all :{len(cap_all)}')
    logger.debug(f'Count per_r_cap_all : {len(per_r_cap_all)}')
    try:
        return round(sum(cap_all) / sum(per_r_cap_all), 2)
    except ZeroDivisionError:
        return float('nan')


def calc_yield_gap(avg_per: float) -> float:
    # 장고에서 사용할 yield gap, mi db에 저장
    date, gbond3y = mongo.MI(index='gbond3y').get_recent()
    if math.isnan(avg_per) or avg_per == 0:
        return float('nan')
    else:
        yield_share = (1 / avg_per) * 100
        yield_gap = round(yield_share - float(gbond3y), 2)
        logger.debug(f'Date - {date}, gbond3y - {gbond3y}, yield_gap - {yield_gap}')
        return yield_gap


def save_to_db(avg_per: float, yield_gap: float):
    """
    평균 per과 yield gap을 mi 데이터베이스에 저장한다.
    """
    s = load_db.Settings()
    date = datetime.today().strftime('%Y.%m.%d')
    if 'mongo' in s.contents['activated_db']:
        # mongodb에 연결
        mongo_addr = s.contents['mongo_addr']
        logger.info(f"mongodb addr : {mongo_addr}")
        db = MongoClient(mongo_addr).mi
        print(f"Save to mongo db...date : {date} avgper : {avg_per} yieldgap : {yield_gap}")

        # insert avgper
        col = db['avgper']
        query = {'date': {"$eq": date}}
        col.delete_many(query)
        data = {
            "date": date,
            "value": avg_per,
        }
        col.insert_one(data)

        # insert yieldgap
        col = db['yieldgap']
        query = {'date': {"$eq": date}}
        col.delete_many(query)
        data = {
            "date": date,
            "value": yield_gap,
        }
        col.insert_one(data)

    if 'sqlite' in s.contents['activated_db']:
        # sqlite3에 연결
        sqlite_path = s.contents['sqlite_path']
        logger.info(f"sqlite3 path : {sqlite_path}")
        engine = make_engine(sqlite_path)
        print(f"Save to sqlite3 db...date : {date} avgper : {avg_per} yieldgap : {yield_gap}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        # insert avgper
        mi_item = session.query(AvgPer).filter(AvgPer.date == date).first()
        logger.info(f'Query result : {mi_item}')
        if mi_item:
            setattr(mi_item, 'value', avg_per)
        else:
            session.add(AvgPer(date=date, value=avg_per))

        # insert yieldgap
        mi_item = session.query(YieldGap).filter(YieldGap.date == date).first()
        logger.info(f'Query result : {mi_item}')
        if mi_item:
            setattr(mi_item, 'value', yield_gap)
        else:
            session.add(YieldGap(date=date, value=yield_gap))

        session.commit()
