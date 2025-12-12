import flet as ft
import os
import json
import glob
import time
import threading
import shutil
from services.workflow_manager import WorkflowManager
# Import overlay logic
from batch_overlay import add_text_overlay as add_cover_overlay
from batch_card_overlay import add_card_overlay as add_internal_overlay

DATA_DIR = 'data'

def load_news():
    news_list = []
    if not os.path.exists(DATA_DIR):
        return []
    
    # Recursive search for JSONs in subfolders
    # Structure: data/Folder/File.json
    news_files = glob.glob(os.path.join(DATA_DIR, '*', '*.json'))
    news_files.sort(key=os.path.getmtime, reverse=True)
    
    for file_path in news_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Store full paths for ease of use
                data['file_path'] = file_path 
                data['dir_path'] = os.path.dirname(file_path)
                data['filename'] = os.path.basename(file_path)
                news_list.append(data)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return news_list

def main(page: ft.Page):
    page.title = "News Scraper Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0 

    workflow = WorkflowManager()
    
    def route_change(route):
        page.views.clear()
        
        # --- HOME VIEW ---
        if page.route == "/":
            
            # --- DASHBOARD TAB CONTENT ---
            news_grid = ft.GridView(
                runs_count=3,
                max_extent=500,
                child_aspect_ratio=0.6,
                spacing=20,
                run_spacing=20,
            )
            
            def load_dashboard_data():
                news_data = load_news()
                news_grid.controls.clear()
                
                def copy_prompt(e, prompt_text):
                    page.set_clipboard(prompt_text)
                    page.open(ft.SnackBar(content=ft.Text("Prompt copied!")))

                for news in news_data:
                    prompts = news.get("prompts", {})
                    summary = news.get('summary', {})
                    file_path = news.get('file_path')
                    dir_path = news.get('dir_path')

                    # Helper to generate image control
                    def get_image_control(image_name):
                        img_path = os.path.join(dir_path, image_name)
                        if os.path.exists(img_path):
                            return ft.Image(
                                src=img_path,
                                width=400,
                                height=250,
                                fit=ft.ImageFit.COVER,
                                border_radius=10,
                            )
                        return ft.Container()

                    # Actions
                    def delete_article(e, path):
                        try:
                            # Delete the entire directory
                            target_dir = os.path.dirname(path)
                            shutil.rmtree(target_dir)
                            page.open(ft.SnackBar(content=ft.Text("Article deleted!")))
                            load_dashboard_data() 
                        except Exception as ex:
                            page.open(ft.SnackBar(content=ft.Text(f"Error deleting: {ex}")))

                    card_content = ft.Column(
                        [
                            # COVER IMAGE
                            get_image_control("general_summary.png"),
                            
                            ft.Row([
                                ft.ElevatedButton(
                                    "Generate Images", 
                                    icon=ft.Icons.IMAGE, 
                                    color=ft.Colors.BLUE_300,
                                    on_click=lambda e, f=file_path: page.go(f"/generate/{f}") # Pass full file path
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE, 
                                    icon_color=ft.Colors.RED_300,
                                    tooltip="Delete Article",
                                    on_click=lambda e, f=file_path: delete_article(e, f)
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            
                            ft.Text(news.get('title', 'No Title'), size=16, weight="bold", selectable=True),
                            ft.Text(news.get('date', ''), size=12, color="grey", italic=True),
                            ft.Divider(),
                            
                            # Content Sections with Images
                            ft.Text("Introduction", size=14, weight="bold", color=ft.Colors.GREEN_200),
                            get_image_control("introduction.png"),
                            ft.Text(summary.get('introduction', 'N/A'), size=12, selectable=True),
                            
                            ft.Divider(),
                            ft.Text("Development", size=14, weight="bold", color=ft.Colors.GREEN_200),
                            get_image_control("development.png"),
                            ft.Text(summary.get('development', 'N/A'), size=12, selectable=True),
                            
                            ft.Divider(),
                            ft.Text("Conclusion", size=14, weight="bold", color=ft.Colors.GREEN_200),
                            get_image_control("conclusion.png"),
                            ft.Text(summary.get('conclusion', 'N/A'), size=12, selectable=True),
                            
                        ],
                        spacing=5,
                        scroll="adaptive", 
                    )
                    card = ft.Container(
                        content=card_content,
                        padding=15,
                        border_radius=10,
                        bgcolor=ft.Colors.GREY_900,
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.Colors.BLACK),
                    )
                    news_grid.controls.append(card)
                page.update()

            # --- EXTRACTION TAB CONTENT ---
            source_dropdown = ft.Dropdown(
                label="Select Source",
                options=[ft.dropdown.Option("Terra"), ft.dropdown.Option("Brasil 247")],
                width=200,
            )
            headlines_list = ft.ListView(expand=1, spacing=10, padding=20)
            process_status = ft.Text("")
            
            def fetch_headlines(e):
                if not source_dropdown.value:
                    process_status.value = "Please select a source."
                    page.update()
                    return
                process_status.value = "Fetching headlines..."
                page.update()
                headlines = workflow.list_headlines(source_dropdown.value)
                headlines_list.controls.clear()
                if not headlines:
                    process_status.value = "No headlines found."
                else:
                    process_status.value = f"Found {len(headlines)} headlines."
                    for title, url in headlines:
                        headlines_list.controls.append(ft.Checkbox(label=title, value=False, data=url))
                page.update()

            def process_selected(e):
                selected = [c for c in headlines_list.controls if c.value]
                if not selected:
                    process_status.value = "No articles selected."
                    page.update()
                    return
                total = len(selected)
                for i, checkbox in enumerate(selected):
                    process_status.value = f"Processing {i+1}/{total}: {checkbox.label[:30]}..."
                    page.update()
                    workflow.process_article(source_dropdown.value, checkbox.data, progress_callback=lambda msg: print(msg))
                    
                process_status.value = "Processing complete! Please run restructure command if needed."
                load_dashboard_data()
                page.update()

            extraction_view = ft.Column([
                ft.Row([source_dropdown, ft.ElevatedButton("Fetch Headlines", on_click=fetch_headlines)]),
                process_status,
                ft.Divider(),
                headlines_list,
                ft.ElevatedButton("Process Selected Articles", on_click=process_selected, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),
            ], expand=True)

            # INITIAL LOAD
            load_dashboard_data()

            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("News Scraper Dashboard"), bgcolor=ft.Colors.GREY_800),
                        ft.Tabs(
                            selected_index=0,
                            animation_duration=300,
                            tabs=[
                                ft.Tab(text="Dashboard", content=ft.Container(content=news_grid, expand=True, padding=10)),
                                ft.Tab(text="New Extraction", content=ft.Container(content=extraction_view, padding=20)),
                            ],
                            expand=1,
                        )
                    ],
                )
            )

        # --- GENERATION VIEW ---
        elif page.route.startswith("/generate/"):
            # Extract FULL path (everything after /generate/)
            path_arg = page.route[len("/generate/"):]
            filename = path_arg 
            
            log_column = ft.Column(scroll="always", expand=True)
            progress_bar = ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee", value=0)
            status_text = ft.Text("Initializing...", size=20)
            
            def go_back(e):
                page.go("/")

            page.views.append(
                ft.View(
                    "/generate",
                    [
                        ft.AppBar(title=ft.Text("Image Generation"), leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back), bgcolor=ft.Colors.GREY_800),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"Generating Images for: {os.path.basename(filename)}", size=16),
                                ft.Divider(),
                                status_text,
                                progress_bar,
                                ft.Divider(),
                                ft.Text("Logs:"),
                                ft.Container(content=log_column, bgcolor=ft.Colors.BLACK54, padding=10, border_radius=5, expand=True),
                            ], alignment="center", horizontal_alignment="center"),
                            padding=50,
                            expand=True
                        )
                    ],
                )
            )
            
            # Real Generation Logic
            def run_generation():
                try:
                    filepath = filename
                    if not os.path.exists(filepath):
                        status_text.value = f"Error: File not found {filepath}"
                        page.update()
                        return

                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    prompts = data.get('prompts', {})
                    summary = data.get('summary', {})
                    
                    status_text.value = "Loading Custom Model..."
                    page.update()
                    
                    from services.image_service import ImageService
                    service = ImageService() 
                    
                    target_dir = os.path.dirname(filepath)
                    
                    stages = ['general_summary', 'introduction', 'development', 'conclusion']
                    total_stages = len(stages)
                    
                    for i, stage in enumerate(stages):
                        prompt = prompts.get(stage)
                        if prompt:
                            msg = f"Generating {stage}..."
                            status_text.value = msg
                            log_column.controls.append(ft.Text(f"[INFO] {msg}", font_family="monospace"))
                            page.update()
                            
                            out_name = f"{stage}.png"
                            out_path = os.path.join(target_dir, out_name)
                            
                            # Generate
                            service.generate_image(prompt, out_path)
                            
                            # Apply Overlay
                            log_column.controls.append(ft.Text(f"[INFO] Applying overlay to {stage}...", font_family="monospace"))
                            page.update()
                            
                            if stage == 'general_summary':
                                add_cover_overlay(out_path, filepath, out_path)
                            else:
                                card_text = summary.get(stage, "")
                                if card_text:
                                    add_internal_overlay(out_path, card_text, out_path)
                            
                            log_column.controls.append(ft.Text(f"[SUCCESS] Saved {out_name}", color=ft.Colors.GREEN, font_family="monospace"))
                        
                        progress_bar.value = (i + 1) / total_stages
                        page.update()

                    status_text.value = "Generation Complete!"
                    status_text.color = ft.Colors.GREEN
                    page.update()

                except Exception as e:
                    status_text.value = f"Error: {str(e)}"
                    status_text.color = ft.Colors.RED
                    log_column.controls.append(ft.Text(f"[ERROR] {str(e)}", color=ft.Colors.RED, font_family="monospace"))
                    page.update()
            
            t = threading.Thread(target=run_generation)
            t.start()
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == '__main__':
    ft.app(target=main)
