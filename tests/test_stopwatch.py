from swissclock.stop import StopWatch


def test_stopwatch_initial_state(qtbot):
    stopwatch = StopWatch()
    qtbot.addWidget(stopwatch)

    assert not stopwatch.running
    assert stopwatch.total_elapsed == 0
    assert not stopwatch.is_digital
    assert stopwatch.countdown_target_ms == 0


def test_stopwatch_toggle_timer(qtbot):
    stopwatch = StopWatch()
    qtbot.addWidget(stopwatch)

    # Start timer
    stopwatch.toggle_timer()
    assert stopwatch.running

    # Pause timer
    stopwatch.toggle_timer()
    assert not stopwatch.running
    assert stopwatch.total_elapsed >= 0


def test_stopwatch_reset(qtbot):
    stopwatch = StopWatch()
    qtbot.addWidget(stopwatch)

    # Deterministically mock elapsed time instead of relying on sleep
    stopwatch.total_elapsed = 150
    stopwatch.running = True

    stopwatch.reset_timer()
    assert not stopwatch.running
    assert stopwatch.total_elapsed == 0


def test_stopwatch_toggle_digital(qtbot):
    stopwatch = StopWatch()
    qtbot.addWidget(stopwatch)

    assert not stopwatch.is_digital
    stopwatch.toggle_digital_mode()
    assert stopwatch.is_digital
    stopwatch.toggle_digital_mode()
    assert not stopwatch.is_digital


def test_stopwatch_set_countdown(qtbot):
    stopwatch = StopWatch()
    qtbot.addWidget(stopwatch)

    stopwatch.set_countdown(60000)
    assert stopwatch.countdown_target_ms == 60000
    assert stopwatch.total_elapsed == 0
    assert not stopwatch.running


def test_stopwatch_countdown_drawing_and_overtime(qtbot, monkeypatch):
    stopwatch = StopWatch()
    qtbot.addWidget(stopwatch)

    # Set a countdown and draw
    stopwatch.set_countdown(100)  # 100ms
    stopwatch.grab()  # Cover countdown drawing

    # Start and wait to reach < 10%
    stopwatch.toggle_timer()
    qtbot.wait(95)
    stopwatch.grab()  # Cover orange color

    # Wait to reach overtime
    qtbot.wait(20)
    stopwatch.grab()  # Cover red color / overtime drawing

    # Digital mode overtime
    stopwatch.toggle_digital_mode()
    stopwatch.update_dial()  # Manually trigger dial update to cover calculations
    stopwatch.grab()  # Cover digital overtime drawing

    # Test context menu (mock exec)
    monkeypatch.setattr("swissclock.stop.QMenu.exec", lambda self, pos: None)

    # Just to cover the instantiation of menu
    stopwatch.show_context_menu(stopwatch.rect().center())
