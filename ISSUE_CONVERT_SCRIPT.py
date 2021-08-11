import pandas as pd
df3 = pd.read_csv("csvFilePath")
df3.fillna("", inplace=True)
columns_list = ["생성일", "우선순위", "이슈 키",'영향 받는 버전', '레이블','레이블.1', '레이블.2', "설명", "상태", "해결일", "보고자", "담당자"]

parents = ['테스트 단말', '테스트단말', '보호자']
child = ['J4+', 'A10e', 'a10e', 'A10E', 'j4+']
version = ['테스트 버전:', '테스트버전:', '테스트버전 :', '테스트 버전 :']
server = ['테스트 서버', '테스트서버']
pre = ['[사전 조건]','*[사전 조건]*', '[사전조건]', '*[사전조건]*' ]
envir = ['[테스트 환경]', '[테스트환경]', '[검증환경]', '[검증 환경]','*[테스트 환경]*', '*[테스트환경]*', '*[검증환경]*', '*[검증 환경]*']
route = ['재현 경로', '재현경로']
actual_result = ["[증상]"]
actual_result2 = ["증상:", "증상 :", "증상 : ", "증상\xa0"]
expected_result = ['기대 결과', '기대결과']

subset = df3.copy()[columns_list]

subset[["인입 경로", "부모 Model", "자녀 Model", "이슈 주체", "앱 서버", "사전 조건", "재현 경로", "증상", "기대 결과"]] = ""
subset.rename(columns = {"생성일": "인입 일", "우선순위": "중요도", "이슈 키" : "JIRA No.", "영향 받는 버전": "앱 버전", "레이블": "대분류", "레이블.1": "중분류",
                         "레이블.2": "소분류", "상태": "현상태", "해결일": "완료 일", "보고자": "QA 담당자", "담당자" : "개발 담당자"}, inplace=True)

subset = subset[["인입 일", "인입 경로", "중요도", "JIRA No.", "부모 Model", "자녀 Model", "이슈 주체", "앱 서버", "앱 버전", "대분류",
                 "중분류", "소분류", "사전 조건", "재현 경로", "증상", "기대 결과", "현상태", "완료 일", "QA 담당자", "개발 담당자", "설명"]]
explain = subset["설명"]


empty_ver = []
a=0
for i in range(len(subset)):
    if subset.at[i, "앱 버전"] == "":
        empty_ver.append(i)
    i=i+1
        
print("흠", empty_ver)
for i in range(explain.size):
    explain[i] =  explain[i].splitlines()
    for j in range(len(explain[i])):
        if any(text in explain[i][j] for text in child):
            ch_device = explain[i][j]
            ch_index = ch_device.find(':')+1
            ch_device = ch_device[ch_index:]
            subset.at[i, "자녀 Model"] = ch_device
        elif any(text in explain[i][j] for text in version):
            ver = explain[i][j]
            ver_index = ver.find(':')+1
            ver = ver[ver_index:]
            if empty_ver[a] == i:
                subset.at[i, "앱 버전"] = ver
                a = a+1
        elif any(text in explain[i][j] for text in server):
            ser = explain[i][j]
            ser_index = ser.find(':')+1
            ser = ser[ser_index:]
            subset.at[i, "앱 서버"] = ser
            
        
for i in range((explain.size)):
    for j in range(len(explain[i])):
        if any(text in explain[i][j] for text in pre):
            pre_condition = ""
            while j < len(explain[i]):
                j=j+1
                if any(text in explain[i][j] for text in route) or j == (len(explain[i])-1):
                    j=j-1
                    pre_condition = pre_condition.strip()
                    #pre_condition = pre_condition.replace("\n", "")
                    subset.at[i, "사전 조건"] = pre_condition
                    break
                else:
                    pre_condition = pre_condition + explain[i][j]
                    
                    
        elif any(text in explain[i][j] for text in route):
            a_route = ""
            while j < len(explain[i]):
                j=j+1
                if any(text in explain[i][j] for text in actual_result) or j == (len(explain[i])-1):
                    j=j-1
                    a_route = a_route.strip()
                    a_route = a_route.replace("\n\n", "\n")
                    subset.at[i, "재현 경로"] = a_route
                    #print("재현 경로 ", a_route)
                    break
                    
                else:
                    a_route = a_route + "\n" + explain[i][j]
                    
                    
        elif any(text in explain[i][j] for text in actual_result2):
            a_result = ""
            #title = explain[i][j]
            while j < len(explain[i]):
                if any(text in explain[i][j] for text in expected_result) or j == (len(explain[i])-1):
                    j=j-1
                    index = a_result.find(':')+1
                    a_result = a_result[index:]
                    a_result = a_result.strip()
                    a_result = a_result.replace("\n\n", "\n")
                    img_index = [k for k, value in enumerate(a_result) if value == "!"]
                    img_list = []
                    for k in range(len(img_index)):
                        if k%2 == 0:
                            num = k
                        else:
                            a_text = a_result[img_index[num]:(img_index[k]+1)]
                            img_list.append(a_text)
                            k = k+1
                    for l in range(len(img_list)):
                        a_result = a_result.replace(img_list[l], "")
                        l=l+1
                    subset.at[i, "증상"] = a_result
                    #print("증상 -- ", a_result)
                    break

                else:
                    a_result = a_result + "\n" + explain[i][j]
                    j=j+1
                    #print("a_result2 : ", a_result)
            
        elif any(text in explain[i][j] for text in expected_result):
            j=j+1
            e_result = ""
            while j < len(explain[i]):
                e_result = e_result + "\n" + explain[i][j]
                j=j+1
            e_result = e_result.strip()
            e_result = e_result.replace("\n", "")
            img_index = [k for k, value in enumerate(e_result) if value == "!"]
            img_list = []
            for k in range(len(img_index)):
                if k%2 == 0:
                    num = k
                else:
                    e_text = e_result[img_index[num]:(img_index[k]+1)]
                    img_list.append(e_text)
                    k = k+1
            for l in range(len(img_list)):
                e_result = e_result.replace(img_list[l], "")
                l=l+1
            subset.at[i, "기대 결과"] = e_result
            #print("기대 결과 ", e_result)
        else:
            continue

                
subset.to_csv("csvFilePath", encoding="utf-8-sig")
            
