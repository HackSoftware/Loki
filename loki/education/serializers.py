from rest_framework import serializers

from .models import CheckIn, Solution, Task
from .validators import (validate_github_solution_url,
                         validate_github_project_url)


class SolutionStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ('status', 'test_output', 'return_code')

    def get_status(self, obj):
        return obj.get_status()


class SolutionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    task = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Task.objects.all(),
    )

    class Meta:
        model = Solution
        extra_kwargs = {'url': {'required': False}}
        fields = ('id', 'task', 'url', 'code', 'status', 'file',
                  'test_output', 'return_code', 'created_at')

    def get_status(self, obj):
        return obj.get_status()

    def validate(self, data):
        code = data.get('code', None)
        file = data.get('file', None)
        is_gradable = data['task'].gradable

        if is_gradable and code is None and file is None:
            validate_github_solution_url(data['url'])

        if not is_gradable:
            validate_github_project_url(data['url'])

        return data


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = ('id', 'date', 'student')
