from PySide6.QtCore import Qt

from swissclock.main import UnifiedApp


def test_unified_app_initial_state(qtbot):
    app = UnifiedApp()
    qtbot.addWidget(app)
    with qtbot.waitExposed(app):
        app.show()
    
    # Check that we start in clock mode
    assert app.stacked.currentIndex() == 0
    assert not app.action_widget.isVisible()
    assert "Stopwatch" in app.btn_toggle.text()

def test_unified_app_toggle_view(qtbot):
    app = UnifiedApp()
    qtbot.addWidget(app)
    with qtbot.waitExposed(app):
        app.show()
    
    # Switch to stopwatch
    qtbot.mouseClick(app.btn_toggle, Qt.LeftButton)
    
    assert app.stacked.currentIndex() == 1
    assert app.action_widget.isVisible()
    assert "Clock" in app.btn_toggle.text()
    
    # Switch back to clock
    qtbot.mouseClick(app.btn_toggle, Qt.LeftButton)
    
    assert app.stacked.currentIndex() == 0
    assert not app.action_widget.isVisible()
    assert "Stopwatch" in app.btn_toggle.text()

def test_unified_app_shortcuts_and_drawing(qtbot):
    app = UnifiedApp()
    qtbot.addWidget(app)
    with qtbot.waitExposed(app):
        app.show()
        
    # Trigger paintEvent for clock
    app.grab()
    
    # Test toggle shortcut via method
    app.toggle_view()
    assert app.stacked.currentIndex() == 1 # Should switch to stopwatch
    
    # Trigger paintEvent for stopwatch (analog)
    app.grab()
    
    # Test start/stop space handler
    app.handle_space()
    assert app.stopwatch_widget.running
    qtbot.wait(100) # Wait a bit for timer to tick
    
    # Trigger paintEvent again while running
    app.grab()
    
    app.handle_space()
    assert not app.stopwatch_widget.running
    
    # Test digital toggle handler
    app.handle_digital()
    assert app.stopwatch_widget.is_digital
    
    # Trigger paintEvent for digital stopwatch
    app.grab()
    
    # Test reset handler
    app.handle_reset()
    assert app.stopwatch_widget.total_elapsed == 0
    
    # Test fullscreen toggle
    assert not app.isFullScreen()
    app.toggle_fullscreen()
    assert app.isFullScreen()
    app.toggle_fullscreen()
    assert not app.isFullScreen()

def test_main(monkeypatch):
    import sys

    from PySide6.QtWidgets import QApplication

    import swissclock.main
    # Mock sys.argv and sys.exit
    monkeypatch.setattr(sys, "argv", ["swissclock"])
    monkeypatch.setattr(sys, "exit", lambda x: x)
    
    # Mock app.exec
    app = QApplication.instance()
    monkeypatch.setattr(app, "exec", lambda: 0)
    
    swissclock.main.main()
