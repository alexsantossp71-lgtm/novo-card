from scrapers.terra_scraper import TerraScraper
from scrapers.brasil247_scraper import Brasil247Scraper
from services.summarizer import OllamaSummarizer
from services.prompt_generator import OllamaPromptGenerator
import json
import os
import re

class WorkflowManager:
    def __init__(self):
        self.summarizer = OllamaSummarizer(model="llama3.2:3b")
        self.prompt_generator = OllamaPromptGenerator(model="llama3.2:3b")
        self.scrapers = {
            'Terra': TerraScraper(),
            'Brasil 247': Brasil247Scraper()
        }

    def list_headlines(self, source_name):
        scraper = self.scrapers.get(source_name)
        if not scraper:
            return []
        
        # Terra uses get_headlines, B247 uses list_headlines. 
        # Ideally we'd standardize this in BaseScraper but for now check:
        if hasattr(scraper, 'list_headlines'):
            return scraper.list_headlines()
        return scraper.get_headlines()

    def process_article(self, source_name, url, progress_callback=None):
        scraper = self.scrapers.get(source_name)
        if not scraper:
            return None

        if progress_callback: progress_callback("Scraping...")
        article_data = scraper.scrape(url)
        
        if not article_data or not article_data.get('content'):
            return None

        if progress_callback: progress_callback("Summarizing...")
        summary = self.summarizer.summarize(article_data['content'])

        if progress_callback: progress_callback("Generating Prompts...")
        prompts = self.prompt_generator.generate_prompts(summary)

        # Append Link to TikTok summary
        if 'tiktok_summary' in summary:
            summary['tiktok_summary'] += f"\n\n🔗 {url}"

        full_data = {
            **article_data,
            "summary": summary,
            "prompts": prompts
        }
        
        # Save
        self.save_news(full_data)
        return full_data

    def save_news(self, data):
        os.makedirs('data', exist_ok=True)
        # Find next index in data root
        existing = os.listdir('data')
        # Check folders that start with digit
        indices = []
        for d in existing:
            if os.path.isdir(os.path.join('data', d)) and d[0].isdigit() and '_' in d:
                try:
                    indices.append(int(d.split('_')[0]))
                except:
                    pass
            # Also check files for legacy compatibility or the ones just created
            elif os.path.isfile(os.path.join('data', d)) and d[0].isdigit() and '_' in d:
                 try:
                    indices.append(int(d.split('_')[0]))
                 except:
                    pass
        
        new_index = max(indices) + 1 if indices else 1

        safe_title = "".join([c for c in data['title'] if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
        base_name = f"{new_index}_{safe_title[:50]}"
        
        # New Structure: data/{base_name}/{base_name}.json
        folder_path = os.path.join('data', base_name)
        os.makedirs(folder_path, exist_ok=True)
        
        filename = os.path.join(folder_path, f"{base_name}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return filename

    def generate_images_for_article(self, json_path, data, progress_callback=None):
        from services.image_service import ImageService
        from batch_overlay import add_text_overlay as add_cover_overlay
        from batch_card_overlay import add_card_overlay as add_internal_overlay

        # Init service
        if progress_callback: progress_callback("Loading Image Model...")
        service = ImageService()
        
        prompts = data.get('prompts', {})
        summary = data.get('summary', {})
        target_dir = os.path.dirname(json_path)
        
        stages = ['general_summary', 'introduction', 'development', 'conclusion']
        
        for stage in stages:
            prompt = prompts.get(stage)
            if not prompt or prompt == "Error":
                continue
                
            if progress_callback: progress_callback(f"Generating {stage}...")
            
            out_path = os.path.join(target_dir, f"{stage}.png")
            service.generate_image(prompt, out_path)
            
            if progress_callback: progress_callback(f"Applying overlay to {stage}...")
            
            if stage == 'general_summary':
                add_cover_overlay(out_path, json_path, out_path)
            else:
                card_text = summary.get(stage, "")
                if card_text:
                    add_internal_overlay(out_path, card_text, out_path)

    def process_article(self, source_name, url, progress_callback=None):
        scraper = self.scrapers.get(source_name)
        if not scraper:
            return None

        if progress_callback: progress_callback("Scraping...")
        article_data = scraper.scrape(url)
        
        if not article_data or not article_data.get('content'):
            return None

        if progress_callback: progress_callback("Summarizing...")
        summary = self.summarizer.summarize(article_data['content'])

        if progress_callback: progress_callback("Generating Prompts...")
        prompts = self.prompt_generator.generate_prompts(summary)

        # Append Link to TikTok summary
        if 'tiktok_summary' in summary:
            summary['tiktok_summary'] += f"\n\n🔗 {url}"

        full_data = {
            **article_data,
            "summary": summary,
            "prompts": prompts
        }
        
        # Save
        json_path = self.save_news(full_data)
        
        # Auto-Generate Images
        try:
            self.generate_images_for_article(json_path, full_data, progress_callback)
        except Exception as e:
            print(f"Auto-generation failed: {e}")
            if progress_callback: progress_callback(f"Image Gen Error: {e}")

        return full_data
