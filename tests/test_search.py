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
import pytest
from conftest import (
    flutter_fill,
    login,
    wait_for_flutter,
    SCREENSHOT_DIR,
)

# =========================
# FIXED CONFIG (CI SAFE)
# =========================

SEARCH_BOX = "Tìm kiếm theo tên sách hoặc tác giả..."
CATEGORY_BOX = "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"

BOOK_CARD = 'flt-semantics[role="group"]'


# =========================
# HELPER SAFE WAIT
# =========================
def wait_books(page):
    wait_for_flutter(page, selector=BOOK_CARD)


# =========================
# TC-04 SEARCH NAME
# =========================
def test_search_book_by_name(page, test_config):
    login(page, test_config)

    wait_books(page)

    flutter_fill(page, SEARCH_BOX, "Flutter")

    wait_books(page)

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-04-search.png"
        )
    )

    books = page.locator(BOOK_CARD).count()

    assert books > 0, \
        f"Search page displayed no books for user {test_config['display_name']}"


# =========================
# TC-05 NO RESULT
# =========================
def test_search_book_no_result(page, test_config):
    login(page, test_config)

    flutter_fill(
        page,
        SEARCH_BOX,
        "xyz_khong_ton_tai_12345"
    )

    page.wait_for_timeout(1000)

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-05-search_book_no_result.png"
        )
    )

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    book_count = page.locator(BOOK_CARD).count()

    assert (
        "Không tìm thấy" in sem_text
        or "Không có" in sem_text
        or book_count == 0
    ), "Search should return no result"


# =========================
# TC-06 CATEGORY
# =========================
def test_filter_by_category(page, test_config):
    login(page, test_config)

    wait_books(page)

    flutter_fill(page, CATEGORY_BOX, "Công nghệ")

    wait_books(page)

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-06-category.png"
        )
    )

    books = page.locator(BOOK_CARD).all()

    assert len(books) > 0, \
        f"No books displayed after filtering for user {test_config['display_name']}"

    books = page.locator(BOOK_CARD).all()

    assert len(books) > 0, \
        f"No books displayed after filtering for user {test_config['display_name']}"


# =========================
# TC-07 AUTHOR
# =========================
def test_search_book_by_author(page, test_config):
    login(page, test_config)

    wait_books(page)

    flutter_fill(page, SEARCH_BOX, "Nguyễn")

    wait_books(page)

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "TC-07-author.png"
        )
    )

    books = page.locator(BOOK_CARD).count()

    assert books > 0, \
        f"Author search returned no books for user {test_config['display_name']}"
    
    