import os
import openai

# 從環境變數讀取 API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    # 這裡使用 print 而非 raise RuntimeError，以避免腳本直接中斷 CI/CD
    print("警告: OPENAI_API_KEY 環境變數未設定。AI 生成功能將無法使用。")
    # 可以選擇在這裡 sys.exit(0) 或讓腳本繼續執行 (如果後面沒有其他依賴 API Key 的操作)
    # 為了 CI/CD 流程的順暢，這裡選擇不中斷，但會印出警告。

def run_prompt(prompt_path: str, output_path: str, model: str = "gpt-4-turbo-preview"):
    """
    根據 Prompt 範本呼叫 LLM 生成程式碼，並將結果寫入指定檔案。
    """
    if not openai.api_key:
        print(f"跳過生成 {output_path}: OPENAI_API_KEY 未設定。")
        return

    try:
        prompt = open(prompt_path, encoding="utf-8").read()
        print(f"正在從 {prompt_path} 生成程式碼...")
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful code generator."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.2
        )
        code = resp.choices[0].message.content
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"✅ 已成功生成並寫入：{output_path}")
    except Exception as e:
        print(f"❌ 生成 {output_path} 時發生錯誤: {e}")

if __name__ == "__main__":
    # 專案根目錄的相對路徑
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

    # AI 生成 Django Product API 與測試骨架
    run_prompt(
      os.path.join(PROJECT_ROOT, "backend/prompts/api_scaffold_prompt.txt"),
      os.path.join(PROJECT_ROOT, "backend/django_order_app/views_product.py")
    )
    run_prompt(
      os.path.join(PROJECT_ROOT, "backend/prompts/test_case_prompt.txt"),
      os.path.join(PROJECT_ROOT, "backend/django_order_app/tests/test_product_api.py")
    )

    # AI 生成 React UserList 元件
    run_prompt(
      os.path.join(PROJECT_ROOT, "frontend-react/prompts/component_scaffold_prompt.txt"),
      os.path.join(PROJECT_ROOT, "frontend-react/src/components/UserList.tsx")
    )

    # AI 生成 Flutter Dashboard 螢幕
    run_prompt(
      os.path.join(PROJECT_ROOT, "flutter-app/prompts/screen_scaffold_prompt.txt"),
      os.path.join(PROJECT_ROOT, "flutter-app/lib/screens/dashboard_screen.dart")
    )
