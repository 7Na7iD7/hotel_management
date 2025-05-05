import datetime
import json
import os
import re
from typing import Dict, List, Optional, Union
from colorama import init, Fore, Back, Style

init()


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu_title(title: str, width: int = 50):
    print("\n" + Fore.BLUE + "═" * width + Style.RESET_ALL)
    print(Fore.BLUE + f"{title.center(width)}" + Style.RESET_ALL)
    print(Fore.BLUE + "═" * width + Style.RESET_ALL + "\n")


def print_message(message: str, message_type: str = "info"):
    if message_type == "success":
        print(f"\n{Back.GREEN}{Fore.BLACK}✔️ {message}{Style.RESET_ALL}\n")
    elif message_type == "error":
        print(f"\n{Back.RED}{Fore.WHITE}⚠️ {message}{Style.RESET_ALL}\n")
    elif message_type == "warning":
        print(f"\n{Back.YELLOW}{Fore.BLACK}⚠️ {message}{Style.RESET_ALL}\n")
    else:
        print(f"\n{Back.BLUE}{Fore.WHITE}ℹ️ {message}{Style.RESET_ALL}\n")


def print_table(headers: List[str], rows: List[List[str]], widths: List[int], title: str = None,
                sortable: bool = False):
    if title:
        print_message(title, "info")
    total_width = sum(widths) + len(widths) * 3 + len(widths) - 1
    print(Fore.CYAN + "─" * total_width + Style.RESET_ALL)
    header_row = "│ "
    for header, width in zip(headers, widths):
        header_row += f"{header:<{width}} │ "
    print(Fore.CYAN + header_row.strip() + Style.RESET_ALL)
    print(Fore.CYAN + "─" * total_width + Style.RESET_ALL)
    for row in rows:
        row_str = "│ "
        for item, width in zip(row, widths):
            if "خالی" in str(item):
                row_str += f"{Fore.GREEN}{str(item):<{width}}{Style.RESET_ALL} │ "
            elif "اشغال شده" in str(item):
                row_str += f"{Fore.RED}{str(item):<{width}}{Style.RESET_ALL} │ "
            elif "رزرو شده" in str(item):
                row_str += f"{Fore.YELLOW}{str(item):<{width}}{Style.RESET_ALL} │ "
            else:
                row_str += f"{str(item):<{width}} │ "
        print(row_str.strip())
    print(Fore.CYAN + "─" * total_width + Style.RESET_ALL + "\n")
    if sortable:
        print(f"{Fore.YELLOW}برای مرتب‌سازی، ستون را انتخاب کنید (1-{len(headers)} یا 0 برای ادامه): {Style.RESET_ALL}",
              end="")
        return input()


def print_bar_chart(data: Dict[str, int], title: str, max_width: int = 30):
    print_message(title, "info")
    max_value = max(data.values()) or 1
    print(Fore.CYAN + "─" * 50 + Style.RESET_ALL)
    for key, value in data.items():
        bar_length = int((value / max_value) * max_width)
        bar = "█" * bar_length
        if key == "خالی":
            color = Fore.GREEN
        elif key == "رزرو شده":
            color = Fore.YELLOW
        else:
            color = Fore.RED
        print(f"{key:<10} | {color}{bar:<{max_width}}{Style.RESET_ALL} ({value})")
    print(Fore.CYAN + "─" * 50 + Style.RESET_ALL + "\n")


def print_timeline(income: float, start_date: str, end_date: str, max_width: int = 30):
    print_message(f"درآمد از {start_date} تا {end_date}", "info")
    print(Fore.CYAN + "─" * 50 + Style.RESET_ALL)
    bar = "⬆" * min(int(income / 1000000), max_width)
    print(f"درآمد: {Fore.GREEN}{bar:<{max_width}}{Style.RESET_ALL} ({income:,.0f} تومان)")
    print(Fore.CYAN + "─" * 50 + Style.RESET_ALL + "\n")


