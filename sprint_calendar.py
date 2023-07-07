# pip install zimsoap
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from zimsoap.zimbra import Zimbra
from zimsoap.zobjects import AccountSelector, CalendarView, GetCalendarItemsRequest

# poll "Which of these topics interests you for the next dev-talk?" "Release process" "Frontend development" "User feedback" "Service deprecation" "How to build a computational service" "How to build a dynamic service" --anonymous --progress --votes=2


zimbra = Zimbra(
    url="https://zimbra.example.com/service/soap",
    username="user@example.com",
    password="mypassword",
)


user_email = "user@example.com"
account_selector = AccountSelector(account=user_email)
calendar_view = CalendarView(start_date="20230501T000000Z", end_date="20230601T000000Z")
request = GetCalendarItemsRequest(account=account_selector, view=calendar_view)
response = zimbra.calendar.GetCalendarItems(request)

for item in response.calendar_item:
    start_time = item.start_time
    end_time = item.end_time
    location = item.location
    print(f"Start Time: {start_time}, End Time: {end_time}, Location: {location}")


# Set up Zimbra connection
zimbra = Zimbra(
    url="https://zimbra.example.com/service/soap",
    username="user@example.com",
    password="mypassword",
)

# Define calendar view
start_date = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
end_date = start_date.replace(month=start_date.month + 1) - timedelta(days=1)
calendar_view = CalendarView(
    start_date=start_date.strftime("%Y%m%dT%H%M%SZ"),
    end_date=end_date.strftime("%Y%m%dT%H%M%SZ"),
)

# Get calendar items
user_email = "user@example.com"
account_selector = AccountSelector(account=user_email)
request = GetCalendarItemsRequest(account=account_selector, view=calendar_view)
response = zimbra.calendar.GetCalendarItems(request)

# Create a calendar heatmap
num_days = (end_date - start_date).days + 1
calendar = np.zeros((num_days,))
for item in response.calendar_item:
    start_time = datetime.strptime(item.start_time, "%Y%m%dT%H%M%SZ")
    end_time = datetime.strptime(item.end_time, "%Y%m%dT%H%M%SZ")
    location = item.location
    if start_time.date() != end_time.date():
        # Handle multi-day events by splitting them into multiple days
        num_days = (end_time.date() - start_time.date()).days + 1
        for i in range(num_days):
            day_index = (start_time.date() - start_date.date() + timedelta(days=i)).days
            if location == "office":
                calendar[day_index] = 1
    else:
        day_index = (start_time.date() - start_date.date()).days
        if location == "office":
            calendar[day_index] = 1

# Plot the calendar heatmap
fig, ax = plt.subplots(figsize=(8, 6))
ax.imshow(calendar.reshape(1, -1), cmap="coolwarm", aspect="auto")
ax.set_xticks(np.arange(num_days))
ax.set_xticklabels(
    [(start_date + timedelta(days=i)).strftime("%d") for i in range(num_days)]
)
ax.set_yticks([])
ax.set_title("User's Office Availability")

# Add avatars for days when the user is in the office
for i in range(num_days):
    if calendar[i] == 1:
        avatar = plt.imread("avatar.png")  # replace with path to your avatar image
        ax.imshow(
            avatar, extent=[i - 0.25, i + 0.25, -0.5, 0.5], aspect="auto", alpha=0.8
        )

plt.show()
