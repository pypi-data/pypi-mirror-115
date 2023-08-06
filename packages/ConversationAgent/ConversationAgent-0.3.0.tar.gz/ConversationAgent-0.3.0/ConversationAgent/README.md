## 說明
不需資料庫之對話腳本代理。

- 透過"ConversationAgent.LibStage.gen_agent"方法來建置機器人
- 透過"ConversationAgent.to_bot"方式與機器人溝通
    - 該方法需要三個參數
        - agent代理物件: gen_agent 產生
        - text: 使用者輸入內容，字串內容
        - data: 過場資訊，預設使用`{}`空字典，第二次與之後溝通應該戴上 `to_bot` 回傳的資料。
    - 該方法會回傳機器人回應與過場資訊，下次溝通保留該過場資訊在進行溝通。
    
## Quick start
```
from ConversationAgent.LibStage import gen_agent
import ConversationAgent

bot = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__QA_STAGE__",
            "qa_threshold": 1,
            "says": {
                "sys_welcome": "歡迎句",
                "sys_refuse": "拒絕句",
                "sys_complete": "完成句"
            },
            "corpus": {
                "早安": "1",
                "午安": "2",
                "晚安": "3"
            },
            "__SAVED_NAME__": {
                "__QA_RESPOND__": "QA_r1",
                "__QA_RESPOND_THRESHOLD__": "QA_th",
                "__QA_RESPOND_QUESTION__": "QA_q1",
                "__QA_RESPOND_SCORE__": "QA_s1",
                "__RUNNING_CORPUS__": "QA_c1",
            },
            "DISSABLE_WELCOME": False
        }
    ]
}
print(f"\n" * 5)

agent = gen_agent(bot)
data = {}
reply_text, data = ConversationAgent.to_bot(agent, "哈囉", data)
print(f"reply_text: {reply_text}， ")
reply_text, data = ConversationAgent.to_bot(agent, "哈囉", data)
print(f"reply_text: {reply_text}， ")
reply_text, data = ConversationAgent.to_bot(agent, "早安", data)
print(f"reply_text: {reply_text}， ")
```

## Stage 種類
### RE_STAGE

RE_STAGE 採用`stage_type`為`__RE_STAGE__`，是用於最基礎的對話階段，由兩個主要結構構成：
1. says: 用來設定該階段的回應句，回應句有三種類型
   * 歡迎句: 第一次到該階段時，機器人會回應該句子。(可依需求關閉功能，`DISSABLE_WELCOME`設為`True`就關閉，預設為`False`。)
   * 拒絕句: 當沒有滿足抓取到所有`is_fits`部分所要求的變數時，機器人會回應該句子。
   * 完成句: 以上都完成時，機器人會回應該句子。(可透過`%%`包裹變數名稱，並以`空格`前後相隔後，調用該變數。)

2. is_fits: 透過`正規表達式(regular expression)`從使用者的輸入句子來抓取變數，該變數會儲存起來提供給`完成句`和 `SWITCH_STAGE`使用。


```
{
    "stage_type": "__RE_STAGE__",
    "says": {
        "sys_welcome": "歡迎句",
        "sys_refuse": "拒絕句",
        "sys_complete": "完成句 %%YOUSAYS%% " 
    },
    "is_fits": [
        [".*", "YOUSAYS"]
    ],
    "DISSABLE_WELCOME": False
}
```

### SWITCH_STAGE

SWITCH_STAGE 採用`stage_type`為`__LIB_SWITCH_STAGE__`，用於在`Agent`不同路線切換，主要結構是`stages_filter`。 stages_filter用來設定切換路線的條件，用`[]`可包含帶多種條件多路線，每一條件單位由`變數名稱`、`限定數值`和 `切換路線`三部分組成。

以下說明主要四種設置方式:
* 無條件設定:
    ```
    [
        ["*",True,"_新路線1_"]
    ]
    ```
* 單一條件設定:
    ```
    [
        ["_VAR_","VALUE1","_新路線1_"],
        ["_VAR_","VALUE2","_新路線2_"]
    ]
    ```
