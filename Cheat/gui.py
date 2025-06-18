import Configs as cfg

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

def checkbox_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)

def combo_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)

def slider_callback(sender, app_data, user_data):
    class_name, attr_name = user_data
    setattr(getattr(cfg, class_name), attr_name, app_data)

def box_style_callback(sender, app_data, user_data):
    cfg.ESP.box_style = user_data

def line_position_callback(sender, app_data, user_data):
    cfg.ESP.line_position = user_data

def render():
    create_context()
    with window(label="", width=GUI_WIDTH, height=GUI_HEIGHT, no_move=True, no_resize=True, no_title_bar=True, tag="Primary Window"):
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
                             width=150, label="##skeleton_color")                
                # Right column - Skeleton Settings
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
                                   callback=slider_callback, user_data=("ESP", "max_distance"),
                                   width=150, label="##max_distance", format="%.0f")
        
    create_viewport(title="CS2", width=GUI_WIDTH, height=GUI_HEIGHT, x_pos=0, y_pos=0, resizable=False)
    setup_dearpygui()
    show_viewport()
    set_primary_window("Primary Window", True)

    while is_dearpygui_running():
        render_dearpygui_frame()

    destroy_context()

if __name__ == '__main__':
    render()