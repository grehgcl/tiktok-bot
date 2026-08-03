from bot import TikTokBot

print("🚀 Testando o bot...")
bot = TikTokBot()
print(f"📹 URLs carregadas: {len(bot.urls)}")

print("\n📱 Executando 1 visualização...")
resultado = bot.executar(num_views=1, modo='normal')

print(f"\n📊 Resultado:")
print(f"✅ Views: {resultado['total_views']}")
print(f"❤️ Likes: {resultado['total_likes']}")