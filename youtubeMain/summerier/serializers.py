from rest_framework import serializers
from .utils import extract_video_id

class summaryreqserializer(serializers.Serializer):
    yt_link=serializers.URLField(required=True)
    summary_type=serializers.ChoiceField(
                choices=[
                ('standard', 'Standard'),
                ('detailed', 'Detailed'),
                ('code', 'Code'),
                ('bullet_points', 'Bullet Points'),
                ('mindmap', 'Mind Map'),
                            
                ],default='standerd'
            )

    language=serializers.CharField(required=False,default='english')
    def validate_yt_link(self, value):
        video_id=extract_video_id(value)
        
        if not video_id:
            raise serializers.ValidationError("invalid youtube link")
        return value