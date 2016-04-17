from flask import render_template, request, Blueprint, jsonify

###############
#### FLASK ####
###############

sam_api_tester_bp = Blueprint('sam_api_tester', __name__, template_folder='templates', static_folder='static',
                              static_url_path='/sam_xml_api_tester/static')

@sam_api_tester_bp.route('/sam_xml_api_tester', methods=['GET','POST'])
def sam_api_tester():
    if request.method == 'GET':
        return render_template('sam_xml_api_tester.html')

    # handle POST method from JQuery (will be filled later)
    elif request.method == 'POST':
        return 0