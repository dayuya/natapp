# natapp
natapp 用于内网穿透
- 直接下载脚本 运行 
- 第一次会提示 添加环境变量 `PUSH_PLUS_TOKEN`  `natapp_authtoken_web`
- PUSH_PLUS_TOKEN:微信plus的token
- natapp_authtoken_web：natapp的web隧道的token
#### win64 
- 拉取脚本
- 同级目录建立 `.env` 文件 ：脚本会将此文件内容添加到 环境变量
  - 格式 一个变量一行  PUSH_PLUS_TOKEN="11"

#### 其他
##### 参考文献
- 百度
- chatgpt
- [csdn 青龙面板使用cpolar实现内网穿透](https://blog.csdn.net/weixin_51863878/article/details/130719604?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522168489087816800217274228%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=168489087816800217274228&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-4-130719604-null-null.142^v87^control_2,239^v2^insert_chatgpt&utm_term=%E9%9D%92%E9%BE%99%E7%A9%BF%E9%80%8F&spm=1018.2226.3001.4187)
