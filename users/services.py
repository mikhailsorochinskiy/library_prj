from .models import User

class UserService:

    @staticmethod
    def add_points(email, points):
        try:
            user = User.objects.get(email=email)
            user.points += points
            user.is_tested = True
            user.save()

            return {
                'success': True,
                'user': email,
                'points_added': points,
                'total_points': user.points,
                'message': f'Баллы успешно добавлены. Текущий баланс: {user.points}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Ошибка на стороне сервера - {e}. Баллы не были добавлены'
            }
