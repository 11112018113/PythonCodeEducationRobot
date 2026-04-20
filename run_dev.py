import asyncio
import sys
from main import FamilyBot
from config.settings import settings


async def main():
    print("=" * 50)
    print("FamilyBot Development Mode")
    print("Using GGUF models for local testing")
    print("=" * 50)

    settings.dev_mode = True
    bot = FamilyBot()
    await bot.initialize()

    print("\n Ready! Type 'quit' to exit.")

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            response = await bot.process_message(user_input)
            print(f"\n[Coordinator] → {response.to_agent}")
            print(f"[Response] {response.payload.get('response', 'No response')}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

    print("\nShutting down...")
    await bot.shutdown()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())