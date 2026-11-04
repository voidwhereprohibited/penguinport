from landfall.scan.owned import describe, is_paid, owned_paid_apps

SCANNED = [
    {"name": "Adobe Photoshop 2025", "version": "26.1", "publisher": "Adobe",
     "icon": "C:\\x.exe", "source": "Installed program"},
    {"name": "Adobe Acrobat Reader", "version": "24", "publisher": "Adobe"},
    {"name": "Microsoft Office Professional Plus 2021", "version": "16.0", "publisher": "Microsoft"},
    {"name": "WinRAR 7.0 (64-bit)", "version": "", "publisher": "win.rar GmbH"},
    {"name": "Google Chrome", "version": "130", "publisher": "Google LLC"},
    {"name": "winrar 7.0 (64-bit)", "version": "", "publisher": ""},
]


def test_free_apps_are_not_listed():
    assert not is_paid("Google Chrome")
    assert not is_paid("Adobe Acrobat Reader")
    assert is_paid("Adobe Acrobat Pro")


def test_lists_paid_apps_sorted_and_deduplicated():
    names = [a["name"] for a in owned_paid_apps(SCANNED)]
    assert names == ["Adobe Photoshop 2025", "Microsoft Office Professional Plus 2021",
                     "WinRAR 7.0 (64-bit)"]


def test_only_name_version_publisher_are_kept():
    for app in owned_paid_apps(SCANNED + [{"name": "Snagit", "product_key": "ABCDE-12345"}]):
        assert set(app) == {"name", "version", "publisher"}


def test_describe():
    assert describe({"name": "Snagit", "version": "24"}) == "Snagit (version 24)"
    assert describe({"name": "Snagit", "version": ""}) == "Snagit"
