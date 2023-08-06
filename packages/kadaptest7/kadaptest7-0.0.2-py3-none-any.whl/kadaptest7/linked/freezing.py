import pandas as pd
import requests
import logging

"""
결빙사고 다발 지역
"""
class Freezing :    
    def __init__(self, debug=False) :
        """
        - debug: True 이면 모든 로깅 메시지 출력, False 이면 에러 로깅 메시지 출력
        """

        self.logger = logging.getLogger("root")

        if debug :
            self.logger.setLevel(logging.INFO)
        else :
            self.logger.setLevel(logging.ERROR)

        formatter = logging.Formatter("[%(levelname)s] %(message)s")

        if len(self.logger.handlers) == 0 :
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        self.url = "https://taas.koroad.or.kr/data/rest/koroadkatech/frequentzone/freezing?authKey="
        # self.key = False
        # self.servicekey = "DXDfo7%2FDj%2B4FR%2FBraEENKroGzkV2LI60ozd%2FeJ3WhvYw1ERffpTu3c9Y9IT%2FmIvJ"

        # 시, 군, 구 코드 변수에 저장
        response = requests.get("https://raw.githubusercontent.com/kr-juso/administrationCode/main/administrationCode.tsv")
        self.results = response.content.decode('utf-8').split("\n")[1:-1]

    def yearCodes(self) :
        yearStrs = ["13~17년도", "14~18년도", "15~19년도", "16~20년도"]
        searchYearCodes = ["2018091", "2019079", "2020036", "2021029"]
      
        result = {key: value for key, value in zip(yearStrs, searchYearCodes)}
        # df = pd.DataFrame(result.items(), columns=['Year', 'Code'])
        # df = df.style.hide_index()
        # df = df.style.hide(axis='index')
        # df = df.to_json(force_ascii=False)

        return result

    def getData(self, yearCode, cityCode, key) :
        """
        - API를 request 함수 통해서 호출 및 데이터 획득, pandas 포맷으로 출력
        """
        return self.request(yearCode, cityCode, key)

    def request(self, yearCode, cityCode, servicekey) :
        """
        - 실질적으로 데이터를 받아오는 함수
        """

        df = pd.DataFrame()

        json_index = ["items", "item"]
        param = {'searchYearCd': yearCode, 'sido': cityCode[:2], 'guGun': cityCode[2:], 'type': 'json'}
        response = requests.get(self.url+servicekey, params=param)

        if not response.ok :
            return print("ERROR: Response not OK")
        
        print("Response ok")

        items = response.json()

        for index in json_index :
            items = items[index]

        # df = pd.concat([df, pd.json_normalize(items)])
        # df = df.to_json(force_ascii=False)

        return items
