from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .engine import GameEngine
from .serializers import ManageGameSerializer, MoveGameSerializer
from drf_yasg.utils import swagger_auto_schema

game_instances = {}
games_count = 0


class ManageGameAPIView(APIView):
    @swagger_auto_schema(request_body=ManageGameSerializer)
    def post(self, request):
        global games_count, game_instances
        serializer = ManageGameSerializer(data=request.data)
        if serializer.is_valid():
            method = serializer.validated_data['method']
            if method.lower() == "start":
                new_game = GameEngine()
                game_instances[games_count] = new_game
                games_count += 1
                return Response({
                    'message': 'Game started successfully',
                    'board': new_game.get_board(),
                    'game_id': games_count - 1
                }, status=status.HTTP_200_OK)
            elif method.lower() == "stop":
                game_id = serializer.validated_data['game_id']
                if game_id is None:
                    return Response({'error': 'For method: stop you need to pass game_id parameter'},
                                    status=status.HTTP_400_BAD_REQUEST)
                game = game_instances.get(game_id, None)
                if game is None:
                    return Response({'error': 'Game id not found'},
                                    status=status.HTTP_404_NOT_FOUND)
                del game_instances[game_id]
                return Response({"message": "Game stopped"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': f'Unsupported method: {method.lower()}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameStateAPIView(APIView):
    def get(self, request, game_id):
        global game_instances
        if game_id not in game_instances:
            return Response({'error': 'No game instance found. Please start a game first.'},
                            status=status.HTTP_404_NOT_FOUND)
        game = game_instances[game_id]
        return Response({
            'board': game.get_board(),
            'game_over': game.game_over,
            'winner': game.winner,
            'current_player': game.current_player
        }, status=status.HTTP_200_OK)


class MoveAPIView(APIView):
    @swagger_auto_schema(request_body=MoveGameSerializer)
    def post(self, request, game_id):
        global game_instances
        serializer = MoveGameSerializer(data=request.data)
        if serializer.is_valid():
            move_from = request.data.get("move_from")
            move_to = request.data.get('move_to')
            if move_from is None or move_to is None:
                return Response({'error': 'Not valid params.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                move_from = int(move_from)
                move_to = int(move_to)
            except ValueError:
                return Response({'error': 'Move parameters must be integers.'}, status=status.HTTP_400_BAD_REQUEST)

            if game_id not in game_instances:
                return Response({'error': 'No game instance found. Please start a game first.'},
                                status=status.HTTP_404_NOT_FOUND)
            game = game_instances[game_id]
            response = game.make_move(move_from, move_to)
            if "Invalid" not in response:
                return Response({'message': 'Move successful', 'board': game.get_board()})
            else:
                return Response({'error': response}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
