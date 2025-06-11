from datetime import datetime, timezone, timedelta

# Định nghĩa múi giờ Việt Nam (UTC+7)
vietnam_tz = timezone(timedelta(hours=7))

# Lấy thời gian hiện tại theo múi giờ Việt Nam
now = datetime.now(vietnam_tz)
# Tạo output như yêu cầu
output = {
    "timestamp": now.isoformat().replace('+00:00', 'Z'),
    "time_display": now.strftime('%H:%M')
}

print(output)
