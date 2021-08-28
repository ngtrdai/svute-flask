from Svute_Flask.models import Code, Code_syntax
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from Svute_Flask import db
from Svute_Flask.codes.form import PostCode, ViewCode, EditCode

codes = Blueprint('codes', __name__)


@codes.route('/code', methods=['POST', 'GET'])
@login_required
def code():
    myCodes = Code.query.filter_by(author=current_user).order_by(Code.code_id.desc()).limit(3).all()
    lastCodes = Code.query.order_by(Code.code_id.desc()).limit(5).all()
    
    form = PostCode()
    form.syntax.choices = [syntax.name for syntax in Code_syntax.query.all()]
    if form.validate_on_submit():
        source = form.sourceCode.data
        title = "Không có tiêu đề"
        description = ""
        if form.title.data:
            title = form.title.data
        if form.description.data:
            description = form.description.data
        code = Code(source = source, user_id = current_user.id, title=title, description=description, syntax=Code_syntax.query.filter_by(name=form.syntax.data).first())
        db.session.add(code)
        db.session.commit()
        flash('Đăng code thành công!', 'success')
        return redirect(url_for('codes.code'))
    
    return render_template('codes/index.html', user=current_user, form = form, title = "Code", myCodes=myCodes, lastCodes=lastCodes)

@codes.route('/code/<string:slug>', methods=['POST','GET'])
def viewCode(slug):
    form = ViewCode()
    code = Code.query.filter_by(slug=slug).first()
    code.views += 1
    db.session.commit()
    form.title.data = code.title
    form.description.data = code.description
    form.sourceCode.data = code.source
    return render_template('codes/viewCode.html', user=current_user, code=code, form = form)

@codes.route('/nhung/<string:slug>')
def embed(slug):
    form = ViewCode()
    code = Code.query.filter_by(slug=slug).first()
    code.views += 1
    form.sourceCode.data = code.source
    return render_template('codes/embed.html', title=code.title, form = form, code=code)

@codes.route('/code/<string:slug>/xoa', methods=['POST', 'GET'])
def deleteCode(slug):
    code = Code.query.filter_by(slug=slug).first()
    if code:
        if code.author == current_user or current_user.role.name == "admin":
            db.session.delete(code)
            db.session.commit()
            flash('Xóa thành công!', 'success')
    return redirect(url_for('codes.code'))

@codes.route('/code/<string:slug>/sua', methods=['GET','POST'])
def editCode(slug):
    form = EditCode()
    myCodes = Code.query.filter_by(author=current_user).order_by(Code.code_id.desc()).limit(3).all()
    lastCodes = Code.query.order_by(Code.code_id.desc()).limit(5).all()
    code = Code.query.filter_by(slug=slug).first()
    if current_user == code.author or current_user.role.name == "admin":
        form.syntax.choices = [syntax.name for syntax in Code_syntax.query.all()]
        if form.validate_on_submit():
            code.source = form.sourceCode.data
            code.title = form.title.data
            code.description = form.description.data
            code.syntax = Code_syntax.query.filter_by(name=form.syntax.data).first()
            db.session.commit()
            flash('Cập nhật thành công!', 'success')
            return redirect(url_for('codes.viewCode', slug=code.slug))
        form.sourceCode.data = code.source
        form.title.data = code.title
        form.description.data = code.description
        form.syntax.data = code.syntax
        return render_template('codes/index.html', user=current_user, form=form, myCodes=myCodes, lastCodes=lastCodes)
    else:
        flash("Bạn không có quyền để sửa", "warning")
        return redirect(url_for('codes.viewCode', slug=code.slug))
