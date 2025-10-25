import flet as ft
import calendar
import datetime

def main(page: ft.Page):
    page.title = "🖥 Productivity Dashboard + Calendar"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1100
    page.window.height = 750

    # --- Calendar Section ---
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month

    selected_day = ft.Text(f"Tanlangan sana: {today}")

    # Vazifalar ro‘yxati
    tasks = {}

    # Funksiya: Kalendar chizish
    def build_calendar(year, month):
        days = []
        month_calendar = calendar.monthcalendar(year, month)

        for week in month_calendar:
            row = []
            for day in week:
                if day == 0:
                    row.append(ft.Container(width=40, height=40))
                else:
                    bg = ft.Colors.BLUE_200 if (day == today.day and month == today.month and year == today.year) else ft.Colors.WHITE
                    btn = ft.ElevatedButton(
                        text=str(day),
                        width=40,
                        height=40,
                        style=ft.ButtonStyle(
                            bgcolor=bg,
                            shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=lambda e, d=day: select_day(d, month, year)
                    )
                    row.append(btn)
            days.append(ft.Row(row, alignment="center"))
        return ft.Column(days)

    # Sana tanlanganda
    def select_day(day, month, year):
        date = datetime.date(year, month, day)
        selected_day.value = f"Tanlangan sana: {date}"
        task_list.controls.clear()
        for t in tasks.get(str(date), []):
            task_list.controls.append(ft.Checkbox(label=t))
        page.update()

    # Oylar oralab yurish
    header = ft.Text(size=20, weight="bold")
    calendar_view = ft.Column()

    def update_calendar(year, month):
        header.value = f"{calendar.month_name[month]} {year}"
        calendar_view.controls.clear()
        calendar_view.controls.append(build_calendar(year, month))
        page.update()

    def prev_month(e):
        nonlocal current_month, current_year
        current_month -= 1
        if current_month < 1:
            current_month = 12
            current_year -= 1
        update_calendar(current_year, current_month)

    def next_month(e):
        nonlocal current_month, current_year
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
        update_calendar(current_year, current_month)

    # Vazifa qo‘shish
    task_input = ft.TextField(hint_text="Sana uchun vazifa yozing...", expand=True)
    task_list = ft.Column()

    def add_task(e):
        text = task_input.value.strip()
        if text:
            date_str = selected_day.value.replace("Tanlangan sana: ", "")
            tasks.setdefault(date_str, []).append(text)
            task_input.value = ""
            select_day(int(date_str.split("-")[2]), int(date_str.split("-")[1]), int(date_str.split("-")[0]))
            page.update()

    add_btn = ft.ElevatedButton("➕ Vazifa qo‘shish", on_click=add_task)

    # Layout
    page.add(
        ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=prev_month),
            header,
            ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=next_month)
        ], alignment="center"),
        calendar_view,
        selected_day,
        ft.Row([task_input, add_btn]),
        task_list
    )

    update_calendar(current_year, current_month)

ft.app(target=main)
