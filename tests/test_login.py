"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
- RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
- Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh.
Sinh viên cần hoàn thành TC-02 và TC-03.*)
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR

def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-01-login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found"

"""💡 Bonus B2 — Data-Driven Testing:
        TC-02 và TC-03 có cùng pattern (nhập → click → kiểm tra lỗi).
        Bạn có thể gộp bằng @pytest.mark.parametrize:

        @pytest.mark.parametrize("email, password, tc_id", [
            ("valid@email.com", "wrongpass", "TC-02"),
            ("", "", "TC-03"),
        ])
        def test_login_fail(page, test_config, email, password, tc_id):
            ...

        Xem thêm: docs/textbook-concepts.md §3 (Data-Driven Testing)"""

@pytest.mark.parametrize("email, password, tc_id", [
            ("librarian@library.com", "wrongpass", "TC-02"),
            ("", "", "TC-03"),
        ])

def test_login_fail(page, test_config, email, password, tc_id):
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")
    wrong_password_message = "Mật khẩu không đúng"
    blank_input_message = "Vui lòng nhập email và mật khẩu"
    if tc_id == "TC-02":
        wait_for_flutter(page, text=wrong_password_message)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-02-login_failure_wrong_password.png"))
    elif tc_id == "TC-03":
        wait_for_flutter(page, text=blank_input_message)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC-03-login_failure_blank_input.png"))
    
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    if tc_id == "TC-02":
        has_wrong_password_message =  wrong_password_message in sem_text
        assert has_wrong_password_message, \
            f"Error message for wrong password not shown"
    elif tc_id == "TC-03":
        has_blank_input_message =  blank_input_message in sem_text
        assert has_blank_input_message, \
            f"Error message for blank input not shown"
