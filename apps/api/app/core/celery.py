"""
Celery configuration for background tasks
"""

import os
from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "homlo",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.image_processing",
        "app.tasks.email_tasks",
        "app.tasks.sms_tasks",
        "app.tasks.booking_tasks",
        "app.tasks.cleanup_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        "app.tasks.image_processing.*": {"queue": "images"},
        "app.tasks.email_tasks.*": {"queue": "emails"},
        "app.tasks.sms_tasks.*": {"queue": "sms"},
        "app.tasks.booking_tasks.*": {"queue": "bookings"},
        "app.tasks.cleanup_tasks.*": {"queue": "cleanup"},
    },
    
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.TIMEZONE,
    enable_utc=True,
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Task execution
    task_always_eager=settings.DEBUG,  # Execute tasks synchronously in debug mode
    task_eager_propagates=True,
    
    # Result backend
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Beat schedule (for periodic tasks)
    beat_schedule={
        "cleanup-expired-sessions": {
            "task": "app.tasks.cleanup_tasks.cleanup_expired_sessions",
            "schedule": 3600.0,  # Every hour
        },
        "cleanup-old-notifications": {
            "task": "app.tasks.cleanup_tasks.cleanup_old_notifications",
            "schedule": 86400.0,  # Every day
        },
        "send-booking-reminders": {
            "task": "app.tasks.booking_tasks.send_booking_reminders",
            "schedule": 3600.0,  # Every hour
        },
        "process-payouts": {
            "task": "app.tasks.booking_tasks.process_payouts",
            "schedule": 3600.0,  # Every hour
        },
    },
    
    # Task time limits
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,  # 10 minutes
    
    # Worker time limits
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Monitoring
    worker_state_db="worker_state.db",
    
    # Error handling
    task_reject_on_worker_lost=True,
    task_acks_late=True,
    
    # Queue configuration
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
    
    # Redis specific settings
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=10,
    
    # Result backend settings
    result_backend_transport_options={
        "master_name": "mymaster",
        "visibility_timeout": 3600,
    },
)

# Task annotations for specific tasks
celery_app.conf.task_annotations = {
    "app.tasks.image_processing.process_listing_images": {
        "rate_limit": "10/m",  # 10 per minute
        "time_limit": 300,     # 5 minutes
    },
    "app.tasks.email_tasks.send_bulk_emails": {
        "rate_limit": "100/m",  # 100 per minute
        "time_limit": 600,      # 10 minutes
    },
    "app.tasks.sms_tasks.send_bulk_sms": {
        "rate_limit": "50/m",   # 50 per minute
        "time_limit": 300,      # 5 minutes
    },
}

# Task routing for different environments
if settings.ENVIRONMENT == "production":
    celery_app.conf.update(
        task_always_eager=False,
        worker_prefetch_multiplier=4,
        worker_max_tasks_per_child=500,
        task_soft_time_limit=600,
        task_time_limit=1200,
    )


# Task base class with common functionality
class HomloTask(celery_app.Task):
    """Base task class with common functionality"""
    
    abstract = True
    
    def on_success(self, retval, task_id, args, kwargs):
        """Task success callback"""
        super().on_success(retval, task_id, args, kwargs)
        # Log success
        print(f"Task {task_id} completed successfully")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Task failure callback"""
        super().on_failure(exc, task_id, args, kwargs, einfo)
        # Log failure
        print(f"Task {task_id} failed: {exc}")
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Task retry callback"""
        super().on_retry(exc, task_id, args, kwargs, einfo)
        # Log retry
        print(f"Task {task_id} retrying: {exc}")


# Register the base task class
celery_app.Task = HomloTask


# Health check task
@celery_app.task(bind=True, base=HomloTask)
def health_check(self):
    """Health check task for monitoring"""
    return {
        "status": "healthy",
        "task_id": self.request.id,
        "worker": self.request.hostname,
    }


# Test task
@celery_app.task(bind=True, base=HomloTask)
def test_task(self, message: str = "Hello from Celery!"):
    """Test task for development"""
    return {
        "message": message,
        "task_id": self.request.id,
        "worker": self.request.hostname,
    }


# Task monitoring
@celery_app.task(bind=True, base=HomloTask)
def monitor_task_queue(self):
    """Monitor task queue status"""
    from app.core.redis import get_redis
    import asyncio
    
    async def get_queue_info():
        redis_client = await get_redis()
        # Get queue lengths
        queues = ["default", "images", "emails", "sms", "bookings", "cleanup"]
        queue_info = {}
        
        for queue in queues:
            length = await redis_client.llen(f"celery:{queue}")
            queue_info[queue] = length
        
        return queue_info
    
    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        queue_info = loop.run_until_complete(get_queue_info())
    finally:
        loop.close()
    
    return {
        "queue_info": queue_info,
        "worker": self.request.hostname,
        "timestamp": self.request.utcnow().isoformat(),
    }


if __name__ == "__main__":
    celery_app.start()
