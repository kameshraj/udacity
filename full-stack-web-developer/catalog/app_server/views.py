
from flask import flash, render_template, redirect, jsonify, url_for, session, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime


# import our app
from app_server import app, db, lm, oid, models, schemas, my_forms

# register user_loader to flask-login
@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

# helper methods
def time_now():
    datetime.utcnow()

# All the routes are defined here

# Show Catalog home
@app.route('/')
@app.route('/index/')
def showcategories():
    return render_template('categories.html', title='Catalog Directory', categories=models.Categories.query.all(),
                           items=models.Items.query.order_by(models.Items.updated_on.desc()).limit(10).all())

# Show a category
@app.route('/category/<int:c_id>/')
def showCategory(c_id):
    category = models.Categories.query.get(c_id)
    if not category:
        flash('category id %s not found.' % c_id)
        return redirect('/')

    items = models.Items.query.filter_by(category_id=c_id).all()
    title = 'Catelog Directory - Category - %s' % category.name
    form = my_forms.CategoryForm()

    return render_template('show_category.html', title=title, form=form, category=category, items=items)


# user should be logged in to add
@app.route('/add-category', methods=['GET', 'POST'])
@login_required
def addCategory():
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


# Delete category
@app.route('/category/<int:c_id>/delete', methods=['GET', 'POST'])
@login_required
def deletecategory(c_id):
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
    item = models.Items.query.get(i_id)
    if not item:
        flash('Item %s is not found' %i_id)
        return redirect('/')

    title = 'Catalog Directory - Item - %s' % item.name
    form = my_forms.ItemForm()

    return render_template('show_item.html', title=title, form=form, item=item)


# user should be logged in to add
@app.route('/add-item', methods=['GET', 'POST'])
@login_required
def addItem():
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


# Edit Item
@app.route('/item/<int:i_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(i_id):
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


# Delete Item
@app.route('/item/<int:i_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(i_id):
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
    categories = models.Categories.query.all()
    serializer = schemas.categories_schema
    result = serializer.dump(categories)
    return jsonify({"Categories": result.data})

# All login stuff here
@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect('/')

    form = my_forms.LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    return render_template('login.html', title='Sign In', form=form,
                           providers=app.config['OPENID_PROVIDERS'])

# before we login, associate user to flask-login
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = time_now()
        db.session.add(g.user)
        db.session.commit()

# after login, add user if new and redirect to page accessed
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))

    user = models.User.query.filter_by(email=resp.email).first()

    # if we don't have this user before, add it
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        tnow = time_now()
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
    #return redirect('/')

# logout user
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')