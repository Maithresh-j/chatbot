import nest_asyncio
import os
import discord
from discord.ext import commands
import google.generativeai as genai
import asyncio

# Apply nest_asyncio for Colab
nest_asyncio.apply()

# Configuration
DISCORD_BOT_TOKEN = "your_discord_bot_token"
GOOGLE_API_KEY = "your_google_api_key"

# Set up Google Generative AI API
genai.configure(api_key=GOOGLE_API_KEY)

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(name="chat")
async def chat(ctx, *, prompt: str = None):
    """Generates a response using AI."""
    if not prompt:
        await ctx.send("❌ Please provide a message. Usage: `!chat <your message>`")
        return

    try:
        response = genai.generate_content(prompt)  # Correct API call
        generated_text = response.text if hasattr(response, "text") else None
        if not generated_text:
            raise ValueError("Empty response received from AI.")

        # Handle Discord's 2000-character limit
        if len(generated_text) > 2000:
            for chunk in [generated_text[i:i+2000] for i in range(0, len(generated_text), 2000)]:
                await ctx.send(chunk)
        else:
            await ctx.send(generated_text)

    except ValueError as ve:
        await ctx.send("Error: AI response was empty.")
        print(f"ValueError: {ve}")

    except google.generativeai.types.errors.APIError as api_err:
        await ctx.send("AI API error. Please try again later.")
        print(f"APIError: {api_err}")

    except Exception as e:
        await ctx.send("Unexpected error occurred.")
        print(f"General Error: {e}")

# Run the bot in an async loop
loop = asyncio.get_event_loop()
loop.create_task(bot.start(DISCORD_BOT_TOKEN))
await asyncio.Future()