* 多條件設定:
    ```
    [
        [["_VAR1_","_VAR2_"],["VALUE1","VALUE2"],"_新路線1_"],
        [["_VAR1_","_VAR2_"],["VALUE3","VALUE4"],"_新路線2_"],
    ]
    ```
* 混合條件設定:
    ```
    [
        ["_VAR1_","VALUE1","_新路線1_"],
        [["_VAR1_","_VAR2_"],["VALUE3","VALUE4"],"_新路線2_"],
        ["*",True,"_新路線3_"]
    ]
    ```

**儲存變數方式是透過`RE_STAGE`的 `is_fits`來執行。

範例：
```
{
    "stage_type": "__LIB_SWITCH_STAGE__",
    "stages_filter": [
        ["VAR","我想要的數值","_成功路線_"],,
        ["*",True,"_失敗路線_"]
    ]

}
```

### QA_STAGE
QA_STAGE 採用`stage_type`為`__QA_STAGE__`，是通過`相似度`來決定回應的一種階段，主要有三個部分的組成。
1. says: 用來設定該階段的回應句，回應句有三種類型
   * 歡迎句: 第一次到該階段時，機器人會回應該句子。(可依需求關閉功能，`DISSABLE_WELCOME`設為`True`就關閉，預設為`False`。)
   * 拒絕句: 當相似分數低於`qa_threshold`時，機器人會回應該句子。(可依需求關閉功能，`__DISABLE_REFUSE__`設為`True`就關閉，預設為`False`。)
   * 完成句: 以上都完成時，機器人會回應該句子。(可透過`%%`包裹變數名稱，並以`空格`前後相隔後，調用該變數。)

2. corpus: 使用者的輸入會與該字典的所有`key`進行比對，並儲存相關結果，相關結果包含：
    * `__QA_RESPOND_QUESTION__`: 相似值最高的 key
    * `__QA_RESPOND__`: 相似值最高的 key 對應之 value
    * `__QA_RESPOND_SCORE__`: 相似值最高的數值
    * `__RUNNING_CORPUS__`: 該次測試時使用的 corpus
    * `__QA_RESPOND_THRESHOLD__`: 該次測試使用的 threshold
    
3. `__SAVED_NAME__`: 設定儲存之變數的名稱，方便使用。


```
 {
    "stage_type": "__QA_STAGE__",
    "qa_threshold": 1,
    "says": {
        "sys_welcome": "歡迎句",
        "sys_refuse": "拒絕句",
        "sys_complete": "完成句"
    },
    "corpus": {
        "早安": "1",
        "午安": "2",
        "晚安": "3"
    },
    "__SAVED_NAME__": {
        QAStage.__QA_RESPOND__: "QA_r1",
        QAStage.__QA_RESPOND_THRESHOLD__: "QA_th",
        QAStage.__QA_RESPOND_QUESTION__: "QA_q1",
        QAStage.__QA_RESPOND_SCORE__: "QA_s1",
        QAStage.__RUNNING_CORPUS__: "QA_c1",
    },
    "DISSABLE_WELCOME": False
}
```


## Example
### 購票系統範例 
```
from ConversationAgent.LibStage import gen_multi_agent, QAStage
import ConversationAgent
bot_json = {
  "__MAIN_STAGES__": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "請問是要做哪種票種呢？",
        "sys_reply_q2": "請說『月票』或是『單程票』",
        "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
      },
      "is_fits": [
        [
          "(月票|1280|長期票|定期票)+",
          "set_level"
        ],
        [
          "(單程票|單程|一次)+",
          "set_level"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "set_level",
          "月票",
          "_月票_"
        ],
        [
          "set_level",
          "1280",
          "_月票_"
        ],
        [
          "set_level",
          "長期票",
          "_月票_"
        ],
        [
          "set_level",
          "定期票",
          "_月票_"
        ],
        [
          "set_level",
          "單程票",
          "_單程票_"
        ],
        [
          "set_level",
          "單程",
          "_單程票_"
        ],
        [
          "set_level",
          "一次",
          "_單程票_"
        ]
      ]
    }
  ],
  "_月票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "月票的價格為 1280元，是否確認？",
        "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
        "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
      },
      "is_fits": [
        [
          "(是|好的|好|沒問題)+$",
          "user_status"
        ],
        [
          "(否|不|不行|不要|不好)+$",
          "user_status"
        ]
      ]
    }
  ],
  "_單程票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "",
        "sys_reply_q2": "",
        "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
      },
      "is_fits": [],
      "__DISSABLE_Q1__": True
    }
  ]
}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "月票"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "好"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")
```

