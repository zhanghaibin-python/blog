from celery import shared_task
from django_redis import get_redis_connection
from .models import Article
from django.db.models import F

@shared_task()
def sync_article_views():
    """
    将 Redis 中的阅读增量同步到 MySQL
    """

    redis_conn = get_redis_connection("default")

    # 使用 san_iter 避免阻塞
    keys = redis_conn.scan_iter("article:views:*")

    synced_count = 0

    for key in keys:
        try:
            # Redis 返回的是 bytes， 需要 decode
            key_str = key.decode()
            incr = redis_conn.get(key)
            
            if not incr:
                continue
                
            incr = int(incr)
            if incr <= 0:
                continue

            # 解析 article_id
            article_id = int(key_str.split(":")[-1])
            
            # 原子更新数据库
            Article.objects.filter(id=article_id).update(
                views=F("views") + incr
            )
            
            # 重点优化：使用 decrby 扣减已同步的数量，而不是直接置 0
            # 这样如果在同步期间有新的阅读量产生（比如变成 15），这里只减去 10，剩下的 5 下次同步
            redis_conn.decrby(key, incr)

            synced_count += 1

        except Exception as e:
            # 不要让某些影响，影响整体同步
            print(f"Sync error for key {key}: {e}")

    return f"Sync completed. Synced {synced_count} keys."
