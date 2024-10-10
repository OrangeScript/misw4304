from src.commands.base_command import BaseCommand
from flask import jsonify


class HealthCheck(BaseCommand):
    
    def execute(self):
        health_status = {"message": "pong"}
        return jsonify(health_status), 200