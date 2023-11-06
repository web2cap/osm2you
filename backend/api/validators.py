from rest_framework import serializers


def validate_length_gte10(value):
    if len(value) < 10:
        raise serializers.ValidationError("Text must be at least 10 characters long.")
