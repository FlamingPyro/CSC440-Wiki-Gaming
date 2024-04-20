"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Flask
from flask import session
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user



import logging
from wiki.core import Processor
from wiki.web.forms import EditorForm
from wiki.web.forms import LikeForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web.forms import CommentForm
from wiki.web.forms import AddToCartForm
from wiki.web.forms import ShoppingInfoForm
from wiki.web.forms import PurchasingForm
from wiki.web.forms import CreateForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect

from .models import ShoppingInfo, HomeDatabase, Helldivers, Tekken, LethalCompany, Minecraft, Destiny, Palworld, EldenRing, HorizonForbiddenWest

from .extensions import db




bp = Blueprint('wiki', __name__)


@bp.route('/', methods=['GET', 'POST'])
@protect
def home():
    form = AddToCartForm()
    if form.validate_on_submit():
        game_id = request.form.get('game_id')
        game = HomeDatabase.query.get(game_id)
        if game:
            game_info = {'id': game.id, 'name': game.name, 'price': game.price}
            session.setdefault('cart', []).append(game_info)
            flash('Game added to cart!', 'success')
            return redirect(url_for('wiki.shopping_cart'))

    home_data = HomeDatabase.query.all()
    return render_template('home.html', form=form, home_data=home_data)


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    index_pages = list()
    for page in pages:
        if 'user' not in page.url:
            index_pages.append(page)
    return render_template('index.html', pages=index_pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']

@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/Tekken/', methods=('GET', 'POST'))
@protect
def tekken():
    return render_page('Tekken', "tekken", Tekken)
@bp.route('/Destiny/', methods=('GET', 'POST'))
@protect
def destiny():
    return render_page('Destiny 2', "destiny", Destiny)
@bp.route('/Elden/', methods=('GET', 'POST'))
@protect
def eldenring():
    return render_page('Elden Ring', "eldenring", EldenRing)
@bp.route('/Horizon/', methods=('GET', 'POST'))
@protect
def horizonforbiddenwest():
    return render_page('Horizon Forbidden West', "horizonforbiddenwest", HorizonForbiddenWest)
@bp.route('/Lethal/', methods=('GET', 'POST'))
@protect
def lethalcompany():
    return render_page('Lethal Company', "lethalcompany", LethalCompany)
@bp.route('/Minecraft/', methods=('GET', 'POST'))
@protect
def minecraft():
    return render_page('Minecraft', "minecraft", Minecraft)
@bp.route('/Palworld/', methods=('GET', 'POST'))
@protect
def palworld():
    return render_page('Palworld', "palworld", Palworld)
@bp.route('/Helldivers/', methods=('GET', 'POST'))
@protect
def helldivers():
    return render_page('Helldivers', "helldivers", Helldivers)


def render_page(page_title, page_name, db_model):
    form = CommentForm()
    likeform = LikeForm()
    purchasingform = AddToCartForm()
    column_data = db_model.query.with_entities(db_model.comments, db_model.username).all()
    num_likes = db_model.query.order_by(db_model.id).first().numLikes
    if form.validate_on_submit():
        new_info = db_model(
            comments=form.comment.data,
            username=current_user.name
        )
        db.session.add(new_info)
        db.session.commit()
        form = CommentForm()
        return redirect(url_for('wiki.' + page_name))
    elif likeform.validate_on_submit():
        comment = db_model.query.order_by(db_model.id).first()
        if comment:
            increment_likes(comment.id, db_model)
        return redirect(url_for('wiki.' + page_name + ''))
    return render_template(page_name + '.html', page={'title': page_title}, form=form, column_data=column_data, numLikes=num_likes, likeform=likeform, purchasingform=purchasingform)

def increment_likes(item_id, db_model):
    item = db_model.query.get(item_id)
    if item:
        item.numLikes += 1
        db.session.commit()


@bp.route('/shopping_cart/', methods=['GET', 'POST'])
@protect
def shopping_cart():
    form = ShoppingInfoForm()
    total_price = 0
    if form.validate_on_submit():
        new_info = ShoppingInfo(
            name=form.name.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data,
            zipcode=form.zipcode.data,
            email=form.email.data,
            phone_number=form.phone_number.data
        )
        db.session.add(new_info)
        db.session.commit()

        return redirect(url_for('wiki.purchasing'))

    game_info = session.get('cart')
    if game_info:
        for item in game_info:
            total_price += float(item['price'])

    return render_template('shopping_cart.html', form=form,
                           game_info=game_info, total_price=total_price)



@bp.route('/remove_from_cart', methods=['POST'])
@protect
def remove_from_cart():
    game_id = request.form.get('game_id')
    if 'cart' in session:
        updated_cart = [item for item in session['cart'] if item['id'] != int(game_id)]
        session['cart'] = updated_cart
    flash('Item removed from cart!', 'success')
    return redirect(url_for('wiki.shopping_cart'))

@bp.route('/success_page', methods=['GET', 'POST'])
@protect
def success_page():
    shopping_info = ShoppingInfo.query.all()
    return render_template('success_page.html', shopping_info=shopping_info)

@bp.route('/purchasing/', methods=['GET', 'POST'])
@protect
def purchasing():
    form = PurchasingForm()
    if form.validate_on_submit():
        return redirect(url_for('wiki.success_page'))
    return render_template('purchasing_form.html', form=form)

@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.home'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/user/page/', methods=['GET'])
def user_page():
    user_id = current_user.get_id()
    page = current_wiki.get(f'user/{user_id}')
    if page:
        return render_template('page.html', page=page)
    else:
        flash('This user does not have a page. Create one now:')
        return redirect(request.args.get("next") or url_for('wiki.edit', url=(f'user/{user_id}/')))


@bp.route('/user/create/', methods=['GET', 'POST'])
def user_create():
    form = CreateForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        user = (current_users.add_user(name=username, password=password, authentication_method='cleartext'))
        login_user(user)
        user.set('authenticated', True)
        user_id = user.get_id()
        flash('Account Creation successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.edit', url=(f'user/{user_id}/')))
    return render_template('account.html', form=form)


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
