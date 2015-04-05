
from flask import flash, render_template, redirect, jsonify, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
import sys

# import our app and needed things from it
from app_server import app, db, lm, oid, models, schemas, my_forms

@lm.user_loader
def load_user(id):
    """
    Register our user to flask-login module's user_loader

    Arguments:
        id: User ID
    """
    return models.User.query.get(int(id))

# helper methods
def time_now():
    """
    Will return current UTC timestamp

    Arguments:
        None

    return:
        Current timestamp in UTC
    """
    return datetime.utcnow()


# All the routes are defined here

@app.route('/')
@app.route('/index/')
def showcategories():
    """
    Renders Categories form which is also the home page for this app.

    Arguments:
        None
    """
    return render_template('categories.html', title='Catalog Directory', categories=models.Categories.query.all(),
                           items=models.Items.query.order_by(models.Items.updated_on.desc()).limit(10).all())


@app.route('/category/<int:c_id>/')
def showCategory(c_id):
    """
    Show a given category

    Arguments:
        c_id: Category ID to be displayed
    """
    category = models.Categories.query.get(c_id)
    if not category:
        flash('category id %s not found.' % c_id)
        return redirect('/')

    items = models.Items.query.filter_by(category_id=c_id).all()
    title = 'Catelog Directory - Category - %s' % category.name
    form = my_forms.CategoryForm()

    return render_template('show_category.html', title=title, form=form, category=category, items=items)


@app.route('/add-category', methods=['GET', 'POST'])
@login_required
def addCategory():
    """
    Renders form to add a Category. Only logged in users can access this page.
    Unauthorized user will be redirected to Login page

    Arguments:
        None
    """
    form = my_forms.CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        user = g.user.get_id()
        category = models.Categories(name=name, created_by=user)

        try:
            db.session.add(category)
        except:
            e = sys.exc_info()[0]
            flash('Error adding category %s.' % name)
            flash('Error: %s' % e)
            db.session.rollback()
            return redirect('/')
        else:
            db.session.commit()
            flash('category {%s} is added.' % name)
            return redirect('/')

    # if form not yet submitted draw the page again
    return render_template('add_category.html', title='Add category', form=form)


