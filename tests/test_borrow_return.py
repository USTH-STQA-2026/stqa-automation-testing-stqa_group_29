"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
    - Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn"
    (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
    - Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")'
    (*Nút mượn*)
    - After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again
    (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
    - Return button: 'flt-semantics[role="button"]:has-text("Trả sách")'
    (*Nút trả*)
"""
import os
import time
from conftest import (
    enable_flutter_semantics, wait_for_flutter,
    login, SCREENSHOT_DIR,
)

def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    Description (*Mô tả*):
        Log in → find an "Available" book → click "Mượn sách này" → confirm dialog
        → verify book status changes to "Borrowed".
        (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
        → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)

    Suggested steps (*Gợi ý các bước*):
        1. login(page, test_config)
        2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]')
        (*Tìm sách Có sẵn*)
        3. Click "Mượn sách này" button inside that book card
        (*Click nút "Mượn sách này" trong sách đó*)
        4. Wait for confirmation dialog, re-enable semantics
        (*Đợi dialog xác nhận, bật lại semantics*)
        5. Click "Mượn" button (confirm button in dialog)
        (*Click nút "Mượn" — nút xác nhận trong dialog*)
        6. Assert: "Đang mượn" or "thành công" appears
        (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)
    """
    login(page, test_config)
    enable_flutter_semantics(page)
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="visible", timeout=10000)
    
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()

    confirm_btn = page.locator('flt-semantics[role="button"]:has-text("Mượn")').last
    confirm_btn.wait_for(state="visible", timeout=5000)
    confirm_btn.click()

    enable_flutter_semantics(page)
    wait_for_flutter(page, text="đang mượn",timeout=10000)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents()).lower()
    assert "đang mượn" in sem_text or "thành công" in sem_text, \
        "Lỗi: Không tìm thấy trạng thái 'Đang mượn' hoặc thông báo mượn sách thành công!"
    page.screenshot(path=os.path.join(SCREENSHOT_DIR,"TC-08_borrow_success.png"))

def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    Description (*Mô tả*):
        Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
        (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

    Hints (*Gợi ý*):
        - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
        - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
        (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)
    """
    login(page, test_config)
    
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.wait_for(state="visible", timeout=10000)
    borrow_tab.click()
    wait_for_flutter(page, "Tra cứu phiếu mượn")
    
    return_buttons = page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    assert return_buttons.count() > 0, \
        "Lỗi: Không tìm thấy bất kỳ cuốn sách nào đang mượn hoặc không thấy nút 'Trả sách' trong tab Mượn / Trả."
    page.screenshot(path=os.path.join(SCREENSHOT_DIR,"TC-09_view_borrowed_books.png"))

def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    Description (*Mô tả*):
        Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
        (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

    Hints (*Gợi ý*):
        - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
        - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
        (*Tìm nút "Trả sách"*)
        - Click and verify status change or success message
        (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)
    """
    login(page, test_config)
    
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.wait_for(state="visible", timeout=10000)
    borrow_tab.click()
    wait_for_flutter(page, "Tra cứu phiếu mượn")
    
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.wait_for(state="visible", timeout=10000)
    return_btn.click()
    # (Tùy chọn) Xử lý Dialog xác nhận trả sách nếu hệ thống có thiết kế
    try:
        # Nếu có hộp thoại hỏi "Bạn có chắc muốn trả?", ta nhấn xác nhận (Trả sách/Xác nhận)
        # Bắt ngoại lệ nếu hệ thống trả sách ngay lập tức mà không cần hỏi thêm.
        confirm_return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').last
        if confirm_return_btn.is_visible(timeout=3000):
            confirm_return_btn.click()
    except:
        pass
    
    enable_flutter_semantics(page)
    wait_for_flutter(page, text="thành công",timeout=10000)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents()).lower()
    assert "thành công" in sem_text or "trả sách" in sem_text, \
        "Lỗi: Việc trả sách không thành công hoặc không nhận diện được thông báo trả sách."
    page.screenshot(path=os.path.join(SCREENSHOT_DIR,"TC-10_return_success.png"))
