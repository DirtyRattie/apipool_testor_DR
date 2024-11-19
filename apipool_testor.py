import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_config(file_path):
    """
    加载JSON配置文件
    :param file_path: JSON文件路径
    :return: 配置内容的字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file {file_path} not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON configuration file {file_path}.")
        exit(1)


def test_api_model(api, model, system_prompt, user_prompt):
    """
    单独测试一个 API 和一个模型。
    :param api: Dict containing 'api_url' and 'api_key'
    :param model: Model name to test
    :param system_prompt: System prompt content
    :param user_prompt: User prompt content
    :return: Dict with the test result
    """
    api_url = api.get("api_url")
    api_key = api.get("api_key")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            reply_message = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No content")
            return {
                "api_url": api_url,
                "model": model,
                "status": "accessible",
                "message": reply_message.strip()
            }
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            return {
                "api_url": api_url,
                "model": model,
                "status": f"failed (status code: {response.status_code})",
                "error": error_message
            }
    except requests.exceptions.RequestException as e:
        return {
            "api_url": api_url,
            "model": model,
            "status": "error",
            "error": str(e)
        }


def test_apis_and_models(api_config, test_config):
    """
    并行测试多个 API 和多个模型。
    :param api_config: API配置内容
    :param test_config: 测试配置内容
    """
    results = []
    system_prompt = test_config["system_prompt"]
    user_prompt = test_config["user_prompt"]
    models = test_config["models"]

    with ThreadPoolExecutor() as executor:
        # 创建所有任务
        tasks = {
            executor.submit(test_api_model, api, model, system_prompt, user_prompt): (api, model)
            for api in api_config
            for model in models
        }
        for future in as_completed(tasks):
            results.append(future.result())

    # 整理输出结果
    print("\n--- Testing Results ---\n")
    grouped_results = {}
    for result in results:
        api_url = result["api_url"]
        if api_url not in grouped_results:
            grouped_results[api_url] = []
        grouped_results[api_url].append(result)

    # 输出结果为清晰的格式
    for api_url, models in grouped_results.items():
        print(f"API URL: {api_url}")
        for model_info in models:
            print(f"  - Model: {model_info['model']}")
            if model_info["status"] == "accessible":
                print(f"    Status: {model_info['status']}")
                print(f"    Reply: {model_info['message']}")
            else:
                print(f"    Status: {model_info['status']}")
                print(f"    Error: {model_info['error']}")
        print("\n")


if __name__ == "__main__":
    # 加载配置
    api_config = load_config("api_config.json")
    test_config = load_config("test_config.json")

    # 执行测试
    test_apis_and_models(api_config, test_config)
