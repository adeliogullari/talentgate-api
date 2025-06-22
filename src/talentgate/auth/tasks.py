import asyncio

from config import get_settings

settings = get_settings()


async def schedule_purge_expired_task():
    while True:
        print("🏁 elected as scheduler leader.")
        await asyncio.sleep(settings.refresh_token_expiration)


# purge_expired_task = asyncio.create_task(schedule_purge_expired_task())
# purge_expired_task.cancel()

# scheduler_task = None  # Global to track the background task

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
#     global scheduler_task
#
#     hostname = os.getenv("HOSTNAME", "")
#     is_leader = hostname.endswith("-1")
#
#     if is_leader:
#         print(f"🏁 {hostname} elected as scheduler leader.")
#         scheduler_task = asyncio.create_task(run_scheduler())
#     else:
#         print(f"⏸️ {hostname} skipping background job.")
#
#     yield  # Start the app
#
#     # Shutdown logic
#     if scheduler_task:
#         scheduler_task.cancel()
#         try:
#             await scheduler_task
#         except asyncio.CancelledError:
#             print("🛑 Scheduler task cancelled cleanly.")
#
# app = FastAPI(lifespan=lifespan)
#
# @app.get("/")
# async def root():
#     return {"message": "FastAPI app with internal scheduler"}