### 購票+問答系統範例 
```
from ConversationAgent.LibStage import gen_multi_agent, QAStage
import ConversationAgent
bot_json = {
  "__MAIN_STAGES__": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "哈囉請問要做什麼？ 目前提供『問答』和『訂票』服務",
        "sys_reply_q2": "目前只提供『問答』和『訂票』服務喔",
        "sys_reply_complete": "好的，將開始 『 %%selected_service%% 』 "
      },
      "is_fits": [
        [
          "(問答|問題|詢問)+",
          "selected_service"
        ],
        [
          "(訂票|票價|買票)+",
          "selected_service"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "selected_service",
          "訂票",
          "_訂票_"
        ],
        [
          "selected_service",
          "買票",
          "_訂票_"
        ],
        [
          "selected_service",
          "票價",
          "_訂票_"
        ],
        [
          "selected_service",
          "問答",
          "_問答_"
        ],
        [
          "selected_service",
          "問題",
          "_問答_"
        ],
        [
          "selected_service",
          "詢問",
          "_問答_"
        ]
      ]
    }
  ],
  "_問答_": [
    {
      "stage_type": "__QA_STAGE__",
      "corpus": {
        "廁所在哪裡": "這裡沒有廁所",
        "詢問處在哪裡": "這裡沒有詢問處",
        "診所在哪裡": "這裡沒有診所",
      },
      "question": {
        "sys_reply_q1": "請問有什麼問題呢？",
        "sys_reply_q2": "",
        "sys_reply_complete": "我有 %%__QA_RESPOND_SCORE__%% 的信心覺得您要問：<br> \n        %%__QA_RESPOND_QUESTION__%% <br> \n        答案是 %%__QA_RESPOND__%% "
      },
      "is_fits": []
    }
  ],
  "_訂票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "請問是要做哪種票種呢？",
        "sys_reply_q2": "請說『月票』或是『單程票』",
        "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
      },
      "is_fits": [
        [
          "(月票|1280|長期票|定期票)+",
          "set_level"
        ],
        [
          "(單程票|單程|一次)+",
          "set_level"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "set_level",
          "月票",
          "_月票_"
        ],
        [
          "set_level",
          "1280",
          "_月票_"
        ],
        [
          "set_level",
          "長期票",
          "_月票_"
        ],
        [
          "set_level",
          "定期票",
          "_月票_"
        ],
        [
          "set_level",
          "單程票",
          "_單程票_"
        ],
        [
          "set_level",
          "單程",
          "_單程票_"
        ],
        [
          "set_level",
          "一次",
          "_單程票_"
        ]
      ]
    }
  ],
  "_月票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "月票的價格為 1280元，是否確認？",
        "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
        "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
      },
      "is_fits": [
        [
          "(是|好的|好|沒問題)+$",
          "user_status"
        ],
        [
          "(否|不|不行|不要|不好)+$",
          "user_status"
        ]
      ]
    }
  ],
  "_單程票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "",
        "sys_reply_q2": "",
        "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
      },
      "is_fits": [],
      "__DISSABLE_Q1__": True
    }
  ]
}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "我要月票"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "好"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")
```

