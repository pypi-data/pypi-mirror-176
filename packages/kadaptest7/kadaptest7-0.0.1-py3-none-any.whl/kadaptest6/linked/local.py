import requests
import logging

"""
지자체별사고 다발 지역
"""
class Local :    
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

        self.url = "https://taas.koroad.or.kr/data/rest/koroadkatech/frequentzone/lg?authKey="
        # self.key = False
        # self.servicekey = "z9r7XSQtQg0%2FQbEzkbq4J1Bzrh%2BLWGbKvKgIV2vlAD260pgFk%2BlWO5lmwDFi%2Bzce"

        # 시, 군, 구 코드 변수에 저장
        response = requests.get("https://raw.githubusercontent.com/kr-juso/administrationCode/main/administrationCode.tsv")
        self.results = response.content.decode('utf-8').split("\n")[1:-1]

    def yearCodes(self) :
        yearStrs = ["17년도", "18년도", "19년도", "20년도"]
        searchYearCodes = ["2018074", "2019056", "2020087", "2021056"]
      
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
        json_index = ["items", "item"]
        param = {'searchYearCd': yearCode, 'sido': cityCode[:2], 'guGun': cityCode[2:], 'type': 'json'}
        response = requests.get(self.url+servicekey, params=param)

        if not response.ok :
            return print("ERROR: Response not OK")
        
        print("Response ok")

        items = response.json()

        for index in json_index :
            items = items[index]

        return items
