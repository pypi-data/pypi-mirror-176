import requests
import logging

"""
어린이사고 다발 지역
"""
class Child :    
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

        self.url = "https://taas.koroad.or.kr/data/rest/koroadkatech/frequentzone/child?authKey="
        # self.servicekey = "LIzNZ7N0GlszFwqmWoeI4CH9sBouiO6dXdtpA7%2BT2tBXDH2exgahPT%2BWV1HxWq2j"

        # 시, 군, 구 코드 변수에 저장
        response = requests.get("https://raw.githubusercontent.com/kr-juso/administrationCode/main/administrationCode.tsv")
        self.results = response.content.decode('utf-8').split("\n")[1:-1]

    def yearCodes(self) :
        yearStrs = ["12년도", "13년도", "14년도", "15년도", "16년도", "17년도", "18년도", "19년도", "20년도"]
        searchYearCodes = ["2013097", "2014110", "2015049", "2016044", "2017027", "2018028", "2019035", "2020016", "2021017"]
      
        result = {key: value for key, value in zip(yearStrs, searchYearCodes)}

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
