import requests

"""
도로교통공단 데이터 검색을 위한 도시, 군(구) 코드 검색
"""
class City :
    def __init__(self) :
        self.response = requests.get("https://raw.githubusercontent.com/kr-juso/administrationCode/main/administrationCode.tsv")
        self.results = self.response.content.decode('utf-8').split("\n")[1:-1]

    def cityCodes(self) :
        """
        - 도시 코드 매칭
        - cityDicts: {도시: 코드}
        """

        # df = pd.DataFrame()
        cityDicts = {}

        for result in self.results :
            data = result.split("\t")

            if data[2] :
                cityDicts[data[1]+", "+data[2]] = data[0][0:5]
    
        # df = pd.DataFrame(cityDicts.items(), columns=['City', 'Code'])
        # df = df.style.hide_index()
        # df = df.style.hide(axis='index')
        # df = df.to_json(force_ascii=False)

        return cityDicts
