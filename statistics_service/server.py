from concurrent import futures
import grpc
from clickhouse_driver import Client
from proto import statistics_pb2, statistics_pb2_grpc

class StatisticsService(statistics_pb2_grpc.StatisticsServiceServicer):
    def __init__(self):
        self.ch_client = Client(host='clickhouse')
    
    def GetPostStats(self, request, context):
        query = """
            SELECT 
                sum(views) AS views,
                sum(likes) AS likes,
                sum(comments) AS comments
            FROM post_statistics_mv
            WHERE post_id = %(post_id)s
        """
        result = self.ch_client.execute(query, {'post_id': request.post_id})
        return statistics_pb2.PostStatsResponse(
            views=result[0][0] or 0,
            likes=result[0][1] or 0,
            comments=result[0][2] or 0
        )
    
    def _get_dynamics(self, request, event_type):
        query = f"""
            SELECT 
                toDate(event_time) AS date,
                count() AS value
            FROM post_events
            WHERE 
                post_id = %(post_id)s
                AND event_type = %(event_type)s
                AND date >= %(start_date)s
                AND date <= %(end_date)s
            GROUP BY date
            ORDER BY date
        """
        params = {
            'post_id': request.post_id,
            'event_type': event_type,
            'start_date': request.start_date,
            'end_date': request.end_date
        }
        result = self.ch_client.execute(query, params)
        return [statistics_pb2.DynamicsItem(date=str(row[0]), value=row[1]) for row in result]
    
    def GetPostViewsDynamics(self, request, context):
        data = self._get_dynamics(request, 'view')
        return statistics_pb2.DynamicsResponse(data=data)
    
    def GetPostLikesDynamics(self, request, context):
        data = self._get_dynamics(request, 'like')
        return statistics_pb2.DynamicsResponse(data=data)
    
    def GetPostCommentsDynamics(self, request, context):
        data = self._get_dynamics(request, 'comment')
        return statistics_pb2.DynamicsResponse(data=data)
    
    def GetTopPosts(self, request, context):
        metric_map = {
            "views": "sum(views)",
            "likes": "sum(likes)",
            "comments": "sum(comments)"
        }
        metric_expr = metric_map.get(request.metric, "sum(views)")
        
        query = f"""
            SELECT 
                post_id,
                {metric_expr} AS value
            FROM post_statistics_mv
            GROUP BY post_id
            ORDER BY value DESC
            LIMIT 10
        """
        result = self.ch_client.execute(query)
        items = [statistics_pb2.TopPostsResponse.Item(post_id=row[0], value=row[1]) for row in result]
        return statistics_pb2.TopPostsResponse(posts=items)
    
    def GetTopUsers(self, request, context):
        metric_map = {
            "views": "countIf(event_type = 'view')",
            "likes": "countIf(event_type = 'like')",
            "comments": "countIf(event_type = 'comment')"
        }
        metric_expr = metric_map.get(request.metric, "count()")
        
        query = f"""
            SELECT 
                user_id,
                {metric_expr} AS value
            FROM post_events
            GROUP BY user_id
            ORDER BY value DESC
            LIMIT 10
        """
        result = self.ch_client.execute(query)
        items = [statistics_pb2.TopUsersResponse.Item(user_id=row[0], value=row[1]) for row in result]
        return statistics_pb2.TopUsersResponse(users=items)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    statistics_pb2_grpc.add_StatisticsServiceServicer_to_server(
        StatisticsService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()