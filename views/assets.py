from flask import Blueprint, request, render_template, redirect, url_for, flash

from models.asset import Asset
from models.user import requires_login, requires_admin

asset_blueprint = Blueprint('assets', __name__)


@asset_blueprint.route('/')
@requires_login
def index():
    assets = Asset.all()

    data = [asset.json() for asset in assets]

    if data:
        # create dynamic table header
        headings = data[0].keys()
        key_headings = [heading.title() for heading in headings if heading != '_id']
        key_headings[3] = key_headings[3].upper()
        key_headings.append('Action')

        # extract the price and make the sum of all of them
        data_values = [datum.values() for datum in data]
        total = sum(list(asset)[7] for asset in data_values)

        # get the number of current assets
        number_of_assets = len(assets)

        # get the device statuses and number of offline devices.
        all_statuses = [list(asset)[8] for asset in data_values]

        offline_status = [offline for offline in all_statuses if offline == 'Offline']
        unknown_status = [offline for offline in all_statuses if offline != 'Offline' or 'Online']
        offline_assets = len(offline_status)

        return render_template('assets/asset_index.html', assets=assets, key_headings=key_headings, total=total,
                               number_of_assets=number_of_assets, offline_assets=offline_assets,
                               unknown_status=unknown_status)

    return render_template('assets/asset_index.html', assets=assets)


@asset_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def create_asset():
    create_asset_session = []

    if request.method == 'POST':
        device_type = request.form['type']
        model = request.form['model']
        name = request.form['name']
        ip = request.form['ip']
        subnet = request.form['subnet']
        floor = request.form['floor']
        room = request.form['room']
        price = request.form['price']
        status = request.form['status']

        create_asset_session.append(
            {
                'device_type': device_type,
                'model': model,
                'name': name,
                'ip': ip,
                'subnet': subnet,
                'floor': floor,
                'room': room,
                'price': price,
                'status': status
            }
        )

        new_asset_data = [datum for datum in create_asset_session[0].values()]
        for data in new_asset_data:
            if len(data) <= 0:
                flash('Please fill in all the fields.', 'danger')
                return render_template("assets/new_asset.html")

        try:
            Asset(device_type.title(), model.title(), name.title(),
                  ip, subnet, floor, room, float(price),
                  status.title()).save_to_mongo()
        except ValueError:
            flash('Invalid input for price. Please enter numbers only (0-.9)', 'danger')
        else:
            return redirect(url_for('.index'))

    # What happens if it's a GET request
    return render_template("assets/new_asset.html")


@asset_blueprint.route('/edit/<string:asset_id>', methods=['GET', 'POST'])
@requires_admin
def edit_asset(asset_id):
    asset = Asset.get_by_id(asset_id)

    if request.method == 'POST':
        device_name = request.form['type']
        model = request.form['model']
        name = request.form['name']
        ip = request.form['ip']
        subnet = request.form['subnet']
        floor = request.form['floor']
        price = request.form['price']
        room = request.form['room']
        status = request.form['status']

        asset.type = device_name.title()
        asset.model = model.title()
        asset.name = name.title()
        asset.ip = ip
        asset.subnet = subnet
        asset.floor = floor
        asset.room = room
        asset.status = status.title()

        try:
            asset.price = float(price)
            asset.save_to_mongo()
        except ValueError:
            flash('Invalid input for price. Please enter numbers only (0-.9)', 'danger')
        else:
            return redirect(url_for('.index'))

    return render_template('assets/edit_asset.html', asset=asset)


@asset_blueprint.route('/delete/<string:asset_id>')
@requires_admin
def delete_asset(asset_id):
    Asset.get_by_id(asset_id).remove_from_mongo()
    return redirect(url_for('.index'))
