from prometheus_client import generate_latest
from sanic import Blueprint
from sanic.response import text

system_bp = Blueprint('system_blueprint')


@system_bp.route('/metrics')
async def metrics(request):
    return text(generate_latest().decode())