### 如何客製化類別：以購票+問答系統為例子 
```
from ConversationAgent.LibStage import __LIB_STAGES__
from ConversationAgent.LibStage import QAStage
import requests


"""
##########
__NEW QAWorkerSTAGE__
##########
"""
__NEW_QUESTIONANSWER__ = "NEW_QUESTIONANSWER"
class QAWorkerSTAGE(QAStage):
    def __init__(self,data):
        super(QAWorkerSTAGE, self).__init__(data)
        self.similar_method = data.get(self.__SIMILAR_METHOD__, "worker_api")
        self.__NLPCORESERVER__ = "http://52.147.71.0:8000"

    def __request_similar_api__(self,text,corpus):
        res = requests.post(url=f"{self.__NLPCORESERVER__}/jobs/{self.similar_method}", json={
            "sentence": [
                text
            ],
            "corpus": corpus})
        return res.json()

# 增加自訂義的類別
__LIB_STAGES__[__NEW_QUESTIONANSWER__] = QAWorkerSTAGE

"""
##########
Bot
##########
"""        
bot_json = {
  "__MAIN_STAGES__": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "哈囉請問要做什麼？ 目前提供『問答』和『訂票』服務",
        "sys_reply_q2": "目前只提供『問答』和『訂票』服務喔",
        "sys_reply_complete": "好的，將開始 『 %%selected_service%% 』 "
      },
      "is_fits": [
        [
          "(問答|問題|詢問)+",
          "selected_service"
        ],
        [
          "(訂票|票價|買票)+",
          "selected_service"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "selected_service",
          "訂票",
          "_訂票_"
        ],
        [
          "selected_service",
          "買票",
          "_訂票_"
        ],
        [
          "selected_service",
          "票價",
          "_訂票_"
        ],
        [
          "selected_service",
          "問答",
          "_問答_"
        ],
        [
          "selected_service",
          "問題",
          "_問答_"
        ],
        [
          "selected_service",
          "詢問",
          "_問答_"
        ]
      ]
    }
  ],
  "_問答_": [
    {
      "stage_type": __NEW_QUESTIONANSWER__,
      "corpus": {
        "廁所在哪裡": "這裡沒有廁所",
        "詢問處在哪裡": "這裡沒有詢問處",
        "診所在哪裡": "這裡沒有診所",
      },
      "question": {
        "sys_reply_q1": "請問有什麼問題呢？",
        "sys_reply_q2": "",
        "sys_reply_complete": "我有 %%__QA_RESPOND_SCORE__%% 的信心覺得您要問：<br> \n        %%__QA_RESPOND_QUESTION__%% <br> \n        答案是 %%__QA_RESPOND__%% "
      },
      "is_fits": []
    }
  ],
  "_訂票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "請問是要做哪種票種呢？",
        "sys_reply_q2": "請說『月票』或是『單程票』",
        "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
      },
      "is_fits": [
        [
          "(月票|1280|長期票|定期票)+",
          "set_level"
        ],
        [
          "(單程票|單程|一次)+",
          "set_level"
        ]
      ]
    },
    {
      "stage_type": "Switch",
      "stages_filter": [
        [
          "set_level",
          "月票",
          "_月票_"
        ],
        [
          "set_level",
          "1280",
          "_月票_"
        ],
        [
          "set_level",
          "長期票",
          "_月票_"
        ],
        [
          "set_level",
          "定期票",
          "_月票_"
        ],
        [
          "set_level",
          "單程票",
          "_單程票_"
        ],
        [
          "set_level",
          "單程",
          "_單程票_"
        ],
        [
          "set_level",
          "一次",
          "_單程票_"
        ]
      ]
    }
  ],
  "_月票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "月票的價格為 1280元，是否確認？",
        "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
        "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
      },
      "is_fits": [
        [
          "(是|好的|好|沒問題)+$",
          "user_status"
        ],
        [
          "(否|不|不行|不要|不好)+$",
          "user_status"
        ]
      ]
    }
  ],
  "_單程票_": [
    {
      "stage_type": "__RE_STAGE__",
      "question": {
        "sys_reply_q1": "",
        "sys_reply_q2": "",
        "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
      },
      "is_fits": [],
      "__DISSABLE_Q1__": True
    }
  ]
}
data = {}
agent = gen_multi_agent(bot_json)



#
text = "hi"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "我有點問題"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "附近有廁所嗎"
reply_text, data = ConversationAgent.mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")
```

## ToDo

* Switch除了等號以外的方法
* DISSABLE_WELCOME測試與勘誤名詞
* Not Found Path時回應一個錯誤用的stage
* QAStage 停用拒絕句(無論分數都會通過)