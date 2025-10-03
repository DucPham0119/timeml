import numpy as np
from get_vecto import get_embed_average

class_name = {
    "I_ACTION": ["thử", "thử nghiệm", "gợi ý", "đề xuất", "hoãn", "cố gắng", "nỗ lực", "điều tra", "xem xét", "tránh",
                 "hủy bỏ", "ra lệnh", "ra quyết định", "yêu cầu", "kêu gọi", "hứa", "thề", "bổ nhiệm", "định",
                 "quyết định", "tìm cách", "thực hiện", "triển khai", "tiến hành", "áp dụng", "thi hành", "cam kết",
                 "phấn đấu", "tuyên thệ", "ra tay", "bắt tay", "lên kế hoạch", "dự định", "chuẩn bị", "lập kế hoạch",
                 "xúc tiến", "chủ trương", "đặt mục tiêu", "vạch ra", "thành lập ban", "soạn thảo", "ban hành",
                 "đưa ra biện pháp", "phát động", "chỉ đạo"],
    "REPORTING": ["nói", "trình bày", "phát biểu", "kể", "cho biết", "chia sẻ", "thông báo", "báo cáo", "giải thích",
                  "công bố", "tuyên bố", "công khai", "xác nhận", "thú nhận", "mô tả", "thuật lại", "phản ánh",
                  "bày tỏ", "nhấn mạnh", "khẳng định", "cảnh báo", "giới thiệu", "công nhận", "phủ nhận", "truyền đạt",
                  "thông tin", "đưa tin", "viết", "nêu rõ", "công luận", "chỉ ra", "tường thuật", "giải trình",
                  "trình bày quan điểm", "bộc bạch", "phát ngôn", "công kích", "bình luận", "nhận định",
                  "kêu gọi báo chí"],
    "PERCEPTION": ["nhìn", "nhìn thấy", "trông thấy", "ngó", "xem", "xem xét", "quan sát", "nhận ra", "phát hiện",
                   "chứng kiến", "theo dõi", "cảm nhận", "nhận biết", "cảm giác", "nghe", "nghe thấy", "lắng nghe",
                   "nghe trộm", "nghe lỏm", "chiêm ngưỡng", "ngửi", "nếm", "trải nghiệm", "nhìn nhận", "soi xét",
                   "cảm thụ", "bắt gặp", "nghe ngóng", "cảm thấy", "ngộ ra", "quan niệm", "tiếp nhận", "thấu hiểu",
                   "nhìn vào", "cảm hóa", "chạm vào"],
    "ASPECTUAL": ["bắt đầu", "khởi đầu", "khởi động", "khởi xướng", "cài đặt", "mở màn", "khai trương", "khai mạc",
                  "bắt tay vào", "dừng", "ngừng", "chấm dứt", "kết thúc", "hoàn tất", "đóng lại", "tạm ngưng",
                  "hoãn lại", "tiếp tục", "tái khởi động", "tái diễn", "kéo dài", "dừng lại", "kết thúc hẳn",
                  "chuyển sang", "chuyển tiếp", "gia hạn", "trì hoãn", "mở ra", "khép lại", "khôi phục", "tiếp diễn",
                  "tiến triển", "diễn ra", "trôi qua", "thực hiện lại"],
    "I_STATE": ["nghĩ", "cho rằng", "tưởng", "cảm thấy", "hy vọng", "ước", "mong", "mong chờ", "trông đợi", "háo hức",
                "khao khát", "mong muốn", "muốn", "cần", "thích", "ưa thích", "ưa chuộng", "sợ", "lo lắng", "băn khoăn",
                "bối rối", "hoài nghi", "tin", "tin rằng", "tin tưởng", "tin chắc", "tin cậy", "đoán", "nghĩ rằng",
                "dự đoán", "suy nghĩ", "tưởng tượng", "hình dung", "khẳng định trong lòng", "tự tin", "tin vào",
                "ngờ vực", "ngại", "do dự", "lạc quan", "bi quan", "ngờ ngợ", "bối rối", "ngạc nhiên", "tò mò",
                "cảm kích", "biết ơn", "căm ghét"],
    "STATE": ["sống", "chết", "tồn tại", "hiện hữu", "ở", "là", "còn", "hết", "ổn định", "bền vững", "khỏe", "mạnh",
              "yếu", "ốm", "bệnh", "yên tĩnh", "ổn thoả", "giàu", "nghèo", "sẵn sàng", "ổn định", "căng thẳng",
              "an toàn", "yên ổn", "hạnh phúc", "đau khổ", "già nua", "trẻ trung", "khỏe mạnh", "ốm yếu", "bền bỉ",
              "kiên cố", "thường trực", "cố định", "tạm thời", "bấp bênh", "ổn định lâu dài", "khủng hoảng", "ổn thỏa",
              "trường tồn"],
    "OCCURRENCE": ["đi", "tới", "đến", "đi", "ra", "xuất hiện", "diễn ra", "xảy ra", "hình thành", "phát sinh", "phát triển",
                   "nảy sinh", "trỗi dậy", "bùng nổ", "bùng phát", "leo thang", "nổ ra", "diễn biến", "tăng", "giảm",
                   "rơi", "sập", "mất", "gặp", "chiến đấu", "giành", "đạt được", "giành được", "chiếm", "thu được",
                   "bầu chọn", "chọn", "tham gia", "xây dựng", "lập nên", "thành lập", "hình thành", "khởi phát",
                   "tái diễn", "nảy nở", "tồn tại", "biến mất", "lắng xuống", "chìm", "vỡ", "tan rã", "giải tán",
                   "bùng cháy", "bốc cháy", "tràn lan", "lan rộng", "rộ lên", "tái bùng phát", "trỗi dậy mạnh mẽ"]}

# tính vector trung bình cho từng class
# class_labels = list(class_name.keys())
# class_centroids = get_embed_average(list(class_name.values()))
#
# # lưu ra file
# np.save("class_centroids.npy", class_centroids)
# with open("class_labels.txt", "w", encoding="utf-8") as f:
#     for label in class_labels:
#         f.write(label + "\n")
