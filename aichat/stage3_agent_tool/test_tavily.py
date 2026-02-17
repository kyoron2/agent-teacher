from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

load_dotenv()

# 检查 API Key 是否存在
api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    print("❌ 错误：未找到 TAVILY_API_KEY")
    print("请在 .env 文件中添加：TAVILY_API_KEY=你的密钥")
else:
    print(f"✅ 找到 API Key: {api_key[:10]}...")
    
    # 测试搜索
    try:
        search = TavilySearchResults(max_results=2)
        result = search.invoke("Python 最新版本")
        print("\n✅ 搜索成功！")
        print(f"结果数量: {len(result)}")
        print(f"第一条结果: {result[0]}")
    except Exception as e:
        print(f"\n❌ 搜索失败: {e}")