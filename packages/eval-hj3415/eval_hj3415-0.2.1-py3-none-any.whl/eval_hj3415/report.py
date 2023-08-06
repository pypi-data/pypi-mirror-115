"""다양한 문자열 출력 형식에 맞춘 함수들
"""

import pandas as pd
import time
from multiprocessing import Process, cpu_count, Queue
from db_hj3415 import mongo, setting
from .eval import red as eval_red, mil as eval_mil, blue as eval_blue, growth as eval_growth
from .score import red as score_red, mil as score_mil, blue as score_blue, growth as score_growth
from .db import CorpsEval
from util_hj3415 import utils
from krx_hj3415 import krx
import textwrap

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)

###########################################################################


def _make_df_part(codes: list, q):
    def make_record(c: str) -> dict:
        # 장고에서 사용할 eval 테이블을 만들기 위해 각각의 레코드를 구성하는 함수
        c101 = mongo.C101(code=c).get_recent()

        red = eval_red(code=c)
        mil = eval_mil(code=c)
        growth = eval_growth(code=c)

        mil_date = mil['date']
        red_date = red['date']
        growth_date = growth['date']

        return {
            'code': c101['코드'],
            '종목명': c101['종목명'],
            '주가': utils.to_int(c101['주가']),
            'PER': utils.to_float(c101['PER']),
            'PBR': utils.to_float(c101['PBR']),
            '시가총액': utils.to_float(c101['시가총액']),
            'RED': utils.to_int(red['red_price']),
            '주주수익률': utils.to_float(mil['주주수익률']),
            '이익지표': utils.to_float(mil['이익지표']),
            'ROIC': utils.to_float(mil['투자수익률']['ROIC']),
            'ROE': utils.to_float(mil['투자수익률']['ROE']),
            'PFCF': utils.to_float(CorpsEval.get_recent(mil['가치지표']['PFCF'])[1]),
            'PCR': utils.to_float(CorpsEval.get_recent(mil['가치지표']['PCR'])[1]),
            '매출액증가율': utils.to_float(growth['매출액증가율'][0]),
            'date': list(set(mil_date + red_date + growth_date))
        }

    t = len(codes)
    d = []
    for i, code in enumerate(codes):
        print(f'{i+1}/{t} {code}')
        try:
            d.append(make_record(code))
        except:
            logger.error(f'error on {code}')
            continue
    df = pd.DataFrame(d)
    logger.info(df)
    q.put(df)


def make_eval_df_all() -> pd.DataFrame:
    def _code_divider(entire_codes: list) -> tuple:
        # 전체 종목코드를 리스트로 넣으면 cpu 코어에 맞춰 나눠준다.
        # reference from https://stackoverflow.com/questions/19086106/how-to-utilize-all-cores-with-python-multiprocessing
        def _split_list(alist, wanted_parts=1):
            # 멀티프로세싱할 갯수로 리스트를 나눈다.
            # reference from https://www.it-swarm.dev/ko/python/%EB%8D%94-%EC%9E%91%EC%9D%80-%EB%AA%A9%EB%A1%9D%EC%9C%BC%EB%A1%9C-%EB%B6%84%ED%95%A0-%EB%B0%98%EC%9C%BC%EB%A1%9C-%EB%B6%84%ED%95%A0/957910776/
            length = len(alist)
            return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                    for i in range(wanted_parts)]

        core = cpu_count()
        print(f'Get number of core for multiprocessing : {core}')
        n = core - 1
        if len(entire_codes) < n:
            n = len(entire_codes)
        print(f'Split total {len(entire_codes)} codes by {n} parts ...')
        divided_list = _split_list(entire_codes, wanted_parts=n)
        return n, divided_list

    print(setting.load())
    codes = mongo.Corps.get_all_corps()

    print('*' * 25, f"Eval all using multiprocess", '*' * 25)
    print(f'Total {len(codes)} items..')
    logger.info(codes)
    n, divided_list = _code_divider(codes)

    start_time = time.time()
    q = Queue()
    ths = []
    for i in range(n):
        ths.append(Process(target=_make_df_part, args=(divided_list[i], q)))
    for i in range(n):
        ths[i].start()
    df_list = []
    for i in range(n):
        df_list.append(q.get())
    # 부분데이터프레임들을 하나로 합침
    final_df = pd.concat(df_list, ignore_index=True)
    for i in range(n):
        ths[i].join()
    print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')
    logger.debug(final_df)
    return final_df


