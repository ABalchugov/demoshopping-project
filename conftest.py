def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Browser to use"
    )
    parser.addoption(
        "--headless",
        choices=["true", "false"],
        default="false",
    )
    parser.addoption(
        "--window_size",
        default="1920*1080",
        help="Window size"
    )
