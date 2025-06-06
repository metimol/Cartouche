# Djoser settings for full user info on /api/auth/users
DJOSER = {
    'SERIALIZERS': {
        'user': 'api.serializers.FullUserSerializer',
        'current_user': 'api.serializers.FullUserSerializer',
        'user_create': 'api.serializers.FullUserSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    }
}