def yield_valid_spac() -> tuple:
    """
    전체 스팩주의 현재가를 평가하여 2000원 이하인 경우 yield한다.

    Returns:
        tuple: (code, name, price)
    """
    codes = mongo.Corps.get_all_corps()
    logger.info(f'len(codes) : {len(codes)}')
    print('<<< Finding valuable SPAC >>>')
    for i, code in enumerate(codes):
        name = krx.get_name(code)
        logger.info(f'code : {code} name : {name}')
        if '스팩' in str(name):
            logger.info(f'>>> spac - code : {code} name : {name}')
            price, _, _ = utils.get_price_now(code=code)
            if price <= 2000:
                logger.warning(f'현재가:{price}')
                print(f"code: {code} name: {name}, price: {price}")
                yield code, name, price


############################################################################

class MakeStr:
    
    separate_line = '\n' + ('-' * 65) + '\n'

    def __init__(self, code: str):
        self.code = code
        self.name = krx.get_name(code)

    def c101(self, full=True):
        c101 = mongo.C101(self.code).get_recent()
        logger.info(c101)

        title = '=' * 35 + f"\t{c101['코드']}\t\t{c101['종목명']}\t\t{c101['업종']}\t" + '=' * 35
        intro = textwrap.fill(f"{c101['intro']}", width=70)

        if full:
            price = (f"{c101['date']}\t\t"
                     f"주가: {utils.deco_num(c101['주가'])}원\t\t"
                     f"52주최고: {utils.deco_num(c101['최고52주'])}원\t"
                     f"52주최저: {utils.deco_num(c101['최저52주'])}원")
            info = (f"PER: {c101['PER']}\t\t"
                    f"PBR: {c101['PBR']}\t\t\t"
                    f"배당수익률: {c101['배당수익률']}%\t\t"
                    f"시가총액: {utils.get_kor_amount(utils.to_int(c101['시가총액']), omit='억')}\n"
                    f"업종PER: {c101['업종PER']}\t"
                    f"유통비율: {c101['유통비율']}%\t\t"
                    f"거래대금: {utils.to_억(c101['거래대금'])}원\t\t"
                    f"발행주식: {utils.to_만(c101['발행주식'])}주")
        else:
            price = (f"<< {c101['date']} >>\n"
                     f"주가: {utils.deco_num(c101['주가'])}원")
            info = (f"PER: {c101['PER']}\n"
                    f"업종PER: {c101['업종PER']}\n"
                    f"PBR: {c101['PBR']}\n"
                    f"배당수익률: {c101['배당수익률']}%\n"
                    f"유통비율: {c101['유통비율']}%\n"
                    f"발행주식: {utils.to_만(c101['발행주식'])}주\n"
                    f"시가총액: {utils.get_kor_amount(utils.to_int(c101['시가총액']), omit='억')}")

        return title + '\n' + intro + self.separate_line + price + '\n' + info

    def red(self, full=True) -> str:
        red_dict = eval_red(self.code)
        p, 괴리율 = score_red(self.code)
        logger.info(red_dict)

        title = f"Red\tPoint({p})\t괴리율({괴리율}%)\t{red_dict['date']}\n"
        if full:
            contents = (f"사업가치({utils.deco_num(red_dict['사업가치'])}억) "
                        f"+ 재산가치({utils.deco_num(red_dict['재산가치'])}억) "
                        f"- 부채({utils.deco_num(red_dict['부채평가'])}억) "
                        f"/ 발행주식({utils.to_만(red_dict['발행주식수'])}주) "
                        f"= {utils.deco_num(red_dict['red_price'])}원")
        else:
            contents = f"{utils.deco_num(red_dict['red_price'])}원"
        return title + contents

    def mil(self, full=True) -> str:
        mil_dict = eval_mil(self.code)
        p1, p2, p3, p4 = score_mil(self.code)
        logger.info(mil_dict)

        title = f"Millenial\tPoint({p1+p2+p3+p4})\t{mil_dict['date']}\n"
        if full:
            contents = (f"1. 주주수익률({p1}): {mil_dict['주주수익률']} %\n"
                        f"2. 이익지표({p2}): {mil_dict['이익지표']}\n"
                        f"3. 투자수익률({p3}): ROIC 4분기합: {mil_dict['투자수익률']['ROIC']}%, 최근 ROE: {mil_dict['투자수익률']['ROE']}%\n"
                        f"4. 가치지표\n"
                        f"\tFCF: {mil_dict['가치지표']['FCF']}\n"
                        f"\tPFCF({p4}) : {mil_dict['가치지표']['PFCF']}\n"
                        f"\tPCR: {mil_dict['가치지표']['PCR']}")
        else:
            contents = (f"1. 주주수익률({p1}): {mil_dict['주주수익률']} %\n"
                        f"2. 이익지표({p2}): {mil_dict['이익지표']}\n"
                        f"3. 투자수익률({p3}): ROIC 4분기합: {mil_dict['투자수익률']['ROIC']}%, 최근 ROE: {mil_dict['투자수익률']['ROE']}%\n"
                        f"4. 가치지표\tPFCF({p4}) : {CorpsEval.get_recent(mil_dict['가치지표']['PFCF'])}")
        return title + contents

    def blue(self, full=True) -> str:
        blue_dict = eval_blue(self.code)
        p1, p2, p3, p4, p5 = score_blue(self.code)
        logger.info(blue_dict)

        title = f"Blue\tPoint({p1+p2+p3+p4+p5})\t{blue_dict['date']}\n"
        if full:
            contents = (f"1. 유동비율({p1}): {blue_dict['유동비율']}(100이하 위험)\n"
                        f"2. 이자보상배율({p2}): {blue_dict['이자보상배율']}(1이하 위험 5이상 양호)\n"
                        f"3. 순부채비율({p3}): {blue_dict['순부채비율']}(30이상 not good)\n"
                        f"4. 순운전자본회전율({p4}): {blue_dict['순운전자본회전율']}\n"
                        f"5. 재고자산회전율({p5}): {blue_dict['재고자산회전율']}")

        else:
            contents = ''
        return title + contents

    def growth(self, full=True) -> str:
        growth_dict = eval_growth(self.code)
        p1, p2 = score_growth(self.code)
        logger.info(growth_dict)

        title = f"Growth\tPoint({p1 + p2})\t{growth_dict['date']}\n"
        if full:
            contents = (f"1. 매출액증가율({p1}): {growth_dict['매출액증가율']}\n"
                        f"2. 영업이익률({p2}): {growth_dict['영업이익률']}")
        else:
            contents = (f"1. 매출액증가율({p1}): {growth_dict['매출액증가율'][0]}\n"
                        f"2. 영업이익률({p2}): {growth_dict['영업이익률'].get(self.name)}")
        return title + contents

    def c108(self, full=True) -> str:
        if full:
            c108_list = mongo.C108(self.code).get_all()
        else:
            c108_list = mongo.C108(self.code).get_recent()
        s = ''
        logger.info(c108_list)
        for i, c108_dict in enumerate(c108_list):
            logger.info(c108_dict)
            if i == 0:
                pass
            else:
                s += '\n'
            header = f"{c108_dict['날짜']}\thprice : {c108_dict['목표가']} 원\n"
            title = f"<<{c108_dict['제목']}>>\n"
            contents = ''
            for line in c108_dict['내용'].split('▶'):
                contents += line.strip()
            s += header + title + textwrap.fill(contents, width=70) + self.separate_line
        return s


