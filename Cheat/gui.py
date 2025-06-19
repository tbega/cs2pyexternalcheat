import Configs as cfg
import time
import math
import os

from dearpygui.dearpygui import create_context, destroy_context, start_dearpygui, create_viewport, setup_dearpygui, show_viewport, is_dearpygui_running, render_dearpygui_frame, set_primary_window
from dearpygui.dearpygui import window, child_window, tab_bar, tab, group, add_spacer
from dearpygui.dearpygui import add_checkbox, add_text, add_combo, add_input_text, add_slider_float, add_separator, add_button
from dearpygui.dearpygui import theme, theme_component, add_theme_color, add_theme_style, bind_theme, bind_item_theme
from dearpygui.dearpygui import add_color_picker, add_color_edit
from dearpygui.dearpygui import add_font, bind_font, add_font_range_hint, mvFontRangeHint_Default, font_registry
from dearpygui.dearpygui import mvAll, mvThemeCat_Core, mvStyleVar_FrameRounding, mvStyleVar_WindowRounding, mvStyleVar_ChildRounding, mvStyleVar_GrabRounding, mvStyleVar_TabRounding, mvStyleVar_ItemSpacing, mvStyleVar_FramePadding, mvStyleVar_WindowPadding
from dearpygui.dearpygui import mvThemeCol_FrameBg, mvThemeCol_WindowBg, mvThemeCol_TitleBgActive, mvThemeCol_TitleBg, mvThemeCol_Button, mvThemeCol_ButtonHovered, mvThemeCol_ButtonActive, mvThemeCol_ChildBg
from dearpygui.dearpygui import mvThemeCol_Header, mvThemeCol_HeaderHovered, mvThemeCol_HeaderActive, mvThemeCol_FrameBgHovered, mvThemeCol_FrameBgActive
from dearpygui.dearpygui import mvThemeCol_Tab, mvThemeCol_TabHovered, mvThemeCol_TabActive, mvThemeCol_SliderGrab, mvThemeCol_SliderGrabActive, mvThemeCol_Text, mvThemeCol_CheckMark
from dearpygui.dearpygui import mvThemeCol_Border, mvThemeCol_Separator, mvThemeCol_ScrollbarBg, mvThemeCol_ScrollbarGrab, mvThemeCol_ScrollbarGrabHovered, mvThemeCol_ScrollbarGrabActive

GUI_WIDTH = 800
GUI_HEIGHT = 800

COLORS = {
    'bg_primary': (20, 20, 20),         
    'bg_secondary': (30, 30, 30),       
    'bg_tertiary': (40, 40, 40),        
    'accent_primary': (70, 130, 220),   
    'accent_secondary': (30, 100, 200), 
    'accent_glow': (100, 150, 255),     
    'text_primary': (255, 255, 255),    
    'text_secondary': (200, 200, 200),  
    'text_accent': (100, 150, 255),     
    'success': (40, 180, 90),           
    'warning': (220, 160, 30),          
    'danger': (200, 60, 60),            
    'border': (60, 60, 60),             
    'separator': (80, 80, 80),          
    'child_bg': (25, 25, 25),           
}

