# Общая статистика по посту
curl http://localhost:8000/posts/123/stats

# Динамика просмотров
curl "http://localhost:8000/posts/123/dynamics/views?start_date=2023-01-01&end_date=2023-12-31"

# Топ постов по лайкам
curl "http://localhost:8000/top/posts?metric=likes"

# Топ пользователей по комментариям
curl "http://localhost:8000/top/users?metric=comments"