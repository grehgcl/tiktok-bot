import time
import random
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TikTokBot:
    def __init__(self):
        self.rodando = False
        self.stats = {
            'total_views': 0,
            'total_likes': 0,
            'videos_visitados': [],
            'logs': []
        }
        self.urls = []
        self.carregar_urls()
    
    def carregar_urls(self):
        try:
            if os.path.exists('dados/urls.txt'):
                with open('dados/urls.txt', 'r', encoding='utf-8-sig') as f:
                    urls = [line.strip() for line in f if line.strip()]
                if urls:
                    self.urls = [url.replace('\ufeff', '').strip() for url in urls]
                    return
        except:
            pass
        self.urls = ["https://www.tiktok.com/@seeagende/video/7669632240116124949"]
    
    def log(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_msg = f"[{timestamp}] {msg}"
        self.stats['logs'].append(log_msg)
        print(log_msg)
    
    def configurar_driver(self):
        """Configura o undetected-chromedriver para evitar detecção"""
        options = uc.ChromeOptions()
        
        # Configurações para servidor
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Headless mode para servidor
        options.add_argument('--headless=new')
        
        # User agent realista
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Cria o driver
        driver = uc.Chrome(options=options, version_main=150)
        
        return driver
    
    def assistir_video(self, url, driver):
        try:
            self.log(f"🌐 Acessando: {url}")
            driver.get(url)
            time.sleep(5)
            
            # Rola a página
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            
            # Tenta dar play no vídeo
            try:
                video = driver.find_element(By.TAG_NAME, "video")
                driver.execute_script("arguments[0].play();", video)
                self.log("🎬 Reproduzindo vídeo...")
            except:
                try:
                    driver.find_element(By.TAG_NAME, 'body').click()
                    self.log("🎬 Clicou na tela")
                except:
                    pass
            
            # Assistir por um tempo
            duracao = random.uniform(30, 60)
            self.log(f"⏳ Assistindo por {duracao:.0f} segundos...")
            
            # Simula comportamento humano durante a visualização
            intervalos = int(duracao / 10)
            for _ in range(intervalos):
                time.sleep(10)
                if random.random() > 0.7:
                    driver.execute_script(f"window.scrollBy(0, {random.randint(-50, 50)})")
            
            time.sleep(random.uniform(2, 5))
            
            # Tenta curtir
            if random.random() > 0.4:
                try:
                    like_selectors = [
                        '[data-e2e="like-icon"]',
                        '[data-e2e="like"]',
                        'button[class*="like"]'
                    ]
                    for selector in like_selectors:
                        try:
                            like_btn = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            like_btn.click()
                            self.stats['total_likes'] += 1
                            self.log("❤️ Curtiu o vídeo!")
                            time.sleep(2)
                            break
                        except:
                            continue
                except:
                    self.log("⚠️ Não foi possível curtir")
            
            # Scroll final
            driver.execute_script("window.scrollBy(0, 200)")
            time.sleep(random.uniform(1, 3))
            
            return True
            
        except Exception as e:
            self.log(f"❌ Erro ao assistir vídeo: {e}")
            return False
    
    def executar(self, num_views=1, modo='normal'):
        self.rodando = True
        self.log(f"🚀 Iniciando bot com {num_views} visualizações")
        self.log(f"📋 Total de URLs: {len(self.urls)}")
        
        for i in range(num_views):
            if not self.rodando:
                break
            
            url = random.choice(self.urls)
            self.log(f"\n📱 Visualização {i+1}/{num_views}")
            
            try:
                driver = self.configurar_driver()
                
                if modo == 'stealth':
                    resolucoes = [(1920,1080), (1366,768), (1536,864)]
                    resolucao = random.choice(resolucoes)
                    driver.set_window_size(resolucao[0], resolucao[1])
                
                sucesso = self.assistir_video(url, driver)
                
                if sucesso:
                    self.stats['total_views'] += 1
                    self.stats['videos_visitados'].append({
                        'url': url,
                        'timestamp': datetime.now().isoformat()
                    })
                    self.log(f"✅ Visualização {i+1} concluída!")
                else:
                    self.log(f"❌ Falha na visualização {i+1}")
                
                driver.quit()
                
            except Exception as e:
                self.log(f"❌ Erro: {e}")
                continue
            
            if i < num_views - 1:
                pausa = random.uniform(30, 60)
                self.log(f"⏳ Aguardando {pausa:.0f} segundos...")
                time.sleep(pausa)
        
        self.log("✅ Processo concluído!")
        self.rodando = False
        return self.stats
    
    def parar(self):
        self.rodando = False
        self.log("🛑 Bot interrompido")
    
    def adicionar_url(self, url):
        url = url.replace('\ufeff', '').strip()
        if url not in self.urls and url.startswith('https://'):
            self.urls.append(url)
            os.makedirs('dados', exist_ok=True)
            with open('dados/urls.txt', 'w', encoding='utf-8-sig') as f:
                for u in self.urls:
                    f.write(f"{u}\n")
            return True
        return False

bot_instance = None

def get_bot():
    global bot_instance
    if bot_instance is None:
        bot_instance = TikTokBot()
    return bot_instance