def for_console(code: str) -> str:
    make_str = MakeStr(code=code)

    return (make_str.c101() + make_str.separate_line
            + make_str.red() + make_str.separate_line
            + make_str.mil() + make_str.separate_line
            + make_str.blue() + make_str.separate_line
            + make_str.growth() + make_str.separate_line
            + make_str.c108())


def for_telegram(code: str) -> str:
    make_str = MakeStr(code=code)

    return (make_str.c101(full=False) + make_str.separate_line
            + make_str.red(full=False) + make_str.separate_line
            + make_str.mil(full=False) + make_str.separate_line
            + make_str.blue(full=False) + make_str.separate_line
            + make_str.growth(full=False) + make_str.separate_line
            + make_str.c108(full=False))


def for_django(code: str) -> dict:
    """ 장고에서 report 페이지에서 사용될 eval data 를 반환

    장고의 view context는 딕셔너리 형식이기 때문에 딕셔너리 모음으로 반환한다.
    """
    return {
        'c101': mongo.C101(code).get_recent(),
        'red': eval_red(code),
        'mil': eval_mil(code),
        'blue': eval_blue(code),
        'growth': eval_growth(code),
        'c108': mongo.C108(code).get_recent(),
        'red_s': score_red(code),
        'mil_s': score_mil(code),
        'blue_s': score_blue(code),
        'growth_s': score_growth(code),
    }
