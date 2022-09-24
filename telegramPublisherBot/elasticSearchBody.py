body = {
    "settings" : { # 색인(index) 정의 
        "index": { # 색인 전체 설정
            "analysis": {
                "analyzer": {
                    "nori_analyzer": { # 사용자 정의 분석기
                        "type": "custom",
                        "tokenizer": "nori_user_dict", # 토크나이저 설정
                        "filter": ["my_posfilter"]
                    }
                },
                "tokenizer": {
                    "nori_user_dict": { # 토크나이저 정의
                        "type": "nori_tokenizer", # 한글 분석기 (nori)
                        "decompound_mode": "mixed", #토큰을 처리하는 방법, 분해하지 않는다(none), 분해하고 원본삭제(discard), 분해하고 원본 유지(mixed)
                        "user_dictionary": "userdict_ko.txt"
                    }
                },
                "filter": {
                    "my_posfilter": { #제거 할 불용어들
                        "type": "nori_part_of_speech",
                        "stoptags": [
                            "E", "IC","J","MAG", "MAJ", "MM",
                            "SP", "SSC", "SSO", "SC", "SE",
                            "XPN", "XSA", "XSN", "XSV",
                            "UNA", "NA", "VSV"
                        ]
                    }
                }
            }
        }
    },
    "mappings": {
        "doc":{
            "properties": {
                "id": {"type": "text"}, 
                "date": {"type":"date"}, 
                "title": {"type": "text", "analyzer": "nori_analyzer"}, 
                "content": {"type": "text", "analyzer": "nori_analyzer"}, 
                "mentioned":{"type": "boolean"}, 
                "forwards": {"type": "text"}, 
                "fwd_msg_channel": {"type": "text"}, 
                "fwd_msg_id": {"type": "text"}, 
                "fwd_msg_date": {"type": "date"}, 
            }
        }
    }
}