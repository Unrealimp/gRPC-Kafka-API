from fastapi import FastAPI, HTTPException
import grpc
from proto import statistics_pb2, statistics_pb2_grpc

app = FastAPI()
channel = grpc.insecure_channel('statistics-service:50051')
stub = statistics_pb2_grpc.StatisticsServiceStub(channel)

@app.get("/posts/{post_id}/stats", summary="Общая статистика по посту")
def get_post_stats(post_id: int):
    try:
        response = stub.GetPostStats(statistics_pb2.PostIdRequest(post_id=post_id))
        return {
            "views": response.views,
            "likes": response.likes,
            "comments": response.comments
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get("/posts/{post_id}/dynamics/views", summary="Динамика просмотров по дням")
def get_views_dynamics(post_id: int, start_date: str, end_date: str):
    try:
        request = statistics_pb2.PostDynamicsRequest(
            post_id=post_id,
            start_date=start_date,
            end_date=end_date
        )
        response = stub.GetPostViewsDynamics(request)
        return [{"date": item.date, "value": item.value} for item in response.data]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get("/posts/{post_id}/dynamics/likes", summary="Динамика лайков по дням")
def get_likes_dynamics(post_id: int, start_date: str, end_date: str):
    try:
        request = statistics_pb2.PostDynamicsRequest(
            post_id=post_id,
            start_date=start_date,
            end_date=end_date
        )
        response = stub.GetPostLikesDynamics(request)
        return [{"date": item.date, "value": item.value} for item in response.data]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get("/posts/{post_id}/dynamics/comments", summary="Динамика комментариев по дням")
def get_comments_dynamics(post_id: int, start_date: str, end_date: str):
    try:
        request = statistics_pb2.PostDynamicsRequest(
            post_id=post_id,
            start_date=start_date,
            end_date=end_date
        )
        response = stub.GetPostCommentsDynamics(request)
        return [{"date": item.date, "value": item.value} for item in response.data]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get("/top/posts", summary="Топ-10 постов по метрике")
def get_top_posts(metric: str = "views"):
    valid_metrics = ["views", "likes", "comments"]
    if metric not in valid_metrics:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid metric. Allowed: {', '.join(valid_metrics)}"
        )
    
    try:
        response = stub.GetTopPosts(statistics_pb2.TopRequest(metric=metric))
        return [{"post_id": item.post_id, "value": item.value} for item in response.posts]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get("/top/users", summary="Топ-10 пользователей по активности")
def get_top_users(metric: str = "views"):
    valid_metrics = ["views", "likes", "comments"]
    if metric not in valid_metrics:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid metric. Allowed: {', '.join(valid_metrics)}"
        )
    
    try:
        response = stub.GetTopUsers(statistics_pb2.TopRequest(metric=metric))
        return [{"user_id": item.user_id, "value": item.value} for item in response.users]
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")