class Room:
    def __init__(self, room_id: str, room_type: str, price: float = 5000000, status: str = "خالی"):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.status = status
        self.current_guest_id = None

    def to_dict(self) -> Dict:
        return {
            "room_id": self.room_id,
            "room_type": self.room_type,
            "price": self.price,
            "status": self.status,
            "current_guest_id": self.current_guest_id
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Room':
        room = cls(
            room_id=data["room_id"],
            room_type=data["room_type"],
            price=data.get("price", 5000000),
            status=data["status"]
        )
        room.current_guest_id = data.get("current_guest_id")
        return room

    def __str__(self) -> str:
        return f"{self.room_id:<10} {self.room_type:<15} {self.price:,.0f} تومان {self.status:<10}"


class Guest:
    def __init__(self, guest_id: str, name: str, family: str, national_id: str, phone: str, address: str = ""):
        self.guest_id = guest_id
        self.name = name
        self.family = family
        self.national_id = national_id
        self.phone = phone
        self.address = address

    def to_dict(self) -> Dict:
        return {
            "guest_id": self.guest_id,
            "name": self.name,
            "family": self.family,
            "national_id": self.national_id,
            "phone": self.phone,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Guest':
        return cls(
            guest_id=data["guest_id"],
            name=data["name"],
            family=data.get("family", ""),
            national_id=data["national_id"],
            phone=data["phone"],
            address=data.get("address", "")
        )

    def __str__(self) -> str:
        return f"{self.guest_id:<10} {self.name:<15} {self.family:<15} {self.national_id:<12} {self.phone:<12}"


class Reservation:
    def __init__(self, reservation_id: str, guest_id: str, room_id: str,
                 check_in_date: str, check_out_date: str, status: str = "فعال"):
        self.reservation_id = reservation_id
        self.guest_id = guest_id
        self.room_id = room_id
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = status
        self.total_cost = 0.0

    def to_dict(self) -> Dict:
        return {
            "reservation_id": self.reservation_id,
            "guest_id": self.guest_id,
            "room_id": self.room_id,
            "check_in_date": self.check_in_date,
            "check_out_date": self.check_out_date,
            "status": self.status,
            "total_cost": self.total_cost
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Reservation':
        reservation = cls(
            reservation_id=data["reservation_id"],
            guest_id=data["guest_id"],
            room_id=data["room_id"],
            check_in_date=data["check_in_date"],
            check_out_date=data["check_out_date"],
            status=data["status"]
        )
        reservation.total_cost = data.get("total_cost", 0.0)
        return reservation

    def __str__(self) -> str:
        return (f"{self.reservation_id:<10} {self.guest_id:<10} {self.room_id:<10} "
                f"{self.check_in_date:<12} {self.check_out_date:<12} {self.status:<10} {self.total_cost:,.0f} تومان")


class HotelManagementSystem:
    def __init__(self):
        self.rooms: List[Room] = []
        self.guests: List[Guest] = []
        self.reservations: List[Reservation] = []
        self.next_room_id = 1
        self.next_guest_id = 1
        self.next_reservation_id = 1
        self.data_file = "hotel_data.json"
        self.load_data()

    def update_room_status(self) -> None:
        today = datetime.datetime.now().date()
        for room in self.rooms:
            if room.status in ["رزرو شده", "اشغال شده"]:
                reservations = self.get_room_reservations(room.room_id)
                expired = True
                for res in reservations:
                    try:
                        check_out = datetime.datetime.strptime(res.check_out_date, "%Y-%m-%d").date()
                        if check_out >= today and res.status == "فعال":
                            expired = False
                            break
                    except ValueError:
                        print_message(f"خطا در تاریخ رزرو {res.reservation_id}: فرمت تاریخ نامعتبر است!", "error")
                        continue
                if expired:
                    room.status = "خالی"
                    room.current_guest_id = None
                    for res in reservations:
                        if res.status == "فعال":
                            res.status = "منقضی شده"
        self.save_data()

    def save_data(self) -> None:
        data = {
            "rooms": [room.to_dict() for room in self.rooms],
            "guests": [guest.to_dict() for guest in self.guests],
            "reservations": [reservation.to_dict() for reservation in self.reservations],
            "next_room_id": self.next_room_id,
            "next_guest_id": self.next_guest_id,
            "next_reservation_id": self.next_reservation_id
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print_message("فایل داده‌ها با موفقیت ذخیره شد.", "success")  # برای دیباگ

    def load_data(self) -> None:
        if not os.path.exists(self.data_file):
            print_message("فایل داده‌ها یافت نشد، یک فایل جدید ایجاد می‌شود.", "info")
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.rooms = [Room.from_dict(room_data) for room_data in data.get("rooms", [])]
            self.guests = [Guest.from_dict(guest_data) for guest_data in data.get("guests", [])]
            self.reservations = [Reservation.from_dict(res_data) for res_data in data.get("reservations", [])]
            self.next_room_id = data.get("next_room_id", 1)
            self.next_guest_id = data.get("next_guest_id", 1)
            self.next_reservation_id = data.get("next_reservation_id", 1)
            self.update_room_status()
        except json.JSONDecodeError:
            print_message("فایل داده‌ها ساختار معتبر JSON ندارد!", "error")
        except KeyError as e:
            print_message(f"کلید {e} در فایل داده‌ها یافت نشد!", "error")
        except Exception as e:
            print_message(f"خطا در بارگذاری داده‌ها: {e}", "error")

    def add_room(self, room_type: str, price: float) -> Room:
        room_id = str(self.next_room_id)
        room = Room(room_id=room_id, room_type=room_type, price=price)
        self.rooms.append(room)
        self.next_room_id += 1
        self.save_data()
        return room

    def delete_room(self, room_id: str) -> bool:
        for reservation in self.reservations:
            if reservation.room_id == room_id and reservation.status == "فعال":
                return False
        for i, room in enumerate(self.rooms):
            if room.room_id == room_id:
                del self.rooms[i]
                self.save_data()
                return True
        return False

    def edit_room(self, room_id: str, room_type: Optional[str] = None,
                  price: Optional[float] = None, status: Optional[str] = None) -> bool:
        for room in self.rooms:
            if room.room_id == room_id:
                if room_type is not None:
                    room.room_type = room_type
                if price is not None:
                    room.price = price
                if status is not None:
                    room.status = status
                self.save_data()
                return True
        return False

    def get_room(self, room_id: str) -> Optional[Room]:
        for room in self.rooms:
            if room.room_id == room_id:
                return room
        return None

    def get_all_rooms(self) -> List[Room]:
        self.update_room_status()
        return self.rooms

    def get_available_rooms(self) -> List[Room]:
        self.update_room_status()
        return [room for room in self.rooms if room.status == "خالی"]

    def add_guest(self, name: str, family: str, national_id: str, phone: str, address: str = "") -> Guest:
        if not name.strip():
            raise ValueError("نام نمی‌تواند خالی باشد!")
        if not family.strip():
            raise ValueError("نام خانوادگی نمی‌تواند خالی باشد!")
        if not re.match(r"^\d{10}$", national_id):
            raise ValueError("کد ملی باید ۱۰ رقم باشد!")
        if not re.match(r"^09\d{9}$", phone):
            raise ValueError("شماره تلفن باید ۱۱ رقم و با 09 شروع شود!")

        guest_id = str(self.next_guest_id)
        guest = Guest(guest_id=guest_id, name=name.strip(), family=family.strip(),
                      national_id=national_id, phone=phone, address=address)
        self.guests.append(guest)
        self.next_guest_id += 1
        self.save_data()
        return guest

    def edit_guest(self, guest_id: str, name: Optional[str] = None, family: Optional[str] = None,
                   national_id: Optional[str] = None, phone: Optional[str] = None,
                   address: Optional[str] = None) -> bool:
        for guest in self.guests:
            if guest.guest_id == guest_id:
                if name is not None:
                    if not name.strip():
                        raise ValueError("نام نمی‌تواند خالی باشد!")
                    guest.name = name.strip()
                if family is not None:
                    if not family.strip():
                        raise ValueError("نام خانوادگی نمی‌تواند خالی باشد!")
                    guest.family = family.strip()
                if national_id is not None:
                    if not re.match(r"^\d{10}$", national_id):
                        raise ValueError("کد ملی باید ۱۰ رقم باشد!")
                    guest.national_id = national_id
                if phone is not None:
                    if not re.match(r"^09\d{9}$", phone):
                        raise ValueError("شماره تلفن باید ۱۱ رقم و با 09 شروع شود!")
                    guest.phone = phone
                if address is not None:
                    guest.address = address
                self.save_data()
                return True
        return False

    def delete_guest(self, guest_id: str) -> bool:
        for reservation in self.reservations:
            if reservation.guest_id == guest_id and reservation.status == "فعال":
                return False
        for i, guest in enumerate(self.guests):
            if guest.guest_id == guest_id:
                del self.guests[i]
                self.save_data()
                return True
        return False

    def get_guest(self, guest_id: str) -> Optional[Guest]:
        for guest in self.guests:
            if guest.guest_id == guest_id:
                return guest
        return None

    def get_all_guests(self) -> List[Guest]:
        return self.guests

    def search_guests(self, query: str) -> List[Guest]:
        query = query.lower()
        return [guest for guest in self.guests
                if query in guest.name.lower() or query in guest.national_id]

    def make_reservation(self, guest_id: str, room_id: str,
                         check_in_date: str, check_out_date: str) -> Optional[Reservation]:
        guest = self.get_guest(guest_id)
        room = self.get_room(room_id)

        if not guest:
            return None
        if not room:
            return None
        if room.status != "خالی":
            return None

        try:
            today = datetime.datetime.now()
            check_in = datetime.datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = datetime.datetime.strptime(check_out_date, "%Y-%m-%d")

            if check_in.date() < today.date():
                return None
            if check_out <= check_in:
                return None

            days = (check_out - check_in).days

            for reservation in self.get_room_reservations(room_id):
                if reservation.status != "فعال":
                    continue
                res_check_in = datetime.datetime.strptime(reservation.check_in_date, "%Y-%m-%d")
                res_check_out = datetime.datetime.strptime(reservation.check_out_date, "%Y-%m-%d")
                if not (check_out <= res_check_in or check_in >= res_check_out):
                    return None

            reservation_id = str(self.next_reservation_id)
            reservation = Reservation(
                reservation_id=reservation_id,
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            )

            reservation.total_cost = days * room.price
            room.status = "رزرو شده"

            self.reservations.append(reservation)
            self.next_reservation_id += 1
            self.save_data()
            return reservation
        except ValueError:
            return None

    def check_in(self, reservation_id: str) -> bool:
        reservation = self.get_reservation(reservation_id)
        if not reservation or reservation.status != "فعال":
            return False
        room = self.get_room(reservation.room_id)
        guest = self.get_guest(reservation.guest_id)
        if not room or not guest:
            return False

        try:
            check_in_date = datetime.datetime.strptime(reservation.check_in_date, "%Y-%m-%d")
            today = datetime.datetime.now()
            if today.date() < check_in_date.date():
                return False
        except ValueError:
            return False

        room.status = "اشغال شده"
        room.current_guest_id = reservation.guest_id
        self.save_data()
        return True

    def check_out(self, reservation_id: str) -> Union[float, bool]:
        reservation = self.get_reservation(reservation_id)
        if not reservation or reservation.status != "فعال":
            return False
        room = self.get_room(reservation.room_id)
        if not room:
            return False

        try:
            today = datetime.datetime.now()
            check_in = datetime.datetime.strptime(reservation.check_in_date, "%Y-%m-%d")
            check_out = today

            if check_out.date() < check_in.date():
                return False

            days = (check_out - check_in).days
            if days <= 0:
                days = 1

            final_cost = days * room.price
            reservation.total_cost = final_cost
            reservation.check_out_date = today.strftime("%Y-%m-%d")

            room.status = "خالی"
            room.current_guest_id = None
            reservation.status = "تسویه شده"
            self.save_data()
            return final_cost
        except ValueError:
            return False

    def cancel_reservation(self, reservation_id: str) -> bool:
        reservation = self.get_reservation(reservation_id)
        if not reservation or reservation.status != "فعال":
            return False
        room = self.get_room(reservation.room_id)
        if not room:
            return False

        room.status = "خالی"
        reservation.status = "لغو شده"
        self.save_data()
        return True

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def get_all_reservations(self) -> List[Reservation]:
        self.update_room_status()
        return self.reservations

    def get_active_reservations(self) -> List[Reservation]:
        self.update_room_status()
        return [reservation for reservation in self.reservations if reservation.status == "فعال"]

    def get_guest_reservations(self, guest_id: str) -> List[Reservation]:
        self.update_room_status()
        return [reservation for reservation in self.reservations if reservation.guest_id == guest_id]

    def get_room_reservations(self, room_id: str) -> List[Reservation]:
        return [reservation for reservation in self.reservations if reservation.room_id == room_id]

    def report_room_status(self) -> Dict[str, int]:
        self.update_room_status()
        status_count = {"خالی": 0, "رزرو شده": 0, "اشغال شده": 0}
        for room in self.rooms:
            if room.status in status_count:
                status_count[room.status] += 1
        return status_count

    def report_reservations_by_date(self, date: str) -> List[Reservation]:
        self.update_room_status()
        try:
            check_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            result = []

            for reservation in self.reservations:
                check_in = datetime.datetime.strptime(reservation.check_in_date, "%Y-%m-%d")
                check_out = datetime.datetime.strptime(reservation.check_out_date, "%Y-%m-%d")

                if check_in <= check_date < check_out and reservation.status == "فعال":
                    result.append(reservation)

            return result
        except ValueError:
            return []

    def report_income(self, start_date: str, end_date: str) -> float:
        try:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            if end < start:
                return 0.0

            total_income = 0.0

            for reservation in self.reservations:
                if reservation.status != "تسویه شده":
                    continue
                check_out = datetime.datetime.strptime(reservation.check_out_date, "%Y-%m-%d")
                if start <= check_out <= end:
                    total_income += reservation.total_cost

            return total_income
        except ValueError:
            return 0.0

    def get_today_income(self) -> float:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return self.report_income(today, today)


def dashboard(hotel: HotelManagementSystem):
    clear_terminal()
    print_menu_title("داشبورد سیستم مدیریت هتل 🏨")
    hotel.update_room_status()
    status_count = hotel.report_room_status()
    active_reservations = len(hotel.get_active_reservations())
    today_income = hotel.get_today_income()

    print_message(
        f"اتاق‌های خالی: {status_count['خالی']} | رزرو شده: {status_count['رزرو شده']} | اشغال شده: {status_count['اشغال شده']}",
        "info")
    print_message(f"رزروهای فعال: {active_reservations}", "info")
    print_message(f"درآمد امروز: {today_income:,.0f} تومان", "success")
    print_bar_chart(status_count, "وضعیت اتاق‌ها")

    input(f"{Fore.YELLOW}برای بازگشت به منوی اصلی، Enter بزنید...{Style.RESET_ALL}")


def main_menu():
    hotel = HotelManagementSystem()

    while True:
        clear_terminal()
        print_menu_title("سیستم مدیریت هتل 🏨")
        print("1. داشبورد 📈")
        print("2. مدیریت اتاق‌ها 🛏️")
        print("3. مدیریت مهمان‌ها 👤")
        print("4. مدیریت رزروها 📋")
        print("5. گزارشات 📊")
        print("0. خروج 🚪")

        choice = input("\nلطفا گزینه مورد نظر را انتخاب کنید: ")

        if choice == "1":
            dashboard(hotel)
        elif choice == "2":
            room_menu(hotel)
        elif choice == "3":
            guest_menu(hotel)
        elif choice == "4":
            reservation_menu(hotel)
        elif choice == "5":
            report_menu(hotel)
        elif choice == "0":
            print_message("خروج از برنامه...", "success")
            break
        else:
            print_message("گزینه نامعتبر! لطفا یک عدد از 0 تا 5 وارد کنید.", "error")


def room_menu(hotel: HotelManagementSystem):
    while True:
        clear_terminal()
        print_menu_title("مدیریت اتاق‌ها 🛏️")
        print("1. افزودن اتاق")
        print("2. ویرایش اتاق")
        print("3. حذف اتاق")
        print("4. مشاهده لیست اتاق‌ها")
        print("5. مشاهده اتاق‌های خالی")
        print("6. نمایش اطلاعات مهمان‌های اتاق‌ها")
        print("0. بازگشت به منوی اصلی")

        choice = input("\nلطفا گزینه مورد نظر را انتخاب کنید: ")

        if choice == "1":
            room_type = input("\nنوع اتاق (تک نفره، دو نفره، سوییت و...): ")
            try:
                price_str = input("قیمت هر شب (پیش‌فرض: 5,000,000 تومان) [Enter برای مقدار پیش‌فرض]: ")
                if price_str:
                    price = float(price_str)
                else:
                    price = 5000000

                room = hotel.add_room(room_type, price)
                print_message(f"اتاق با موفقیت اضافه شد: {room}", "success")
            except ValueError:
                print_message("خطا: قیمت باید عدد باشد!", "error")

        elif choice == "2":
            room_id = input("\nشناسه اتاق: ")
            room = hotel.get_room(room_id)

            if not room:
                print_message("اتاق یافت نشد!", "error")
                continue

            print_message(f"اطلاعات فعلی: {room}")
            room_type = input(f"نوع اتاق جدید (فعلی: {room.room_type}) [Enter برای بدون تغییر]: ")
            price_str = input(f"قیمت جدید (فعلی: {room.price:,.0f} تومان) [Enter برای بدون تغییر]: ")
            status = input(f"وضعیت جدید (فعلی: {room.status}) [Enter برای بدون تغییر]: ")

            price = None
            if price_str:
                try:
                    price = float(price_str)
                except ValueError:
                    print_message("خطا: قیمت باید عدد باشد!", "error")
                    continue

            if not room_type:
                room_type = None
            if not status:
                status = None

            if hotel.edit_room(room_id, room_type, price, status):
                print_message("اتاق با موفقیت ویرایش شد!", "success")
            else:
                print_message("خطا در ویرایش اتاق!", "error")

        elif choice == "3":
            room_id = input("\nشناسه اتاق: ")
            if hotel.delete_room(room_id):
                print_message("اتاق با موفقیت حذف شد!", "success")
            else:
                print_message("خطا: اتاق یافت نشد یا دارای رزرو فعال است!", "error")

        elif choice == "4":
            rooms = hotel.get_all_rooms()
            if not rooms:
                print_message("هیچ اتاقی ثبت نشده است!")
            else:
                headers = ["شناسه", "نوع", "قیمت", "وضعیت"]
                widths = [10, 15, 15, 10]
                rows = [[room.room_id, room.room_type, f"{room.price:,.0f} تومان", room.status] for room in rooms]
                sort_choice = print_table(headers, rows, widths, "لیست اتاق‌ها:", sortable=True)
                if sort_choice and sort_choice.isdigit() and 1 <= int(sort_choice) <= len(headers):
                    col = int(sort_choice) - 1
                    rows.sort(key=lambda x: x[col])
                    print_table(headers, rows, widths, "لیست اتاق‌ها (مرتب‌شده):")

        elif choice == "5":
            rooms = hotel.get_available_rooms()
            if not rooms:
                print_message("هیچ اتاق خالی وجود ندارد!")
            else:
                headers = ["شناسه", "نوع", "قیمت", "وضعیت"]
                widths = [10, 15, 15, 10]
                rows = [[room.room_id, room.room_type, f"{room.price:,.0f} تومان", room.status] for room in rooms]
                print_table(headers, rows, widths, "لیست اتاق‌های خالی:")

        elif choice == "6":
            occupied_rooms = [room for room in hotel.get_all_rooms() if room.status == "اشغال شده"]
            if not occupied_rooms:
                print_message("هیچ اتاقی اشغال نشده است!")
            else:
                print_message("اطلاعات مهمان‌های اتاق‌ها:")
                total_width = 90
                print(Fore.CYAN + "─" * total_width + Style.RESET_ALL)
                for room in occupied_rooms:
                    guest = hotel.get_guest(room.current_guest_id) if room.current_guest_id else None
                    reservation = next((r for r in hotel.get_room_reservations(room.room_id) if r.status == "فعال"),
                                       None)
                    print(f"اتاق {room.room_id} - نوع: {room.room_type}")
                    if guest:
                        print(
                            f"  مهمان: {guest.name} {guest.family} - کد ملی: {guest.national_id} - تلفن: {guest.phone}")
                        if reservation:
                            print(f"  تاریخ تخلیه پیش‌بینی‌شده: {reservation.check_out_date}")
                    else:
                        print_message("اطلاعات مهمان در دسترس نیست!", "error")
                    print(Fore.CYAN + "─" * total_width + Style.RESET_ALL)
                print()

        elif choice == "0":
            break

        else:
            print_message("گزینه نامعتبر! لطفا یک عدد از 0 تا 6 وارد کنید.", "error")


def guest_menu(hotel: HotelManagementSystem):
    while True:
        clear_terminal()
        print_menu_title("مدیریت مهمان‌ها 👤")
        print("1. افزودن مهمان")
        print("2. ویرایش مهمان")
        print("3. حذف مهمان")
        print("4. مشاهده لیست مهمان‌ها")
        print("5. جستجوی مهمان")
        print("0. بازگشت به منوی اصلی")

        choice = input("\nلطفا گزینه مورد نظر را انتخاب کنید: ")

        if choice == "1":
            name = input("\nنام مهمان: ")
            family = input("نام خانوادگی مهمان: ")
            national_id = input("کد ملی (۱۰ رقم، مثال: 0123456789): ")
            phone = input("شماره تماس (۱۱ رقم، شروع با 09، مثال: 09123456789): ")
            address = input("آدرس (اختیاری): ")

            try:
                guest = hotel.add_guest(name, family, national_id, phone, address)
                headers = ["شناسه", "نام", "نام خانوادگی", "کد ملی", "تلفن"]
                widths = [10, 15, 15, 12, 12]
                rows = [[guest.guest_id, guest.name, guest.family, guest.national_id, guest.phone]]
                print_message("مهمان با موفقیت اضافه شد!", "success")
                print_table(headers, rows, widths)
            except ValueError as e:
                print_message(f"خطا: {e}", "error")

        elif choice == "2":
            guests = hotel.get_all_guests()
            if not guests:
                print_message("هیچ مهمانی ثبت نشده است!")
                continue
            headers = ["ردیف", "شناسه", "نام", "نام خانوادگی", "کد ملی", "تلفن"]
            widths = [6, 10, 15, 15, 12, 12]
            rows = [[str(i + 1), g.guest_id, g.name, g.family, g.national_id, g.phone] for i, g in enumerate(guests)]
            print_table(headers, rows, widths, "لیست مهمان‌ها:")
            row_num = input("شماره ردیف مهمان برای ویرایش (یا Enter برای لغو): ")
            if not row_num or not row_num.isdigit() or int(row_num) > len(guests):
                continue
            guest = guests[int(row_num) - 1]
            print_message(f"اطلاعات فعلی: {guest}")
            name = input(f"نام جدید (فعلی: {guest.name}) [Enter برای بدون تغییر]: ")
            family = input(f"نام خانوادگی جدید (فعلی: {guest.family}) [Enter برای بدون تغییر]: ")
            national_id = input(f"کد ملی جدید (فعلی: {guest.national_id}) [Enter برای بدون تغییر]: ")
            phone = input(f"شماره تماس جدید (فعلی: {guest.phone}) [Enter برای بدون تغییر]: ")
            address = input(f"آدرس جدید (فعلی: {guest.address}) [Enter برای بدون تغییر]: ")

            if not name:
                name = None
            if not family:
                family = None
            if not national_id:
                national_id = None
            if not phone:
                phone = None
            if not address:
                address = None

            try:
                if hotel.edit_guest(guest.guest_id, name, family, national_id, phone, address):
                    print_message("مهمان با موفقیت ویرایش شد!", "success")
            except ValueError as e:
                print_message(f"خطا: {e}", "error")

        elif choice == "3":
            guest_id = input("\nشناسه مهمان: ")
            if hotel.delete_guest(guest_id):
                print_message("مهمان با موفقیت حذف شد!", "success")
            else:
                print_message("خطا: مهمان یافت نشد یا دارای رزرو فعال است!", "error")

        elif choice == "4":
            guests = hotel.get_all_guests()
            if not guests:
                print_message("هیچ مهمانی ثبت نشده است!")
            else:
                headers = ["شناسه", "نام", "نام خانوادگی", "کد ملی", "تلفن"]
                widths = [10, 15, 15, 12, 12]
                rows = [[g.guest_id, g.name, g.family, g.national_id, g.phone] for g in guests]
                sort_choice = print_table(headers, rows, widths, "لیست مهمان‌ها:", sortable=True)
                if sort_choice and sort_choice.isdigit() and 1 <= int(sort_choice) <= len(headers):
                    col = int(sort_choice) - 1
                    rows.sort(key=lambda x: x[col])
                    print_table(headers, rows, widths, "لیست مهمان‌ها (مرتب‌شده):")

        elif choice == "5":
            query = input("\nجستجو (نام یا کد ملی): ")
            guests = hotel.search_guests(query)

            if not guests:
                print_message("هیچ مهمانی یافت نشد!")
            else:
                headers = ["شناسه", "نام", "نام خانوادگی", "کد ملی", "تلفن"]
                widths = [10, 15, 15, 12, 12]
                rows = [[g.guest_id, g.name, g.family, g.national_id, g.phone] for g in guests]
                print_table(headers, rows, widths, f"نتایج جستجو برای '{query}':")

        elif choice == "0":
            break

        else:
            print_message("گزینه نامعتبر! لطفا یک عدد از 0 تا 5 وارد کنید.", "error")


def reservation_menu(hotel: HotelManagementSystem):
    while True:
        clear_terminal()
        print_menu_title("مدیریت رزروها 📋")
        print("1. رزرو کردن اتاق")
        print("2. تحویل اتاق (چک-این)")
        print("3. تسویه و تخلیه اتاق (چک-اوت)")
        print("4. لغو رزرو")
        print("5. مشاهده لیست رزروها")
        print("6. مشاهده رزروهای فعال")
        print("7. مشاهده رزروهای یک مهمان")
        print("8. مشاهده رزروهای یک اتاق")
        print("0. بازگشت به منوی اصلی")

        choice = input("\nلطفا گزینه مورد نظر را انتخاب کنید: ")

        if choice == "1":
            guests = hotel.get_all_guests()
            if not guests:
                print_message("هیچ مهمانی ثبت نشده است! ابتدا یک مهمان اضافه کنید.")
                continue

            headers = ["شناسه", "نام", "نام خانوادگی", "کد ملی", "تلفن"]
            widths = [10, 15, 15, 12, 12]
            rows = [[g.guest_id, g.name, g.family, g.national_id, g.phone] for g in guests]
            print_table(headers, rows, widths, "لیست مهمان‌ها:")

            guest_id = input("\nشناسه مهمان: ")

            rooms = hotel.get_available_rooms()
            if not rooms:
                print_message("هیچ اتاق خالی وجود ندارد!")
                continue

            headers = ["شناسه", "نوع", "قیمت", "وضعیت"]
            widths = [10, 15, 15, 10]
            rows = [[room.room_id, room.room_type, f"{room.price:,.0f} تومان", room.status] for room in rooms]
            print_table(headers, rows, widths, "لیست اتاق‌های خالی:")

            room_id = input("\nشناسه اتاق: ")
            check_in_date = input("تاریخ ورود (مثال: 1404-01-01): ")
            check_out_date = input("تاریخ خروج (مثال: 1404-01-05): ")

            reservation = hotel.make_reservation(guest_id, room_id, check_in_date, check_out_date)
            if reservation:
                guest = hotel.get_guest(guest_id)
                room = hotel.get_room(room_id)
                headers = ["شناسه", "مهمان", "اتاق", "ورود", "خروج", "وضعیت", "هزینه"]
                widths = [10, 20, 15, 12, 12, 10, 15]
                rows = [[reservation.reservation_id, f"{guest.name} {guest.family}", room.room_type,
                         reservation.check_in_date, reservation.check_out_date, reservation.status,
                         f"{reservation.total_cost:,.0f} تومان"]]
                print_message("رزرو با موفقیت انجام شد!", "success")
                print_table(headers, rows, widths)
                print(f"{Fore.YELLOW}ℹ️ هزینه کل: {reservation.total_cost:,.0f} تومان{Style.RESET_ALL}\n")
            else:
                print_message(
                    "خطا: رزرو انجام نشد! (مهمان/اتاق یافت نشد، اتاق خالی نیست، تاریخ نامعتبر یا رزرو همپوشان)",
                    "error")

        elif choice == "2":
            reservation_id = input("\nشناسه رزرو: ")
            if hotel.check_in(reservation_id):
                print_message("تحویل اتاق با موفقیت انجام شد!", "success")
            else:
                print_message("خطا: رزرو یافت نشد، فعال نیست یا هنوز به تاریخ ورود نرسیده‌ایم!", "error")

        elif choice == "3":
            reservation_id = input("\nشناسه رزرو: ")
            result = hotel.check_out(reservation_id)
            if isinstance(result, float):
                print_message(f"تسویه و تخلیه اتاق با موفقیت انجام شد! هزینه نهایی: {result:,.0f} تومان", "success")
            else:
                print_message("خطا: رزرو یافت نشد، فعال نیست یا تاریخ نامعتبر است!", "error")

        elif choice == "4":
            reservation_id = input("\nشناسه رزرو: ")
            if hotel.cancel_reservation(reservation_id):
                print_message("رزرو با موفقیت لغو شد!", "success")
            else:
                print_message("خطا: رزرو یافت نشد یا فعال نیست!", "error")

        elif choice == "5":
            reservations = hotel.get_all_reservations()
            if not reservations:
                print_message("هیچ رزروی ثبت نشده است!")
            else:
                headers = ["شناسه", "مهمان", "اتاق", "ورود", "خروج", "وضعیت", "هزینه"]
                widths = [10, 20, 15, 12, 12, 10, 15]
                rows = []
                for r in reservations:
                    guest = hotel.get_guest(r.guest_id)
                    room = hotel.get_room(r.room_id)
                    rows.append([r.reservation_id, f"{guest.name} {guest.family}" if guest else "نامشخص",
                                 room.room_type if room else "نامشخص", r.check_in_date, r.check_out_date, r.status,
                                 f"{r.total_cost:,.0f} تومان"])
                sort_choice = print_table(headers, rows, widths, "لیست رزروها:", sortable=True)
                if sort_choice and sort_choice.isdigit() and 1 <= int(sort_choice) <= len(headers):
                    col = int(sort_choice) - 1
                    rows.sort(key=lambda x: x[col])
                    print_table(headers, rows, widths, "لیست رزروها (مرتب‌شده):")

        elif choice == "6":
            reservations = hotel.get_active_reservations()
            if not reservations:
                print_message("هیچ رزرو فعالی وجود ندارد!")
            else:
                headers = ["شناسه", "مهمان", "اتاق", "ورود", "خروج", "وضعیت", "هزینه"]
                widths = [10, 20, 15, 12, 12, 10, 15]
                rows = []
                for r in reservations:
                    guest = hotel.get_guest(r.guest_id)
                    room = hotel.get_room(r.room_id)
                    rows.append([r.reservation_id, f"{guest.name} {guest.family}" if guest else "نامشخص",
                                 room.room_type if room else "نامشخص", r.check_in_date, r.check_out_date, r.status,
                                 f"{r.total_cost:,.0f} تومان"])
                print_table(headers, rows, widths, "لیست رزروهای فعال:")

        elif choice == "7":
            guest_id = input("\nشناسه مهمان: ")
            reservations = hotel.get_guest_reservations(guest_id)
            if not reservations:
                print_message(f"هیچ رزروی برای مهمان با شناسه {guest_id} یافت نشد!")
            else:
                headers = ["شناسه", "مهمان", "اتاق", "ورود", "خروج", "وضعیت", "هزینه"]
                widths = [10, 20, 15, 12, 12, 10, 15]
                rows = []
                for r in reservations:
                    guest = hotel.get_guest(r.guest_id)
                    room = hotel.get_room(r.room_id)
                    rows.append([r.reservation_id, f"{guest.name} {guest.family}" if guest else "نامشخص",
                                 room.room_type if room else "نامشخص", r.check_in_date, r.check_out_date, r.status,
                                 f"{r.total_cost:,.0f} تومان"])
                print_table(headers, rows, widths, f"لیست رزروهای مهمان {guest_id}:")

        elif choice == "8":
            room_id = input("\nشناسه اتاق: ")
            reservations = hotel.get_room_reservations(room_id)
            if not reservations:
                print_message(f"هیچ رزروی برای اتاق با شناسه {room_id} یافت نشد!")
            else:
                headers = ["شناسه", "مهمان", "اتاق", "ورود", "خروج", "وضعیت", "هزینه"]
                widths = [10, 20, 15, 12, 12, 10, 15]
                rows = []
                for r in reservations:
                    guest = hotel.get_guest(r.guest_id)
                    room = hotel.get_room(r.room_id)
                    rows.append([r.reservation_id, f"{guest.name} {guest.family}" if guest else "نامشخص",
                                 room.room_type if room else "نامشخص", r.check_in_date, r.check_out_date, r.status,
                                 f"{r.total_cost:,.0f} تومان"])
                print_table(headers, rows, widths, f"لیست رزروهای اتاق {room_id}:")

        elif choice == "0":
            break

        else:
            print_message("گزینه نامعتبر! لطفا یک عدد از 0 تا 8 وارد کنید.", "error")


def report_menu(hotel: HotelManagementSystem):
    while True:
        clear_terminal()
        print_menu_title("گزارشات 📊")
        print("1. گزارش وضعیت اتاق‌ها")
        print("2. گزارش رزروهای یک تاریخ")
        print("3. گزارش درآمد")
        print("0. بازگشت به منوی اصلی")

        choice = input("\nلطفا گزینه مورد نظر را انتخاب کنید: ")

        if choice == "1":
            status_count = hotel.report_room_status()
            print_bar_chart(status_count, "گزارش وضعیت اتاق‌ها")

        elif choice == "2":
            date = input("\nتاریخ مورد نظر (مثال: 1404-01-01): ")
            reservations = hotel.report_reservations_by_date(date)

            if not reservations:
                print_message(f"هیچ رزرو فعالی برای تاریخ {date} یافت نشد!")
            else:
                headers = ["شناسه", "مهمان", "اتاق", "هزینه"]
                widths = [10, 20, 15, 15]
                rows = []
                for reservation in reservations:
                    guest = hotel.get_guest(reservation.guest_id)
                    room = hotel.get_room(reservation.room_id)
                    guest_name = f"{guest.name} {guest.family}" if guest else "نامشخص"
                    room_type = room.room_type if room else "نامشخص"
                    rows.append(
                        [reservation.reservation_id, guest_name, room_type, f"{reservation.total_cost:,.0f} تومان"])
                print_table(headers, rows, widths, f"رزروهای فعال در تاریخ {date}:")

        elif choice == "3":
            start_date = input("\nتاریخ شروع (مثال: 1404-01-01): ")
            end_date = input("تاریخ پایان (مثال: 1404-01-30): ")

            income = hotel.report_income(start_date, end_date)
            if income == 0.0:
                print_message(f"هیچ درآمدی در بازه {start_date} تا {end_date} ثبت نشده یا تاریخ نامعتبر است!")
            else:
                print_timeline(income, start_date, end_date)

        elif choice == "0":
            break

        else:
            print_message("گزینه نامعتبر! لطفا یک عدد از 0 تا 3 وارد کنید.", "error")


if __name__ == "__main__":
    main_menu()
