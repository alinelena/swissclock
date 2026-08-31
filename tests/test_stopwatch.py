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
    
    stopwatch.toggle_timer()
    qtbot.wait(50)
    stopwatch.toggle_timer()
    
    assert stopwatch.total_elapsed > 0
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
