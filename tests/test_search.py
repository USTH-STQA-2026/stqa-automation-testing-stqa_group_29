"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
    (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
    (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
    (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    login,
    wait_for_flutter,
    SCREENSHOT_DIR,
)

def test_search_book_by_name(page, test_config):
    login(page, test_config)
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Flutter"
    )
    wait_for_flutter(page, text="Flutter")
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-04-search_book_by_name.png"
        )
    )
    books = page.locator(
        'flt-semantics[aria-label*="Flutter"]'
    ).count()
    assert books > 0, \
        "No \"Flutter\" books found"

def test_search_book_no_result(page, test_config):
    login(page, test_config)
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai"
    )
    wait_for_flutter(page, text="Không")  # hoặc text của empty state
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-05-search_book_no_result.png"
        )
    )
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    no_books_found = "Không tìm thấy sách" in sem_text
    assert no_books_found, \
        "Expected no books but still found results"

def test_filter_by_category(page, test_config):
    login(page, test_config)
    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ"
    )
    wait_for_flutter(page, text="Công nghệ")
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-06-filter_by_category.png"
        )
    )
    books = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    )
    count = books.count()
    assert count > 0, \
        "No books displayed after filtering"
    for i in range(count):
        text = books.nth(i).get_attribute("aria-label")
        assert "Công nghệ" in text, \
            f"Book {i+1} is not in Công nghệ category"

def test_search_book_by_author(page, test_config):
    login(page, test_config)
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Nguyễn Minh Đức"
    )
    wait_for_flutter(
        page,
        text="Mã: BOOK001"
    )
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-07-search_book_by_author.png"
        )
    )
    books = page.locator(
        'flt-semantics[aria-label*="BOOK001"]'
    ).count()
    assert books > 0, \
        "No books found for author Nguyễn Minh Đức"