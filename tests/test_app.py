import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget
from swissclock.main import UnifiedApp

def test_unified_app_initial_state(qtbot):
    app = UnifiedApp()
    qtbot.addWidget(app)
    with qtbot.waitExposed(app):
        app.show()
    
    # Check that we start in clock mode
    assert app.stacked.currentIndex() == 0
    assert app.action_widget.isVisible() == False
    assert "Stopwatch" in app.btn_toggle.text()

def test_unified_app_toggle_view(qtbot):
    app = UnifiedApp()
    qtbot.addWidget(app)
    with qtbot.waitExposed(app):
        app.show()
    
    # Switch to stopwatch
    qtbot.mouseClick(app.btn_toggle, Qt.LeftButton)
    
    assert app.stacked.currentIndex() == 1
    assert app.action_widget.isVisible() == True
    assert "Clock" in app.btn_toggle.text()
    
    # Switch back to clock
    qtbot.mouseClick(app.btn_toggle, Qt.LeftButton)
    
    assert app.stacked.currentIndex() == 0
    assert app.action_widget.isVisible() == False
    assert "Stopwatch" in app.btn_toggle.text()
