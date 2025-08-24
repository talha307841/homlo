"""
Redis configuration and client management
"""

import json
from typing import Optional, Any, Dict
import redis.asyncio as redis
from app.core.config import settings

# Redis client instance
redis_client: Optional[redis.Redis] = None


async def init_redis() -> redis.Redis:
    """Initialize Redis connection"""
    global redis_client
    
    if redis_client is None:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            health_check_interval=30,
        )
        
        # Test connection
        await redis_client.ping()
    
    return redis_client


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    if redis_client is None:
        await init_redis()
    return redis_client


async def close_redis() -> None:
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


# Cache functions
async def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """Set cache value with expiration"""
    try:
        redis_client = await get_redis()
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        return await redis_client.setex(key, expire, value)
    except Exception:
        return False


async def get_cache(key: str) -> Optional[Any]:
    """Get cache value"""
    try:
        redis_client = await get_redis()
        value = await redis_client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    except Exception:
        return None


async def delete_cache(key: str) -> bool:
    """Delete cache key"""
    try:
        redis_client = await get_redis()
        return bool(await redis_client.delete(key))
    except Exception:
        return False


async def clear_pattern(pattern: str) -> int:
    """Clear cache keys matching pattern"""
    try:
        redis_client = await get_redis()
        keys = await redis_client.keys(pattern)
        if keys:
            return await redis_client.delete(*keys)
        return 0
    except Exception:
        return 0


# Rate limiting functions
async def increment_rate_limit(key: str, window: int = 60) -> int:
    """Increment rate limit counter"""
    try:
        redis_client = await get_redis()
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, window)
        return current
    except Exception:
        return 0


async def check_rate_limit(key: str, limit: int) -> bool:
    """Check if rate limit exceeded"""
    try:
        redis_client = await get_redis()
        current = await redis_client.get(key)
        return int(current or 0) < limit
    except Exception:
        return True


# Session management
async def set_session(session_id: str, user_data: Dict[str, Any], expire: int = 86400) -> bool:
    """Set user session data"""
    return await set_cache(f"session:{session_id}", user_data, expire)


async def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Get user session data"""
    return await get_cache(f"session:{session_id}")


async def delete_session(session_id: str) -> bool:
    """Delete user session"""
    return await delete_cache(f"session:{session_id}")


# WebSocket connection management
async def add_ws_connection(user_id: str, connection_id: str) -> bool:
    """Add WebSocket connection for user"""
    try:
        redis_client = await get_redis()
        await redis_client.sadd(f"ws:user:{user_id}", connection_id)
        await redis_client.expire(f"ws:user:{user_id}", 3600)  # 1 hour
        return True
    except Exception:
        return False


async def remove_ws_connection(user_id: str, connection_id: str) -> bool:
    """Remove WebSocket connection for user"""
    try:
        redis_client = await get_redis()
        await redis_client.srem(f"ws:user:{user_id}", connection_id)
        return True
    except Exception:
        return False


async def get_user_ws_connections(user_id: str) -> list:
    """Get all WebSocket connections for user"""
    try:
        redis_client = await get_redis()
        return await redis_client.smembers(f"ws:user:{user_id}")
    except Exception:
        return []


# Chat message caching
async def cache_chat_message(thread_id: str, message_data: Dict[str, Any]) -> bool:
    """Cache recent chat message"""
    key = f"chat:thread:{thread_id}:recent"
    return await set_cache(key, message_data, 86400)  # 24 hours


async def get_recent_chat_message(thread_id: str) -> Optional[Dict[str, Any]]:
    """Get recent chat message for thread"""
    key = f"chat:thread:{thread_id}:recent"
    return await get_cache(key)


# Notification caching
async def add_user_notification(user_id: str, notification: Dict[str, Any]) -> bool:
    """Add user notification to cache"""
    key = f"notifications:user:{user_id}"
    try:
        redis_client = await get_redis()
        # Add to list (newest first)
        await redis_client.lpush(key, json.dumps(notification))
        # Keep only last 50 notifications
        await redis_client.ltrim(key, 0, 49)
        await redis_client.expire(key, 86400)  # 24 hours
        return True
    except Exception:
        return False


async def get_user_notifications(user_id: str, limit: int = 20) -> list:
    """Get user notifications from cache"""
    key = f"notifications:user:{user_id}"
    try:
        redis_client = await get_redis()
        notifications = await redis_client.lrange(key, 0, limit - 1)
        return [json.loads(n) for n in notifications]
    except Exception:
        return []


# Health check
async def redis_health_check() -> bool:
    """Check Redis health"""
    try:
        redis_client = await get_redis()
        await redis_client.ping()
        return True
    except Exception:
        return False
