from pandas.io.json import json_normalize

import pandas as pd
import requests
import logging

"""
자전거 사고 다발 지역
"""
class Bicycle :    
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

        self.url = "https://taas.koroad.or.kr/data/rest/koroadkatech/frequentzone/bicycle?authKey="
        self.key = False
        # self.servicekey = "uksm5YcI4llc5U2xnKy7bIxbUEbEvAwISBrPnG1udflarvxq59YY%2FXYQ1J3lYHcd"

        # 시, 군, 구 코드 변수에 저장
        response = requests.get("https://raw.githubusercontent.com/kr-juso/administrationCode/main/administrationCode.tsv")
        self.results = response.content.decode('utf-8').split("\n")[1:-1]

    def setServicekey(self, servicekey) :
        """
        - servicekey 저장 함수 // 최초 저장 시 사용하며, 저장된 키를 사용하여 getData() 함수 호출
        - servicekey: 도로교통공단 서비스 api 키 문자열
        """

        if self.key :
            return f"Your key is alreay exist : [ {servicekey} ]"

        self.servicekey = servicekey
        self.key = True

        return f"Your key is set to [ {servicekey} ]"

    def changeServicekey(self, servicekey) :
        """
        - 저장된 servicekey 변경을 위한 함수
        - 기 저장된 key가 없으면, 입력된 key 값을 저장
        - 기 저장된 key가 있으면, 입력된 key 값으로 덮어씀
        """

        self.servicekey = servicekey

        if self.key :
            return f"Your key is changed to [ {servicekey} ]"
        else :
            self.key = True
            return f"Your key is set to [ {servicekey} ]"


    def getSearchYearCodes(self) :
        """
        자전거 사고 다발 지역 호출을 위한 년도 코드
        딕셔너리 형태로 리턴
        """

        yearStrs = ["~ 12년도", "13년도", "14년도", "15년도", "16년도", "17년도", "18년도", "19년도", "20년도 ~"]
        searchYearCodes = ["2013099", "2014109", "2015046", "2016147", "2017050", "2018032", "2019038", "2020037", "2021028"]
      
        result = {key: value for key, value in zip(yearStrs, searchYearCodes)}
        df = pd.DataFrame(result.items(), columns=['Year', 'Code'])
        df = df.style.hide_index()

        return df

    def getData(self, yearCode, cityCode, key=False) :
        """
        - API를 request 함수 통해서 호출 및 데이터 획득, pandas 포맷으로 출력
        """

        if not key :
            if self.key :
                return self.request(yearCode, cityCode, self.servicekey)
            else :
                return "Please input your API key first. Using [ setServicekey() ]"

        else :
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

        df = pd.concat([df, json_normalize(items)])

        return df