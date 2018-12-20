from sanic import Blueprint

generic_bp = Blueprint('generic_blueprint')


@generic_bp.route('/')
async def index(request):
    return request.app.templating.render_template('index.html', name='David', request=request)
