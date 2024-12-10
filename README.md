## 说明

运行前需要申请deepseek或者chatglm的api key；建议申请glm的key(相对于deepseek速度更快)

创建glm 的api key：

```
https://bigmodel.cn/usercenter/proj-mgmt/apikeys
```

安装访问大模型的openai sdk

```
pip install --upgrade 'openai>=1.0'
```

安装依赖

```
pip install requests
pip install gradio
pip install beautifulsoup4
```


## 环境变量设置

1. Windows CMD 中临时设置：

```
set GLM_API_KEY=xxxx
```

2. Windows PowerShell 中临时设置：

```
$env:GLM_API_KEY="xxxxx"
```

3. Linux/Mac 中临时设置：

```
export GLM_API_KEY="xxxxx"
```