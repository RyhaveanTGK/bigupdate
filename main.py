import os
import asyncio
import logging
import threading

from pyrogram import Client, idle
from convopyro import Conversation
from config import *
from plugin_loader import load_extra_plugins, load_plugin_file
from languages import init_language_manager
import i18n

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
)

logger = logging.getLogger("userbot")

print("═" * 50)
print("🤖 RYHAVEAN USERBOT v1.0.0")
print("═" * 50)
print("Starting Userbot...")
print("═" * 50)

async def main():
    # Bütün çıxan mesajları aktiv dilə çevirən hook (az/tr/en)
    i18n.install_hook()
    i18n.bind_storage(user_sessions)

    # Get session string from environment or user input
    session_string = SESSION_STR if SESSION_STR else input("Enter your Pyrogram session string: ")

    # Initialize bot client with bot-specific plugins only. The bot is optional —
    # it only powers inline/special-group features. Skip it entirely when no
    # BOT_TOKEN is configured so nothing registers a dead client in apps["app"].
    app = None
    if BOT_TOKEN:
        app = Client(
            "main_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True,
            sleep_threshold=30,
            plugins=dict(root="bot")
        )

        # Initialize conversation for the bot
        Conversation(app)

    # Initialize userbot client with userbot-specific plugins
    userbot = Client(
        "userbot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
        plugins=dict(root="userbot")
    )
    
    # Initialize conversation for userbot
    Conversation(userbot)

    try:
        # Start bot client if it was created. A bot failure (e.g. FLOOD_WAIT
        # on auth.ImportBotAuthorization) must NOT take down the userbot — the
        # bot client only powers inline/special-group features. Only a client
        # that actually connected goes into apps["app"]: tools._BotProxy falls
        # back to the userbot when it's absent, but a dead client parked there
        # would defeat that fallback and raise ConnectionError instead.
        if app is not None:
            try:
                await app.start()
                apps["app"] = app
                print(f"Bot started successfully!")
                print(f"Bot logged in as: {app.me.first_name} (@{app.me.username})")
            except Exception as e:
                print(f"Bot client failed to start (continuing without it): {e}")

        # Start userbot client
        await userbot.start()
        print(f"Userbot started successfully!")
        print(f"Userbot logged in as: {userbot.me.first_name} (@{userbot.me.username})")

        # Add to clients dict for compatibility
        clients[userbot.me.id] = userbot

        # Dili MongoDB-dən yüklə (restartdan sonra da yadda qalır)
        i18n.bind_storage(user_sessions, userbot.me.id)
        active_lang = i18n.load_lang_from_db(userbot.me.id)
        print(f"Aktiv dil / Active language: {active_lang}")

        # MongoDB-də saxlanılan istifadəçi plaginlərini bərpa et və yüklə
        try:
            from userbot.plugin_installer import restore_user_plugins, PLUGINS_DIR
            restored = restore_user_plugins(userbot.me.id)
            for name in restored:
                path = os.path.join(PLUGINS_DIR, str(userbot.me.id), f"{name}.py")
                try:
                    load_plugin_file(userbot, path, name)
                    loaded_extra_plugins.append(name)
                except Exception as e:
                    logger.warning(f"Plugin '{name}' yüklənmədi / could not load: {e}")
            if restored:
                print(f"MongoDB-dən bərpa olunan plaginlər: {', '.join(restored)}")
        except Exception as e:
            logger.warning(f"Plaginlər bərpa olunmadı / plugin restore failed: {e}")

        # Load sudo users from database
        user_data = user_sessions.find_one({"user_id": userbot.me.id})
        if user_data and "sudoers" in user_data:
            SUDO[userbot.me.id] = user_data["sudoers"]

        # Load external community plugins (no repo fork needed)
        loaded_extra_plugins.extend(load_extra_plugins(userbot, EXTRA_PLUGINS_DIR))
        if loaded_extra_plugins:
            print(f"Loaded {len(loaded_extra_plugins)} extra plugin(s): {', '.join(loaded_extra_plugins)}")

    except Exception as e:
        print(f"Error starting clients: {e}")
    await idle()

def start_uptime_robot():
    """Start Uptime Robot HTTP server in a separate thread for Render deployment"""
    try:
        import uptimerobot
        port = int(os.getenv('PORT', 8000))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(uptimerobot.start_uptime_monitor())
    except Exception as e:
        logger.warning(f"Could not start Uptime Robot server: {e}")


if __name__ == "__main__":
    # Check if running on Render
    if os.getenv('DEPLOYMENT_PLATFORM') == 'render' or os.getenv('RENDER'):
        logger.info("🌐 Detected Render deployment - starting Uptime Robot handler")
        # Start uptime robot in a separate thread
        uptime_thread = threading.Thread(target=start_uptime_robot, daemon=True)
        uptime_thread.start()
    
    print("═" * 50)
    logger.info("🚀 Ryhavean Userbot is starting...")
    print("═" * 50)
    asyncio.run(main())