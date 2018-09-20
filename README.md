##备忘
中文版对话(作为Remote服务器方式)，目前问题

- 使用rasa_core对话管理部分存在问题，实体提取还可以；
- 计划做分类器，根据用户输入转rasaBot、闲聊bot与其他功能性bot;
- ChatterBot尚未仔细研究

###使用产品
1. （对话管理）rasa_core==0.8.6，https://rasa.com/docs/core/0.8.6/
2. （意图识别）rasa-nlu==0.11.4，https://rasa.com/docs/nlu/0.11.4/
- （辅助，nlu语料编辑）rasa-nlu-trainer，https://github.com/RasaHQ/rasa-nlu-trainer
- （闲聊）chatterbot==0.8.7，https://github.com/gunthercox/ChatterBot 
- （辅助，chatterbot可视化）ChatterBotFlask，https://github.com/Fazalcs13/ChatterBotFlask
    
###目录结构

```
chatbot
├── README.md
├── gossip      【闲聊bot、flask可视化】
│   └──app.py      （ChatterBot主程序，中文语料库、单一logic_adapters）
├── main_bot    【RasaBot】
│   ├── bot.py                  （训练rasaBot模型的方法）
│   ├── data    
│   │   ├── dm_story.md                          （对话管理数据）
│   │   ├── nlu_data.json                        （nlu语料）
│   │   ├── nlu_data_ori.json                    （备份）
│   │   └── total_word_feature_extractor_zh.dat  （MITIE模型训练）
│   ├── dm_domain.yml        
│   ├── dm_domain_local.yml
│   ├── logs
│   ├── models                  （nlu、dialogue模型）
│   ├── nlu_model_config.json   （pipeline）
│   ├── out.log
│   ├── rasa_nlu
│   ├── requirements.txt        （环境要求）
│   ├── start.sh                （启动rasaBot整体）
│   └──  start_rasa_nlu.sh      （启动nlu解析）       
└── rasa_nlu_ui 【提高效率，rasa_nlu意图识别语料的可视化编辑】
```
###使用方法
- MainBot启动方法 

```
sh start.sh
```
- GossipBot启动方法

```
python3 app.py
```

- rasa_nlu_ui启动方法

```
npm start
```