# Edit category
@app.route('/category/<int:c_id>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(c_id):
    """
    Renders form to edit a category. Only logged in users can access this page,
    Unauthorized user will be redirected to Login page. Also makes sure only user
    who added this Category can only edit it.

    Arguments:
        c_id: Category ID to edit
    """
    category = models.Categories.query.get(c_id)
    if not category:
        flash('category id %s not found.' %c_id)
        return redirect('/')

    user = int(g.user.get_id())
    if user != category.created_by:
        flash('Can be edited only by user who added this category')
        return redirect('/')

    form = my_forms.CategoryForm()
    name = category.name
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        flash('category {%s} is renamed to {%s}.' % (name, category.name))
        return redirect('/category/%s' % c_id)

    title = 'Catalog Directory - Edit category - %s' % name
    form.name.data = name
    return render_template('edit_category.html', title=title, form=form, category=category)


@app.route('/category/<int:c_id>/delete', methods=['GET', 'POST'])
@login_required
def deletecategory(c_id):
    """
    Renders form to delete a category. Only logged in users can access this page,
    Unauthorized user will be redirected to Login page. Also makes sure only user
    who added this Category can only delete it.

    Arguments:
       c_id: Category ID to edit
    """
    category = models.Categories.query.get(c_id)
    if not category:
        flash('category id %s not found.' % c_id)
        return redirect('/')

    user = int(g.user.get_id())
    if user != category.created_by:
        flash('Can be delete only by user who added this category')
        return redirect('/')

    form = my_forms.OptionalForm()
    if form.validate_on_submit():
        # delete all items in this category
        i_del = models.Items.query.filter_by(category_id=c_id).delete()
        flash('Deleted %s items from Category: %s' % (i_del, category.name))

        db.session.delete(category)
        db.session.commit()
        flash('category {%s} is deleted.' % category.name)
        return redirect('/')

    title = 'Catalog Directory - Delete category - %s' % category.name
    return render_template('delete_category.html', title=title, form=form, category=category)


# Show an item
@app.route('/item/<int:i_id>/')
def showItem(i_id):
    """
    Show a given Item

    Arguments:
        i_id: Item ID to be displayed
    """
    item = models.Items.query.get(i_id)
    if not item:
        flash('Item %s is not found' %i_id)
        return redirect('/')

    title = 'Catalog Directory - Item - %s' % item.name
    form = my_forms.ItemForm()

    return render_template('show_item.html', title=title, form=form, item=item)


@app.route('/add-item', methods=['GET', 'POST'])
@login_required
def addItem():
    """
    Renders form to add an Item. Only logged in users can access this page.
    Unauthorized user will be redirected to Login page

    Arguments:
        None
    """
    form = my_forms.ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category = form.category.data
        user = g.user.get_id()

        item = models.Items(name=name, description=description, category_id=category, created_by=user)

        try:
            db.session.add(item)
        except:
            e = sys.exc_info()[0]
            flash('Error adding Item %s.' % name)
            flash('Error: %s' % e)
            db.session.rollback()
            return redirect('/')
        else:
            db.session.commit()
            flash('Item {%s} is added.' % name)
            return redirect('/')

    # if form not yet submitted draw the page again
    return render_template('add_item.html', title='Add an Item', form=form, categories=models.Categories.query.all())


@app.route('/item/<int:i_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(i_id):
    """
    Renders form to edit an Item. Only logged in users can access this page,
    Unauthorized user will be redirected to Login page. Also makes sure only user
    who added this Item can only edit it.

    Arguments:
        i_id: Item ID to edit
    """
    item = models.Items.query.get(i_id)
    if not item:
        flash('Item id %s not found.' %i_id)
        return redirect('/')

    user = int(g.user.get_id())
    if user != item.created_by:
        flash('Can be edited only by user who added this item')
        return redirect('/')

    form = my_forms.ItemForm()
    name = item.name
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category_id = form.category.data
        db.session.add(item)
        db.session.commit()
        flash('Item {%s} is modified.' % name)
        return redirect('/item/%s' % i_id)

    title = 'Catalog Directory - Edit Item - %s' % name
    form.name.data = name
    form.category.data = item.category_id
    form.description.data = item.description
    categories = models.Categories.query.all()
    return render_template('edit_item.html', title=title, form=form, item=item, categories=categories)


@app.route('/item/<int:i_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(i_id):
    """
    Renders form to delete an Item. Only logged in users can access this page,
    Unauthorized user will be redirected to Login page. Also makes sure only user
    who added this Category can only delete it.

    Arguments:
       i_id: Item ID to edit
    """
    item = models.Items.query.get(i_id)
    if not item:
        flash('Item id %s not found.' %i_id)
        return redirect('/')

    user = int(g.user.get_id())
    if user != item.created_by:
        flash('Can be deleted only by user who added this item')
        return redirect('/')

    form = my_forms.OptionalForm()
    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        flash('Item {%s} is deleted.' % item.name)
        return redirect('/')

    title = 'Catalog Directory - Delete Item - %s' % item.name
    return render_template('delete_item.html', title=title, form=form, item=item)

# All JSON stuff here
@app.route('/catalog.json')
def catalogJson():
    """
    Returns a JSON list of all Categories and Items in each of them
    """
    categories = models.Categories.query.all()
    serializer = schemas.categories_schema
    result = serializer.dump(categories)
    return jsonify({"Categories": result.data})


#### All login stuff here ###
@lm.user_loader
def load_user(id):
    """
    Returns user for given user ID

    Arguments:
        id: User ID

    return:
        User
    """
    return models.User.query.get(int(id))


@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """
    Renders Login form for user to Login using OpenIDs. If session has an user
    already logged just return to home page
    """
    # if logged in already, just return
    if g.user is not None and g.user.is_authenticated():
        return redirect('/')

    form = my_forms.LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    return render_template('login.html', title='Sign In', form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.before_request
def before_request():
    """
    populates flash user for our session and updates last seen time for this user
    """
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = time_now()
        db.session.add(g.user)
        db.session.commit()

# after login, add user if new and redirect to page accessed
@oid.after_login
def after_login(resp):
    """
    Parses the response received from OpenID servers. If this is a new user
    add them to Users table

    Arguments:
        resp: Response form OpenID server
    """

    # If OpenID response didn't have an email ID, force login again
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))

    # if we don't have this user in our database before, add them
    user = models.User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]

        user = models.User(nickname=nickname, email=resp.email)

        try:
            db.session.add(user)
        except:
            e = sys.exc_info()[0]
            flash('Error adding User %s.' % name)
            flash('Error: %s' % e)
            db.session.rollback()
            return redirect('/')
        else:
            db.session.commit()

        flash('User {%s} is added.' % nickname)

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or '/')


@app.route('/logout')
def logout():
    """
    Logout User and redirect to home page
    """
    logout_user()
    return redirect('/')