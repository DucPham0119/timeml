import subprocess
import re
import tempfile
import os

def heideltime_process2(text):
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as f:
        f.write(text)
        f.flush()
        file_path = f.name

    root = os.path.dirname(os.path.abspath(__file__))
    # print(root)
    jar = os.path.join(root, 'de.unihd.dbs.heideltime.standalone.jar')
    conf = os.path.join(root, 'conf/config.props')
    
    cmd = [
        "java",
        "-Dfile.encoding=UTF-8",
        "-jar", jar, 
        "-l", "VIETNAMESE",
        "-t", "narratives",
        "-o", "timeml",
        "-c", conf,
        file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # return result.stdout.strip()
    s = result.stdout.strip()
    pattern = re.compile(r'<TimeML\b[^>]*>(.*?)</TimeML>', re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(s)
    out = matches[0].strip()
    return out

if __name__ == "__main__":
    s = heideltime_process2("Lớp tôi đá bóng vào thứ 2 hàng tuần .")
    print(s)