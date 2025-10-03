# import subprocess
# from typing import Dict, Any
#
# # from dp_module import run_dependency_parsing  # giả sử bạn đã có module DP riêng
#
# def run_heideltime(text: str) -> str:
#     """Gọi HeidelTime qua subprocess"""
#     result = subprocess.run(
#         ["java", "-jar", "heideltime/heideltime.jar", "-text", text, "-l", "VIETNAMESE"],
#         capture_output=True,
#         text=True
#     )
#     return result.stdout
#
# def extract_time(text: str) -> dict[str, str | Any]:
#     # 1. chạy dependency parsing trước
#     # dp_result = run_dependency_parsing(text)
#
#     # 2. chạy HeidelTime trên text hoặc output đã chuẩn hóa từ DP
#     ht_result = run_heideltime(text)
#
#     # 3. kết hợp (tùy bạn định nghĩa: ví dụ gộp JSON)
#     return {
#         "dp": dp_result,
#         "heideltime": ht_result
#     }
