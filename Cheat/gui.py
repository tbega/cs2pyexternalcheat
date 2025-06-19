import Configs as cfg
import time

from dearpygui.dearpygui import create_context, destroy_context, start_dearpygui,create_viewport, setup_dearpygui, show_viewport, is_dearpygui_running, render_dearpygui_frame, set_primary_window
from dearpygui.dearpygui import window, child_window, tab_bar, tab
from dearpygui.dearpygui import add_checkbox, add_text, add_combo, add_input_text, add_slider_float, add_separator

GUI_WIDTH = 600
GUI_HEIGHT = 500

# Visual ESP checkboxes 
visual_esp_checkboxes = {
    "Show Box": ("ESP", "show_box"),
    "Show Line": ("ESP", "show_line"),
    "Show Health Bar": ("ESP", "show_health"),
    "Show Teammates": ("ESP", "show_teammates"),
}

# Information ESP checkboxes
info_esp_checkboxes = {
    "Show Distance": ("ESP", "show_distance"),
    "Show Weapon": ("ESP", "show_weapon"),
    "Show Name": ("ESP", "show_name"),
    "Show Health Text": ("ESP", "show_health_text"),
}

# Skeleton ESP checkboxes
skeleton_esp_checkboxes = {
    "Show Skeleton": ("ESP", "show_skeleton"),
    "Show Head Circle": ("ESP", "show_head_circle"),
    "Skeleton Shadow": ("ESP", "skeleton_shadow"),
}

# Misc checkboxes
misc_checkboxes = {
    "Always On Top": ("MISC", "always_on_top"),
}

def checkbox_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def combo_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def slider_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def fps_callback(sender, app_data, user_data):
    """Special callback for FPS that updates dynamically and saves config"""
    cfg.MISC.overlay_fps = int(app_data)
    cfg.ConfigManager.save_config()
    
    # Update the overlay FPS dynamically if possible
    try:
        import Main
        cheat_instance = Main.get_cheat_instance()
        if cheat_instance:
            success = cheat_instance.update_overlay_fps(int(app_data))
            if success:
                print(f"[GUI] Overlay FPS updated to {int(app_data)}")
            else:
                print(f"[GUI] FPS setting saved ({int(app_data)}), dynamic update not supported")
        else:
            print(f"[GUI] FPS setting saved ({int(app_data)}), cheat not initialized yet")
    except Exception as e:
        print(f"[GUI] FPS setting saved ({int(app_data)}), dynamic update failed: {e}")

def always_on_top_callback(sender, app_data, user_data):
    """Special callback for always on top to immediately apply the setting"""
    cfg.MISC.always_on_top = app_data
    cfg.ConfigManager.save_config()
    
    # Immediately apply the always on top setting
    try:
        import ctypes
        user32 = ctypes.windll.user32
        HWND_TOPMOST = -1
        HWND_NOTOPMOST = -2
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        
        hwnd = user32.FindWindowW(None, "CS2 Cheat Menu")
        if hwnd:
            if app_data:  # Enable always on top
                user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                print("[GUI] Always on top enabled")
            else:  # Disable always on top
                user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
                print("[GUI] Always on top disabled")
    except Exception as e:
        print(f"[GUI] Failed to toggle always on top: {e}")

def box_style_callback(sender, app_data, user_data):
    cfg.ESP.box_style = user_data

def line_position_callback(sender, app_data, user_data):
    cfg.ESP.line_position = user_data