def apply_light_blue_theme():
    with theme() as global_theme:
        with theme_component(mvAll):            
            add_theme_color(mvThemeCol_WindowBg, COLORS['bg_primary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_ChildBg, COLORS['bg_secondary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_FrameBg, COLORS['bg_secondary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_FrameBgHovered, COLORS['bg_tertiary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_FrameBgActive, COLORS['accent_secondary'], category=mvThemeCat_Core)
            
            
            add_theme_color(mvThemeCol_TitleBg, COLORS['bg_secondary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_TitleBgActive, COLORS['accent_primary'], category=mvThemeCat_Core)
            
            
            add_theme_color(mvThemeCol_Button, COLORS['accent_primary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_ButtonHovered, COLORS['accent_glow'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_ButtonActive, COLORS['accent_secondary'], category=mvThemeCat_Core)
            
            
            add_theme_color(mvThemeCol_Header, COLORS['bg_tertiary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_HeaderHovered, COLORS['accent_primary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_HeaderActive, COLORS['accent_secondary'], category=mvThemeCat_Core)
            
            add_theme_color(mvThemeCol_Tab, COLORS['bg_secondary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_TabHovered, COLORS['accent_primary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_TabActive, COLORS['accent_glow'], category=mvThemeCat_Core)
            
            
            add_theme_color(mvThemeCol_SliderGrab, COLORS['accent_glow'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_SliderGrabActive, COLORS['text_accent'], category=mvThemeCat_Core)
            
           
            add_theme_color(mvThemeCol_Text, COLORS['text_primary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_CheckMark, COLORS['accent_glow'], category=mvThemeCat_Core)
            
           
            add_theme_color(mvThemeCol_Border, COLORS['border'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_Separator, COLORS['separator'], category=mvThemeCat_Core)
            
            
            add_theme_color(mvThemeCol_ScrollbarBg, COLORS['bg_secondary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_ScrollbarGrab, COLORS['accent_primary'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_ScrollbarGrabHovered, COLORS['accent_glow'], category=mvThemeCat_Core)
            add_theme_color(mvThemeCol_ScrollbarGrabActive, COLORS['text_accent'], category=mvThemeCat_Core)
            
            
            add_theme_style(mvStyleVar_FrameRounding, 8, category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_WindowRounding, 12, category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_ChildRounding, 10, category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_GrabRounding, 6, category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_TabRounding, 6, category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_ItemSpacing, 8, 6, category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_FramePadding, 10, 6, category=mvThemeCat_Core)
            add_theme_style(mvStyleVar_WindowPadding, 15, 15, category=mvThemeCat_Core)
            
            add_theme_color(mvThemeCol_ChildBg, COLORS['child_bg'], category=mvThemeCat_Core)  # Ensure this is set last
            
    bind_theme(global_theme)

def create_section_header(text, color=None):
    """Create a styled section header with optional color"""
    if color is None:
        color = COLORS['text_accent']
    add_spacer(height=5)
    add_text(text, color=color)
    add_separator()
    add_spacer(height=3)

def create_info_text(text, color=None):
    """Create styled info text"""
    if color is None:
        color = COLORS['text_secondary']
    add_text(text, color=color)


visual_esp_checkboxes = {
    "Show Box": ("ESP", "show_box"),
    "Show Line": ("ESP", "show_line"),
    "Show Health Bar": ("ESP", "show_health"),
    "Show Teammates": ("ESP", "show_teammates"),
}


info_esp_checkboxes = {
    "Show Distance": ("ESP", "show_distance"),
    "Show Weapon": ("ESP", "show_weapon"),
    "Show Name": ("ESP", "show_name"),
    "Show Health Text": ("ESP", "show_health_text"),
}


skeleton_esp_checkboxes = {
    "Show Skeleton": ("ESP", "show_skeleton"),
    "Show Head Circle": ("ESP", "show_head_circle"),
    "Skeleton Shadow": ("ESP", "skeleton_shadow"),
}


triggerbot_checkboxes = {
    "Enable Triggerbot": ("TRIGGERBOT", "enabled"),
    "Shoot Teammates": ("TRIGGERBOT", "shoot_teammates"),
}

def checkbox_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def combo_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def toggle_callback(sender, app_data, user_data):
    """Callback for toggle switches (checkboxes acting as switches)"""
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def slider_callback(sender, app_data, user_data):
    """Callback for regular sliders"""
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def box_style_callback(sender, app_data, user_data):
    """Callback for box style options"""
    cfg.ESP.box_style = app_data
    cfg.ConfigManager.save_config()

# Add these globals for color debouncing
color_update_timer = {}
color_pending_updates = {}

def debounced_color_callback(sender, app_data, user_data):
    """Debounced callback for color picker changes to reduce excessive updates"""
    class_name, attr_name = user_data
    key = f"{class_name}.{attr_name}"
    
    
    color_pending_updates[key] = (class_name, attr_name, app_data)
    
    
    if key in color_update_timer:
        try:
            color_update_timer[key].cancel()
        except:
            pass
    
   
    import threading
    def apply_color_update():
        if key in color_pending_updates:
            stored_class_name, stored_attr_name, stored_app_data = color_pending_updates[key]
            r, g, b, a = stored_app_data
              
            setattr(getattr(cfg, stored_class_name), stored_attr_name, [r, g, b, a])
            cfg.ConfigManager.save_config()
            
            
            if key in color_pending_updates:
                del color_pending_updates[key]
            if key in color_update_timer:
                del color_update_timer[key]
    
    color_update_timer[key] = threading.Timer(0.2, apply_color_update)
    color_update_timer[key].start()

def color_callback(sender, app_data, user_data):
    """Immediate callback for color picker changes - reduced logging"""
    class_name, attr_name = user_data
    r, g, b, a = app_data
    
    
    setattr(getattr(cfg, class_name), attr_name, [r, g, b, a])
    
    
    cfg.ConfigManager.save_config()

def triggerbot_delay_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    
    setattr(getattr(cfg, class_name), attr_name, app_data)
    
    if attr_name == "delay_min" and app_data >= cfg.TRIGGERBOT.delay_max:
        cfg.TRIGGERBOT.delay_max = app_data + 0.05  # Add 50ms to max
    elif attr_name == "delay_max" and app_data <= cfg.TRIGGERBOT.delay_min:
        cfg.TRIGGERBOT.delay_min = app_data - 0.05  # Subtract 50ms from min
        if cfg.TRIGGERBOT.delay_min < 0.0:  # Don't go below 0ms
            cfg.TRIGGERBOT.delay_min = 0.0
    
    cfg.ConfigManager.save_config()

def fps_callback(sender, app_data, user_data):
    """Special callback for FPS that updates dynamically and saves config"""
    cfg.MISC.overlay_fps = int(app_data)
    cfg.ConfigManager.save_config()
      
    try:
        import Main
        cheat_instance = Main.get_cheat_instance()
        if cheat_instance:
            cheat_instance.update_overlay_fps(int(app_data))
    except Exception as e:
        pass  

def always_on_top_callback(sender, app_data, user_data):
    """Special callback for always on top to immediately apply the setting"""
    cfg.MISC.always_on_top = app_data
    cfg.ConfigManager.save_config()
    try:
        import ctypes
        user32 = ctypes.windll.user32
        HWND_TOPMOST = -1
        HWND_NOTOPMOST = -2
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        
        hwnd = user32.FindWindowW(None, "Cheat Menu")  
        if hwnd:
            if app_data:  
                user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            else:  
                user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    except Exception as e:
        pass 

def input_text_callback(sender, app_data, user_data):
    """Callback for text input fields like trigger key"""
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)
    cfg.ConfigManager.save_config()

def load_fonts():
    """Load a more readable font for the GUI"""
    font_tag = None
    with font_registry():
        try:
            local_font_path = os.path.join(os.path.dirname(__file__), "ARLRDBD.ttf")
            if os.path.exists(local_font_path):
                font_tag = add_font(local_font_path, 16)
                return font_tag
        except Exception as e:
            pass

        try:
            font_tag = add_font(r"C:\Windows\Fonts\arial.ttf", 16)
            return font_tag
        except Exception as e:
            pass

        try:
            
            font_tag = add_font(r"C:\Windows\Fonts\segoeui.ttf", 16)
            return font_tag
        except Exception as e:
            pass

        try:
            
            font_tag = add_font(r"C:\Windows\Fonts\calibri.ttf", 16)
            return font_tag
        except Exception as e:
            pass

        try:
            
            font_tag = add_font(r"C:\Windows\Fonts\consola.ttf", 16)
            return font_tag
        except Exception as e:
            pass

    print("[GUI] Using default DearPyGUI font.")
    return None

def obfuscate_gui_title():
    """Obfuscate the GUI window title for security"""
    try:
        import random
        import string
        
        legitimate_titles = [
            "Microsoft Word",
            "Calculator", 
            "Notepad",
            "Windows Explorer",
            "Control Panel",
            "Task Manager",
            "System Settings",
            "Device Manager",
            "Windows Update"
        ]
        
        base_title = random.choice(legitimate_titles)
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        new_title = f"{base_title} - {random_suffix}"
        
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.FindWindowW(None, "Cheat Menu")
        
        if hwnd:
            user32.SetWindowTextW(hwnd, new_title)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"[GUI] Failed to obfuscate title: {e}")
        return False

def render():
    create_context()
    
   
    create_viewport(title="Cheat Menu", width=GUI_WIDTH, height=GUI_HEIGHT, x_pos=100, y_pos=100, resizable=False, always_on_top=cfg.MISC.always_on_top)
    setup_dearpygui()

    
    default_colors = {
        "box_color":      [1.0, 1.0, 1.0, 1.0],
        "box_fill_color": [1.0, 1.0, 1.0, 0.3],
        "line_color":     [1.0, 1.0, 1.0, 1.0],
        "skeleton_color": [1.0, 1.0, 1.0, 1.0],
    }
    
   
    for key, default in default_colors.items():
        val = getattr(cfg.ESP, key, None)
          
        if not isinstance(val, (list, tuple)) or len(val) < 3:
            
            setattr(cfg.ESP, key, default)
        else:
            
            val_list = list(val)
            
           
            if len(val_list) == 3:
                val_list.append(1.0 if key != "box_fill_color" else 0.3)
            elif len(val_list) > 4:
                val_list = val_list[:4]  
            
            
            if any(isinstance(c, (int, float)) and c > 1.0 for c in val_list[:3]):
                val_list = [float(c)/255.0 for c in val_list[:3]] + [val_list[3]]
            
            
            if key == "box_fill_color":
                if val_list[3] < 0.05:  
                    val_list[3] = 0.3  
            else:
                if val_list[3] < 0.5:  
                    val_list[3] = 1.0  
            val_list = [max(0.0, min(1.0, float(c))) for c in val_list]
            
            setattr(cfg.ESP, key, val_list)
    
    cfg.ConfigManager.save_config()

    default_font = load_fonts()
    if default_font:
        bind_font(default_font)

    with window(label="Cheat Menu", width=GUI_WIDTH, height=GUI_HEIGHT, no_resize=True, tag="Primary Window"):
        apply_light_blue_theme()
        
        # Header section
        add_spacer(height=10)
        add_text("CS2 External Cheat", color=COLORS['accent_primary'])
        add_text("Advanced Gaming Enhancment Program", color=COLORS['text_secondary'])
        add_separator()
        with tab_bar():
            with tab(label="ESP"):
                add_spacer(height=15)
                
                # Visual ESP Section
                create_section_header("Visual ESP", COLORS['accent_primary'])
                add_spacer(height=10)
                
                # Show Box Toggle
                with group(horizontal=True):
                    add_text("Show Box:", color=COLORS['text_primary'])
                    add_spacer(width=80)
                    initial_box = getattr(cfg.ESP, "show_box")
                    add_checkbox(label="##show_box_toggle", default_value=initial_box,
                               callback=toggle_callback, user_data=("ESP", "show_box"))
                
                add_spacer(height=8)
                
                # Show Line Toggle
                with group(horizontal=True):
                    add_text("Show Line:", color=COLORS['text_primary'])
                    add_spacer(width=75)
                    initial_line = getattr(cfg.ESP, "show_line")
                    add_checkbox(label="##show_line_toggle", default_value=initial_line,
                               callback=toggle_callback, user_data=("ESP", "show_line"))
                
                add_spacer(height=8)
                
                # Health Bar Toggle
                with group(horizontal=True):
                    add_text("Health Bar:", color=COLORS['text_primary'])
                    add_spacer(width=70)
                    initial_health = getattr(cfg.ESP, "show_health")
                    add_checkbox(label="##show_health_toggle", default_value=initial_health,
                               callback=toggle_callback, user_data=("ESP", "show_health"))
                
                add_spacer(height=8)
                
                # Show Teammates Toggle
                with group(horizontal=True):
                    add_text("Show Teammates:", color=COLORS['text_primary'])
                    add_spacer(width=45)
                    initial_teammates = getattr(cfg.ESP, "show_teammates")
                    add_checkbox(label="##show_teammates_toggle", default_value=initial_teammates,
                               callback=toggle_callback, user_data=("ESP", "show_teammates"))
                
                add_spacer(height=20)
                
                # Info ESP Section
                create_section_header("Info ESP", COLORS['accent_secondary'])
                add_spacer(height=10)
                
                # Information checkboxes in a more compact layout
                with group(horizontal=True):
                    add_checkbox(label="Distance", default_value=getattr(cfg.ESP, "show_distance"),
                               callback=toggle_callback, user_data=("ESP", "show_distance"))
                    add_spacer(width=20)
                    add_checkbox(label="Name", default_value=getattr(cfg.ESP, "show_name"),
                               callback=toggle_callback, user_data=("ESP", "show_name"))
                    add_spacer(width=20)
                    add_checkbox(label="Weapon", default_value=getattr(cfg.ESP, "show_weapon"),
                               callback=toggle_callback, user_data=("ESP", "show_weapon"))
                
                add_spacer(height=8)
                with group(horizontal=True):
                    add_checkbox(label="Health Text", default_value=getattr(cfg.ESP, "show_health_text"),
                               callback=toggle_callback, user_data=("ESP", "show_health_text"))
                
                add_spacer(height=20)
                
                # Skeleton Section - more compact
                create_section_header("Skeleton ESP", COLORS['text_accent'])
                add_spacer(height=10)
                
                with group(horizontal=True):
                    add_checkbox(label="Skeleton", default_value=getattr(cfg.ESP, "show_skeleton"),
                               callback=toggle_callback, user_data=("ESP", "show_skeleton"))
                    add_spacer(width=20)
                    add_checkbox(label="Head Circle", default_value=getattr(cfg.ESP, "show_head_circle"),
                               callback=toggle_callback, user_data=("ESP", "show_head_circle"))
                    add_spacer(width=20)
                    add_checkbox(label="Shadow", default_value=getattr(cfg.ESP, "skeleton_shadow"),
                               callback=toggle_callback, user_data=("ESP", "skeleton_shadow"))
                
                add_spacer(height=20)
                
                # Color Settings Section
                create_section_header("Color Settings", COLORS['accent_glow'])
                add_spacer(height=10)
                
                # Box Color with color picker and opacity
                add_text("Box Color:", color=COLORS['text_primary'])
                add_spacer(height=5)
                box_color_val = list(cfg.ESP.box_color)  # Make a copy
                add_color_edit(default_value=box_color_val, 
                             callback=debounced_color_callback, user_data=("ESP", "box_color"),
                             width=200, label="##box_color_picker", alpha_preview=True, no_inputs=True)
                
                add_spacer(height=10)
                # Box Fill Color (for filled boxes)
                add_text("Box Fill Color:", color=COLORS['text_primary'])
                add_spacer(height=5)
                box_fill_color_val = list(cfg.ESP.box_fill_color)  # Make a copy
                add_color_edit(default_value=box_fill_color_val, 
                             callback=debounced_color_callback, user_data=("ESP", "box_fill_color"),
                             width=200, label="##box_fill_color_picker", alpha_preview=True, no_inputs=True)
            
                add_spacer(height=10)
                
                # Line Color with color picker and opacity
                add_text("Line Color:", color=COLORS['text_primary'])
                add_spacer(height=5)
                line_color_val = list(cfg.ESP.line_color)  # Make a copy
                add_color_edit(default_value=line_color_val, 
                             callback=debounced_color_callback, user_data=("ESP", "line_color"),
                             width=200, label="##line_color_picker", alpha_preview=True, no_inputs=True)
                
                add_spacer(height=10)
                
                # Skeleton Color with color picker and opacity
                add_text("Skeleton Color:", color=COLORS['text_primary'])
                add_spacer(height=5)
                skeleton_color_val = list(cfg.ESP.skeleton_color)  # Make a copy
                add_color_edit(default_value=skeleton_color_val, 
                             callback=debounced_color_callback, user_data=("ESP", "skeleton_color"),
                             width=200, label="##skeleton_color_picker", alpha_preview=True, no_inputs=True)
                
                add_spacer(height=15)
                # Style Settings
                create_section_header("Style Settings", COLORS['text_accent'])
                add_spacer(height=10)
                # Box Style setting
                with group(horizontal=True):
                    add_text("Box Style:", color=COLORS['text_primary'])
                    add_spacer(width=50)
                    box_style_options = ["Regular", "Cornered", "Filled", "Cornered + Filled"]
                    current_box_style = getattr(cfg.ESP, "box_style", "Regular")
                    add_combo(items=box_style_options, default_value=current_box_style,
                              callback=combo_callback, user_data=("ESP", "box_style"),
                              width=140, label="##box_style")
                
                add_spacer(height=8)
                
                # Line Position setting
                with group(horizontal=True):
                    add_text("Line Position:", color=COLORS['text_primary'])
                    add_spacer(width=35)
                    line_position_options = ["Top", "Center", "Bottom"]
                    current_line_position = getattr(cfg.ESP, "line_position", "Top")
                    add_combo(items=line_position_options, default_value=current_line_position,
                              callback=combo_callback, user_data=("ESP", "line_position"),
                              width=120, label="##line_position")
                
                add_spacer(height=15)
                
                # Slider Settings
                create_section_header("Settings", COLORS['text_accent'])
                add_spacer(height=10)
                
                add_text("Max Distance:", color=COLORS['text_primary'])
                add_spacer(height=5)
                current_max_distance = getattr(cfg.ESP, "max_distance")
                add_slider_float(min_value=5, max_value=50, default_value=current_max_distance,
                                 callback=slider_callback, user_data=("ESP", "max_distance"),
                                 width=300, label="##max_distance", format="%.0f meters")
                
                add_spacer(height=10)
                
                add_text("Skeleton Thickness:", color=COLORS['text_primary'])
                add_spacer(height=5)
                current_thickness = getattr(cfg.ESP, "skeleton_thickness")
                add_slider_float(min_value=0.5, max_value=5.0, default_value=current_thickness,
                                 callback=slider_callback, user_data=("ESP", "skeleton_thickness"),
                                 width=300, label="##skeleton_thickness", format="%.1f")
            
            with tab(label="Assist"):
                create_section_header("Triggerbot System", COLORS['accent_glow'])
                
                # Triggerbot checkboxes with modern styling
                for label, (class_name, attr_name) in triggerbot_checkboxes.items():
                    initial_value = getattr(getattr(cfg, class_name), attr_name)
                    add_checkbox(label=f"  {label}", default_value=initial_value, callback=checkbox_callback, user_data=(class_name, attr_name))
                
                add_spacer(height=15)
                create_section_header("Configuration")
                
                add_text("Trigger Key:", color=COLORS['text_primary'])
                current_trigger_key = getattr(cfg.TRIGGERBOT, "trigger_key")
                add_input_text(default_value=current_trigger_key, 
                              callback=input_text_callback, user_data=("TRIGGERBOT", "trigger_key"),
                              width=200, label="##trigger_key")
                
                add_spacer(height=15)
                create_section_header("Timing Settings", COLORS['warning'])
                
                add_text("Min Delay:", color=COLORS['text_primary'])
                current_delay_min = getattr(cfg.TRIGGERBOT, "delay_min")
                add_slider_float(min_value=0.0, max_value=0.4, default_value=current_delay_min,
                               callback=triggerbot_delay_callback, user_data=("TRIGGERBOT", "delay_min"),
                               width=400, label="##delay_min", format="%.2f sec")
                
                add_text("Max Delay:", color=COLORS['text_primary'])
                current_delay_max = getattr(cfg.TRIGGERBOT, "delay_max")
                add_slider_float(min_value=0.0, max_value=0.4, default_value=current_delay_max,
                               callback=triggerbot_delay_callback, user_data=("TRIGGERBOT", "delay_max"),
                               width=400, label="##delay_max", format="%.2f sec")
                
                add_spacer(height=10)
               
            
            with tab(label="Settings"):
                create_section_header("Application Settings", COLORS['accent_glow'])
                
                # Always on top checkbox with special callback
                initial_always_on_top = getattr(cfg.MISC, "always_on_top")
                add_checkbox(label="  Always On Top", default_value=initial_always_on_top, 
                           callback=always_on_top_callback, user_data=("MISC", "always_on_top"))
                
                add_spacer(height=15)
                create_section_header("Performance Optimization", COLORS['success'])
                
                add_text("Overlay FPS:", color=COLORS['text_primary'])
                current_fps = getattr(cfg.MISC, "overlay_fps")
                add_slider_float(min_value=30, max_value=240, default_value=current_fps,
                               callback=fps_callback, user_data=("MISC", "overlay_fps"),
                               width=400, label="##overlay_fps", format="%.0f fps")
                
                add_spacer(height=10)
                create_info_text("Higher FPS = smoother overlay but more CPU usage")
                create_info_text("Lower FPS = less CPU usage but choppier overlay")
                
                add_spacer(height=20)
                create_section_header("Information", COLORS['text_accent'])
                create_info_text("Settings are automatically saved")
    
    show_viewport()
    set_primary_window("Primary Window", True)
    
    try:
        import time
        time.sleep(0.5)  
        obfuscate_gui_title()
    except Exception as e:
        print(f"[GUI] Initial title obfuscation failed: {e}")
    
    try:
        import ctypes
        import time
        
        user32 = ctypes.windll.user32
        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        
        hwnd = user32.FindWindowW(None, "Cheat Menu")
        if not hwnd:
            
            def find_gui_window():
                def enum_callback(hwnd, lParam):
                    try:
                        class_buffer = ctypes.create_unicode_buffer(256)
                        user32.GetClassNameW(hwnd, class_buffer, 256)
                        class_name = class_buffer.value
                        
                
                        if "GLFW" in class_name or "SDL" in class_name:
                            return hwnd
                    except:
                        pass
                    return None
                
                EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
                return None
            
            if not hwnd:
                hwnd = find_gui_window()
        
        if hwnd and cfg.MISC.always_on_top:
            user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    except Exception as e:
        pass  

    frame_count = 0
    title_obfuscation_interval = 1800 
    
    while is_dearpygui_running():
        render_dearpygui_frame()
        
        frame_count += 1
        
       
        if frame_count % title_obfuscation_interval == 0:
            try:
                obfuscate_gui_title()
            except:
                pass
        
        
        if frame_count % 300 == 0 and cfg.MISC.always_on_top:  
            try:
                
                hwnd = None
                
               
                for potential_title in ["Microsoft Word", "Calculator", "Notepad", "Windows Explorer", "Control Panel"]:
                    temp_hwnd = user32.FindWindowW(None, potential_title)
                    if temp_hwnd:
                        
                        hwnd = temp_hwnd
                        break
                
                
                if not hwnd:
                    hwnd = user32.FindWindowW(None, "Cheat Menu")
                
                if hwnd:
                    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            except:
                pass

    destroy_context()

if __name__ == '__main__':
    render()