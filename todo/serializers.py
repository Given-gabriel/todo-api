from rest_framework import serializers
from .models import Task
import pytz

class TaskSerializer(serializers.ModelSerializer):
    timezone = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def validate(self,data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time should be before end time.")
        
        if data.get('remind_at') and data['remind_at'] >= data['start_time']:
            raise serializers.ValidationError("Reminder time should be before start time")
        return data
    
    
    def create(self,validated_data):
        tz_name = validated_data.pop('timezone', None)
        if tz_name:
            tz = pytz.timezone(tz_name)
            for key in ['start_time', 'end_time']:
                dt = validated_data[key]
                if dt.tzinfo is None:
                    validated_data[key] = tz.localize(dt).astimezone(pytz.UTC)
                else:
                    validated_data[key] = dt.astimezone(pytz.UTC)

        return super().create(validated_data)
    
    def to_representation(self, instance):
        #use default serialization
        data = super().to_representation(instance)

        #Get timezone from request query param
        request = self.context.get('request')
        tz_name = request.query_params.get("timezone") if request else None

        if tz_name:
            try:
                tz = pytz.timezone(tz_name)
                #convert UTC datetime string back to user's timezone
                start = instance.start_time.astimezone(tz)
                end = instance.end_time.astimezone(tz)
                data['start_time'] = start.isoformat()
                data['end_time'] = end.isoformat()
            except Exception:
                pass #Fallback to default UTC

        return data