def render():
    create_context()
    with window(label="CS2 Cheat Menu", width=GUI_WIDTH, height=GUI_HEIGHT, no_resize=True, tag="Primary Window"):
        with tab_bar():
            with tab(label="ESP"):                # Left column - Visual ESP
                with child_window(width=180, height=400, tag="visual_esp"):
                    add_text("Visual ESP")
                    add_separator()
                    for label, (class_name, attr_name) in visual_esp_checkboxes.items():
                        initial_value = getattr(getattr(cfg, class_name), attr_name)
                        add_checkbox(label=label, default_value=initial_value, callback=checkbox_callback, user_data=(class_name, attr_name))
                    
                    add_separator()
                    add_text("Box Style:")
                    box_style_options = ["Regular", "Filled", "Cornered"]
                    current_box_style = getattr(cfg.ESP, "box_style")
                    add_combo(items=box_style_options, default_value=current_box_style,
                             callback=combo_callback, user_data=("ESP", "box_style"),
                             width=150, label="##box_style")
                    
                    add_separator()
                    add_text("Line Position:")
                    line_position_options = ["Top", "Center", "Bottom"]
                    current_line_position = getattr(cfg.ESP, "line_position")
                    add_combo(items=line_position_options, default_value=current_line_position,
                             callback=combo_callback, user_data=("ESP", "line_position"),
                             width=150, label="##line_position")
                    
                    add_separator()
                    add_text("Information ESP")
                    add_separator()
                    for label, (class_name, attr_name) in info_esp_checkboxes.items():
                        initial_value = getattr(getattr(cfg, class_name), attr_name)
                        add_checkbox(label=label, default_value=initial_value, callback=checkbox_callback, user_data=(class_name, attr_name))
                
                # Middle column - Colors
                with child_window(width=180, height=400, pos=[190, 30], tag="colors"):
                    add_text("Colors")
                    add_separator()
                    
                    color_options = ["Red", "Green", "Blue", "Yellow", "Magenta", "Cyan", "White", "Orange", "Purple", "Pink"]
                    
                    add_text("Box Color:")
                    current_box_color = getattr(cfg.ESP, "box_color")
                    add_combo(items=color_options, default_value=current_box_color,
                             callback=combo_callback, user_data=("ESP", "box_color"),
                             width=150, label="##box_color")
                    
                    add_text("Line Color:")
                    current_line_color = getattr(cfg.ESP, "line_color")
                    add_combo(items=color_options, default_value=current_line_color,
                             callback=combo_callback, user_data=("ESP", "line_color"),
                             width=150, label="##line_color")
                    
                    add_text("Skeleton Color:")
                    current_skeleton_color = getattr(cfg.ESP, "skeleton_color")
                    add_combo(items=color_options, default_value=current_skeleton_color,
                             callback=combo_callback, user_data=("ESP", "skeleton_color"),
                             width=150, label="##skeleton_color")                  # Right column - Skeleton Settings
                with child_window(width=180, height=400, pos=[380, 30], tag="skeleton"):
                    add_text("Skeleton Settings")
                    add_separator()
                    for label, (class_name, attr_name) in skeleton_esp_checkboxes.items():
                        initial_value = getattr(getattr(cfg, class_name), attr_name)
                        add_checkbox(label=label, default_value=initial_value, callback=checkbox_callback, user_data=(class_name, attr_name))
                    
                    add_text("Skeleton Thickness:")
                    current_thickness = getattr(cfg.ESP, "skeleton_thickness")
                    add_slider_float(min_value=0.5, max_value=5.0, default_value=current_thickness,
                                   callback=slider_callback, user_data=("ESP", "skeleton_thickness"),
                                   width=150, label="##skeleton_thickness", format="%.1f")
                    
                    add_separator()
                    add_text("ESP Range Settings")
                    add_separator()
                    
                    add_text("Max Distance (meters):")
                    current_max_distance = getattr(cfg.ESP, "max_distance")
                    add_slider_float(min_value=5, max_value=50, default_value=current_max_distance,
                                   callback=slider_callback, user_data=("ESP", "max_distance"),                                   width=150, label="##max_distance", format="%.0f")
            
            with tab(label="Misc"):
                with child_window(width=560, height=400, tag="misc_settings"):
                    add_text("Miscellaneous Settings")
                    add_separator()
                      # Always on top checkbox with special callback
                    initial_always_on_top = getattr(cfg.MISC, "always_on_top")
                    add_checkbox(label="Always On Top", default_value=initial_always_on_top, 
                               callback=always_on_top_callback, user_data=("MISC", "always_on_top"))
                    
                    add_separator()
                    add_text("Overlay Performance")
                    add_separator()
                    
                    add_text("Overlay FPS:")
                    current_fps = getattr(cfg.MISC, "overlay_fps")
                    add_slider_float(min_value=30, max_value=240, default_value=current_fps,
                                   callback=fps_callback, user_data=("MISC", "overlay_fps"),
                                   width=300, label="##overlay_fps", format="%.0f fps")
                    
                    add_text("Higher FPS = smoother overlay but more CPU usage")
                    add_text("Lower FPS = less CPU usage but choppier overlay")
                    
                    add_separator()
                    add_text("Application Settings")
                    add_separator()
                    add_text("Settings are automatically saved")
                    add_text("Always On Top setting takes effect immediately")
                    add_text("FPS changes take effect immediately when possible")
    
    create_viewport(title="CS2 Cheat Menu", width=GUI_WIDTH, height=GUI_HEIGHT, x_pos=100, y_pos=100, resizable=False, always_on_top=cfg.MISC.always_on_top)
    setup_dearpygui()
    show_viewport()
    set_primary_window("Primary Window", True)
    
    # Force the window to stay on top using Windows API if enabled
    try:
        import ctypes
        import time
        time.sleep(0.5)  # Let window create
        
        user32 = ctypes.windll.user32
        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        
        # Find our GUI window and set always on top if enabled
        hwnd = user32.FindWindowW(None, "CS2 Cheat Menu")
        if hwnd and cfg.MISC.always_on_top:
            user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            print("[GUI] Menu window set to always on top")
        elif hwnd:
            print("[GUI] Menu window created (always on top disabled)")
        else:
            print("[GUI] Could not find menu window")
    except Exception as e:
        print(f"[GUI] Could not set window properties: {e}")

    frame_count = 0
    
    while is_dearpygui_running():
        render_dearpygui_frame()
        
        # Periodically ensure window stays on top if enabled (every 5 seconds)
        frame_count += 1
        if frame_count % 300 == 0 and cfg.MISC.always_on_top:  # Roughly every 5 seconds at 60fps
            try:
                hwnd = user32.FindWindowW(None, "CS2 Cheat Menu")
                if hwnd:
                    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            except:
                pass

    destroy_context()

if __name__ == '__main__':
    render()